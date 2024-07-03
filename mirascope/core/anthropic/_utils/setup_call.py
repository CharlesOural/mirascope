"""This module contains the setup_call function for the Anthropic API."""

import inspect
from typing import Any, Awaitable, Callable

from anthropic import (
    Anthropic,
    AnthropicBedrock,
    AnthropicVertex,
    AsyncAnthropic,
    AsyncAnthropicBedrock,
    AsyncAnthropicVertex,
)
from anthropic.types import Message, MessageParam

from ...base import BaseTool, _utils
from ..call_params import AnthropicCallParams
from ..dynamic_config import AnthropicDynamicConfig
from ..tool import AnthropicTool


def setup_call(
    *,
    model: str,
    client: Anthropic
    | AsyncAnthropic
    | AnthropicBedrock
    | AsyncAnthropicBedrock
    | AnthropicVertex
    | AsyncAnthropicVertex
    | None,
    fn: Callable[..., AnthropicDynamicConfig | Awaitable[AnthropicDynamicConfig]],
    fn_args: dict[str, Any],
    dynamic_config: AnthropicDynamicConfig,
    tools: list[type[BaseTool] | Callable] | None,
    json_mode: bool,
    call_params: AnthropicCallParams,
    extract: bool,
) -> tuple[
    Callable[..., Message] | Callable[..., Awaitable[Message]],
    str,
    list[dict[str, MessageParam]],
    list[type[AnthropicTool]] | None,
    dict[str, Any],
]:
    prompt_template, messages, tool_types, call_kwargs = _utils.setup_call(
        fn, fn_args, dynamic_config, tools, AnthropicTool, call_params
    )
    if messages[0]["role"] == "system":
        call_kwargs["system"] = messages.pop(0)["content"]
    if client is None:
        client = AsyncAnthropic() if inspect.iscoroutinefunction(fn) else Anthropic()
    create = client.messages.create
    call_kwargs |= {"model": model, "messages": messages}

    if json_mode:
        messages[-1]["content"] += _utils.json_mode_content(
            tool_types[0] if tool_types else None
        )
        call_kwargs.pop("tools", None)
    elif extract:
        assert tool_types, "At least one tool must be provided for extraction."
        call_kwargs["tool_choice"] = {"type": "tool", "name": tool_types[0]._name()}

    return create, prompt_template, messages, tool_types, call_kwargs
