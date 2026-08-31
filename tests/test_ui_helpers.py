"""Focused tests for the shared interaction and progression contracts."""

import unittest
import inspect
from unittest.mock import patch

import ui_helpers


class _Context:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class _StreamlitStub:
    def __init__(self):
        self.session_state = {}
        self.buttons = []
        self.expanders = []
        self.html_fragments = []
        self.markdowns = []
        self.captions = []

    def columns(self, *_args, **_kwargs):
        return [_Context(), _Context(), _Context()]

    def container(self, **_kwargs):
        return _Context()

    def expander(self, label, **_kwargs):
        self.expanders.append(label)
        return _Context()

    def button(self, label, **kwargs):
        self.buttons.append(label)
        return False

    def info(self, *_args, **_kwargs):
        pass

    def success(self, *_args, **_kwargs):
        pass

    def write(self, *_args, **_kwargs):
        pass

    def markdown(self, body, **_kwargs):
        self.markdowns.append(body)

    def caption(self, body, **_kwargs):
        self.captions.append(body)

    def html(self, body, **_kwargs):
        self.html_fragments.append(body)

    def text_area(self, _label, *, key, **_kwargs):
        return self.session_state.setdefault(key, "")


class SharedInteractionTests(unittest.TestCase):
    def navigation(self, stub, step=0):
        ui_helpers.step_buttons(["One", "Two"], "tab", "step", "scroll", step, "test")
        return stub.buttons

    def test_hard_reveal_persists_and_exposes_downstream_state(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            self.assertFalse(ui_helpers.hard_reveal("Predict", "evidence", reveal_label="Reveal"))
            self.assertNotIn("Continue →", self.navigation(stub))
            stub.session_state["evidence"] = True
            self.assertTrue(ui_helpers.hard_reveal("Predict", "evidence", reveal_label="Reveal"))
            self.assertTrue(ui_helpers.hard_reveal("Predict", "evidence", reveal_label="Reveal"))

    def test_hard_reveal_leaves_cognitive_choreography_to_the_experience(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.hard_reveal("Compare the two groups.", "evidence", reveal_label="Reveal")
            self.assertEqual(stub.markdowns, [])
            self.assertEqual(stub.captions, [])

            ui_helpers.hard_reveal(
                "Compare the two groups.",
                "labelled_evidence",
                reveal_label="Reveal",
                pre_reveal_label="Compare first",
                pre_reveal_guidance="Agree on a comparison before revealing the evidence.",
            )
            self.assertIn("Compare first", stub.markdowns[0])
            self.assertEqual(stub.captions, ["Agree on a comparison before revealing the evidence."])

    def test_multiple_gates_require_all_requirements(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.completion_gate(False)
            ui_helpers.completion_gate(False)
            self.assertNotIn("Continue →", self.navigation(stub))
            stub.buttons.clear()
            ui_helpers.completion_gate(True)
            ui_helpers.completion_gate(False)
            self.assertNotIn("Continue →", self.navigation(stub))
            stub.buttons.clear()
            ui_helpers.completion_gate(True)
            ui_helpers.completion_gate(True)
            self.assertIn("Continue →", self.navigation(stub))

    def test_back_remains_available_when_continue_is_blocked(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.completion_gate(False)
            buttons = self.navigation(stub, step=1)
            self.assertIn("← Back", buttons)
            self.assertNotIn("Continue →", buttons)

    def test_gate_is_transient_between_stage_renders(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.completion_gate(False)
            self.assertNotIn("Continue →", self.navigation(stub))
            stub.buttons.clear()
            self.assertIn("Continue →", self.navigation(stub, step=0))

    def test_response_persists_and_teacher_guidance_is_visibility_only(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            self.assertEqual(ui_helpers.response_box("Respond", "stage_response"), "")
            stub.session_state["stage_response"] = "An observation"
            self.assertEqual(ui_helpers.response_box("Respond", "stage_response"), "An observation")
            ui_helpers.teacher_guidance("Stage", "Listen for evidence")
            self.assertEqual(stub.expanders, [])
            stub.session_state["teacher_view"] = True
            ui_helpers.teacher_guidance("Stage", "Listen for evidence")
            self.assertEqual(stub.expanders, ["Teacher guidance: Stage"])
            self.assertEqual(stub.session_state["stage_response"], "An observation")

    def test_resource_identity_uses_one_safe_grid_component(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            # The helper lives in visual_system because it is part of the visual shell;
            # this test guards the rendered contract without starting Streamlit.
            import visual_system

            with patch.object(visual_system, "st", stub):
                visual_system.resource_identity(
                    "Animal Traits <teaching> dataset",
                    logo_path=None,
                )

        self.assertEqual(len(stub.html_fragments), 1)
        fragment = stub.html_fragments[0]
        self.assertIn("grid-template-columns: max-content minmax(0, 1fr)", fragment)
        self.assertIn("grid-template-columns: minmax(0, 1fr)", fragment)
        self.assertIn("Animal Traits &lt;teaching&gt; dataset", fragment)
        self.assertNotIn("stHorizontalBlock", fragment)
        self.assertNotIn("data-testid=\"column\"", fragment)
        about_source = inspect.getsource(visual_system.render_resource_context)
        self.assertNotIn("st.columns", about_source)
        self.assertNotIn("data-testid", about_source)


if __name__ == "__main__":
    unittest.main()
