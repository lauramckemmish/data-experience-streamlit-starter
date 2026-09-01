"""Starter-specific route and burst interaction for classroom smoke testing."""

from __future__ import annotations

import sys
from pathlib import Path


class StarterClassroomAdapter:
    """Exercise the existing two-variable Data Playground flow.

    This starter has no subject-specific facilitated activity. The playground's
    dataset-preview disclosure is therefore the smallest real
    interactive flow available for a reusable infrastructure reference.
    """

    def streamlit_command(self, root: Path, port: int) -> list[str]:
        return [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            f"--server.port={port}",
            "--server.headless=true",
            "--server.fileWatcherType=none",
        ]

    async def arrive(self, page: object) -> None:
        await page.get_by_role("button", name="Data Exploration Playground", exact=True).click(no_wait_after=True)
        await page.get_by_role("heading", name="Data Exploration Playground", exact=True).first.wait_for()
        await page.get_by_text("Dataset preview", exact=True).wait_for()

    async def interact(self, page: object, round_number: int) -> None:
        await page.get_by_text("Dataset preview", exact=True).click()

    async def assert_usable(self, page: object) -> None:
        await page.get_by_role("heading", name="Data Exploration Playground", exact=True).first.wait_for()
        await page.get_by_text("Dataset preview", exact=True).wait_for()


ADAPTER = StarterClassroomAdapter()
