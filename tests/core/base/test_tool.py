"""Tests for the `tool` module."""

import pytest

from mirascope.core.base._utils import DEFAULT_TOOL_DOCSTRING
from mirascope.core.base.tool import BaseTool


def test_base_tool() -> None:
    """Tests the `BaseTool` class."""

    class FormatBook(BaseTool):
        """Returns a formatted book title and author."""

        title: str
        author: str

        def call(self) -> str:
            return f"{self.title} by {self.author}"

    tool = FormatBook(title="The Name of the Wind", author="Patrick Rothfuss")
    assert tool._name() == "FormatBook"
    assert tool._description() == "Returns a formatted book title and author."
    assert tool.args == {"title": "The Name of the Wind", "author": "Patrick Rothfuss"}
    assert tool.call() == "The Name of the Wind by Patrick Rothfuss"


@pytest.mark.asyncio
async def test_base_tool_call_async() -> None:
    """Tests the `BaseTool.call` method with an async function."""

    class FormatBook(BaseTool):
        """Returns a formatted book title and author."""

        title: str
        author: str

        async def call(self) -> str:
            return f"{self.title} by {self.author}"

    tool = FormatBook(title="The Name of the Wind", author="Patrick Rothfuss")
    assert await tool.call() == "The Name of the Wind by Patrick Rothfuss"


def test_base_tool_no_doc() -> None:
    """Tests the `BaseTool` class with no docstring."""
    from mirascope.core.base import BaseTool

    class FormatBook(BaseTool):
        title: str

    assert FormatBook._description() == DEFAULT_TOOL_DOCSTRING


def test_base_tool_custom_name() -> None:
    """Tests the `BaseTool` class with a custom name."""
    from mirascope.core.base import BaseTool

    class FormatBook(BaseTool):
        __custom_name__ = "format_book"

    assert FormatBook._name() == "format_book"
