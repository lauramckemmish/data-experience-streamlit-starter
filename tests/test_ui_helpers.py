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
        self.button_kwargs = []
        self.expanders = []
        self.expander_kwargs = []
        self.html_fragments = []
        self.markdowns = []
        self.captions = []
        self.writes = []
        self.images = []
        self.containers = []
        self.column_args = []
        self.toggles = []

    def columns(self, *args, **kwargs):
        self.column_args.append((args, kwargs))
        count = len(args[0]) if args and isinstance(args[0], list) else (args[0] if args else 3)
        return [_Context() for _ in range(count)]

    def container(self, **_kwargs):
        self.containers.append(_kwargs)
        return _Context()

    def expander(self, label, **_kwargs):
        self.expanders.append(label)
        self.expander_kwargs.append(_kwargs)
        return _Context()

    def button(self, label, **kwargs):
        self.buttons.append(label)
        self.button_kwargs.append((label, kwargs))
        return False

    def info(self, *_args, **_kwargs):
        pass

    def success(self, *_args, **_kwargs):
        pass

    def write(self, body, **_kwargs):
        self.writes.append(body)

    def markdown(self, body, **_kwargs):
        self.markdowns.append(body)

    def caption(self, body, **_kwargs):
        self.captions.append(body)

    def image(self, image, **kwargs):
        self.images.append((image, kwargs))

    def html(self, body, **_kwargs):
        self.html_fragments.append(body)

    def text_area(self, _label, *, key, **_kwargs):
        return self.session_state.setdefault(key, "")

    def toggle(self, label, *, key, **_kwargs):
        self.toggles.append((label, key))
        return self.session_state.setdefault(key, False)


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

    def test_semantic_prompts_name_the_cognitive_job_without_gating(self):
        stub = _StreamlitStub()
        prompts = (
            (ui_helpers.notice_prompt, "Notice"),
            (ui_helpers.compare_prompt, "Compare"),
            (ui_helpers.predict_prompt, "Predict"),
            (ui_helpers.explain_prompt, "Explain"),
            (ui_helpers.conclude_prompt, "Conclude"),
            (ui_helpers.revise_prompt, "Revise"),
            (ui_helpers.recall_prompt, "Recall"),
        )
        with patch.object(ui_helpers, "st", stub):
            for render_prompt, label in prompts:
                render_prompt(f"{label} this evidence.")
            self.assertIn("Continue →", self.navigation(stub))

        self.assertEqual(len(stub.markdowns), len(prompts))
        for (_, label), markdown in zip(prompts, stub.markdowns):
            self.assertIn(label, markdown)
        self.assertEqual(
            stub.writes[: len(prompts)],
            [f"{label} this evidence." for _, label in prompts],
        )

    def test_self_check_is_collapsed_and_never_blocks_continue(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            with ui_helpers.self_check("Check your reading"):
                stub.write("Compare this with your own observation.")
            self.assertIn("Continue →", self.navigation(stub))

        self.assertEqual(stub.expanders, ["Self-check: Check your reading"])
        self.assertEqual(stub.expander_kwargs, [{"expanded": False}])

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

    def test_final_step_has_no_right_action_without_terminal_action(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            buttons = self.navigation(stub, step=1)
        self.assertEqual(buttons, ["← Back"])

    def test_terminal_action_is_rendered_on_the_final_step(self):
        stub = _StreamlitStub()

        def return_to_experiences():
            pass

        with patch.object(ui_helpers, "st", stub):
            ui_helpers.step_buttons(
                ["One", "Two"],
                "tab",
                "step",
                "scroll",
                1,
                "test",
                terminal_action=return_to_experiences,
                terminal_label="Back to experiences",
            )

        self.assertEqual(stub.buttons, ["← Back", "Back to experiences"])
        label, kwargs = stub.button_kwargs[-1]
        self.assertEqual(label, "Back to experiences")
        self.assertIs(kwargs["on_click"], return_to_experiences)
        self.assertEqual(kwargs["key"], "test_terminal")

    def test_terminal_action_requires_a_label(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            with self.assertRaisesRegex(ValueError, "terminal_label"):
                ui_helpers.step_buttons(
                    ["One", "Two"],
                    "tab",
                    "step",
                    "scroll",
                    1,
                    "test",
                    terminal_action=lambda: None,
                )

    def test_facilitator_notes_are_visibility_only_and_preparation_is_collapsed(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            self.assertEqual(ui_helpers.response_box("Respond", "stage_response"), "")
            stub.session_state["stage_response"] = "An observation"
            self.assertEqual(ui_helpers.response_box("Respond", "stage_response"), "An observation")
            ui_helpers.facilitator_preparation("Listen for evidence")
            self.assertEqual(stub.expanders, [])
            stub.session_state[ui_helpers.FACILITATOR_NOTES_KEY] = True
            ui_helpers.facilitator_preparation("Listen for evidence")
            self.assertEqual(stub.expanders, ["For facilitators"])
            self.assertEqual(stub.expander_kwargs, [{"expanded": False}])
            self.assertEqual(stub.session_state["stage_response"], "An observation")

    def test_facilitator_control_and_live_cues_use_only_canonical_labels(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.facilitator_notes_control()
            self.assertEqual(stub.toggles, [("Facilitator notes", ui_helpers.FACILITATOR_NOTES_KEY)])
            stub.session_state[ui_helpers.FACILITATOR_NOTES_KEY] = True
            for label in ui_helpers.FACILITATOR_LIVE_LABELS:
                ui_helpers.facilitator_live_cue(label, "A delivery decision.")
            with self.assertRaisesRegex(ValueError, "Unknown facilitator live cue"):
                ui_helpers.facilitator_live_cue("SKIP", "Not a canonical label.")

        self.assertEqual(len(stub.containers), 4)
        self.assertEqual(len(stub.markdowns), 4)
        self.assertEqual(stub.writes[-4:], ["A delivery decision."] * 4)

    def test_facilitator_orientation_is_conditional_and_student_safe(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.facilitator_orientation()
            self.assertEqual(stub.markdowns, [])
            self.assertEqual(stub.writes, [])

            stub.session_state[ui_helpers.FACILITATOR_NOTES_KEY] = True
            ui_helpers.facilitator_orientation()

        self.assertEqual(stub.markdowns, ["**Facilitator notes**"])
        orientation = stub.writes[-1]
        self.assertIn("walk through the learner experience", orientation)
        self.assertIn("Facilitator notes on", orientation)
        self.assertNotIn("answer", orientation.lower())

    def test_facilitator_notes_persist_across_ordinary_routes_without_touching_learning_state(self):
        from experiences import router

        stub = _StreamlitStub()
        stub.session_state.update(
            {
                ui_helpers.FACILITATOR_NOTES_KEY: True,
                "stage_response": "An observation",
                "curious_context_evidence": True,
                "_ui_helpers_continue_blocked": True,
            }
        )
        with patch.object(router, "st", stub):
            router.open_experience("Home")
            router.open_experience("Template Experience")
            router.open_experience("Pattern Reference")

        self.assertTrue(stub.session_state[ui_helpers.FACILITATOR_NOTES_KEY])
        self.assertEqual(stub.session_state["stage_response"], "An observation")
        self.assertTrue(stub.session_state["curious_context_evidence"])
        self.assertTrue(stub.session_state["_ui_helpers_continue_blocked"])

    def test_sample_note_separates_missing_and_overlapping_log_exclusions(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            ui_helpers.sample_note(
                1,
                6,
                missing=2,
                log_x_excluded=2,
                log_y_excluded=2,
                log_both_excluded=1,
                log_excluded=3,
                x_label="x",
                y_label="y",
            )

        note = stub.captions[-1]
        self.assertIn("2 omitted because a required value is missing", note)
        self.assertIn("3 additional records excluded", note)
        self.assertIn("2 on x; 2 on y", note)
        self.assertIn("counted once", note)

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

    def test_role_image_accepts_shared_roles_and_rejects_unknown_roles(self):
        stub = _StreamlitStub()
        roles = ("context", "evidence", "graph", "support", "hero")
        with patch.object(ui_helpers, "st", stub):
            for role in roles:
                ui_helpers.role_image("image.png", role=role, caption="Context", key=role)
            with self.assertRaisesRegex(ValueError, "Unknown image role"):
                ui_helpers.role_image("image.png", role="thumbnail")

        self.assertEqual(len(stub.images), 5)
        self.assertTrue(all(kwargs == {"caption": "Context", "width": "stretch"} for _, kwargs in stub.images))
        self.assertEqual(
            [container["key"] for container in stub.containers],
            [f"role_image_{role}_{role}" for role in roles],
        )

    def test_media_text_pair_uses_role_specific_ratios_and_rejects_non_pair_roles(self):
        stub = _StreamlitStub()
        with patch.object(ui_helpers, "st", stub):
            with ui_helpers.media_text_pair("context.png", role="context", caption="Context", key="context_pair"):
                stub.write("Associated explanation")
            with ui_helpers.media_text_pair("support.png", role="support", key="support_pair"):
                stub.write("Associated support")
            with self.assertRaisesRegex(ValueError, "context or support"):
                with ui_helpers.media_text_pair("graph.png", role="graph", key="invalid_pair"):
                    pass

        self.assertEqual(stub.column_args, [(([1, 1],), {"gap": "medium"}), (([1, 2],), {"gap": "medium"})])
        self.assertEqual(stub.images, [("context.png", {"caption": "Context", "width": "stretch"}), ("support.png", {"caption": None, "width": "stretch"})])
        self.assertEqual(stub.writes[-2:], ["Associated explanation", "Associated support"])

    def test_visual_system_defines_responsive_media_pair_structure(self):
        import visual_system

        styles = inspect.getsource(visual_system.apply_visual_system)
        self.assertIn('class*="st-key-media_text_"', styles)
        self.assertIn("@media (max-width:700px)", styles)
        self.assertIn("flex-direction:column", styles)

    def test_visual_system_uses_one_navy_facilitator_family(self):
        import visual_system

        self.assertEqual(visual_system.SEMANTIC_TOKENS["facilitator"], "#294C70")
        self.assertNotIn("facilitator_prep", visual_system.SEMANTIC_TOKENS)
        self.assertNotIn("facilitator_live", visual_system.SEMANTIC_TOKENS)
        self.assertNotEqual(
            visual_system.SEMANTIC_TOKENS["facilitator"],
            visual_system.SEMANTIC_TOKENS["secondary_accent"],
        )
        styles = inspect.getsource(visual_system.apply_visual_system)
        self.assertIn("--unsw-facilitator", styles)
        self.assertIn("overflow-wrap:anywhere", styles)


if __name__ == "__main__":
    unittest.main()
