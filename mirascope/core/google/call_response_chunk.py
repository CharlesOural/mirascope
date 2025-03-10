"""This module contains the `GoogleCallResponseChunk` class.

usage docs: learn/streams.md#handling-streamed-responses
"""

from typing import cast

from google.genai.types import FinishReason as GoogleFinishReason
from google.genai.types import GenerateContentResponse

from mirascope.core.base.types import FinishReason

from ..base import BaseCallResponseChunk
from ._utils._convert_finish_reason_to_common_finish_reasons import (
    _convert_finish_reasons_to_common_finish_reasons,
)


class GoogleCallResponseChunk(
    BaseCallResponseChunk[GenerateContentResponse, GoogleFinishReason]
):
    """A convenience wrapper around the Google API streamed response chunks.

    When calling the Google API using a function decorated with `google_call` and
    `stream` set to `True`, the stream will contain `GoogleCallResponseChunk` instances

    Example:

    ```python
    from mirascope.core import prompt_template
    from mirascope.core.google import google_call


    @google_call("google-1.5-flash", stream=True)
    def recommend_book(genre: str) -> str:
        return f"Recommend a {genre} book"


    stream = recommend_book("fantasy")  # response is an `GoogleStream`
    for chunk, _ in stream:
        print(chunk.content, end="", flush=True)
    ```
    """

    @property
    def content(self) -> str:
        """Returns the chunk content for the 0th choice."""
        return self.chunk.candidates[0].content.parts[0].text  # pyright: ignore [reportOptionalMemberAccess, reportOptionalSubscript, reportReturnType]

    @property
    def finish_reasons(self) -> list[GoogleFinishReason]:
        """Returns the finish reasons of the response."""
        return [
            candidate.finish_reason
            for candidate in (self.chunk.candidates or [])
            if candidate.finish_reason is not None
        ]

    @property
    def model(self) -> None:
        """Returns the model name.

        google.generativeai does not return model, so we return None
        """
        return None

    @property
    def id(self) -> str | None:
        """Returns the id of the response.

        google.generativeai does not return an id
        """
        return None

    @property
    def usage(self) -> None:
        """Returns the usage of the chat completion.

        google.generativeai does not have Usage, so we return None
        """
        return None

    @property
    def input_tokens(self) -> None:
        """Returns the number of input tokens."""
        return None

    @property
    def output_tokens(self) -> None:
        """Returns the number of output tokens."""
        return None

    @property
    def common_finish_reasons(self) -> list[FinishReason] | None:
        return _convert_finish_reasons_to_common_finish_reasons(
            cast(list[str], self.finish_reasons)
        )
