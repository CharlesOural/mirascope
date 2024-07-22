"""Tests the `openai._utils.setup_call` module."""

import inspect
from unittest.mock import MagicMock, patch

import pytest
from openai import OpenAI

from mirascope.core.openai._utils.setup_call import setup_call
from mirascope.core.openai.tool import OpenAITool


@pytest.fixture()
def mock_base_setup_call() -> MagicMock:
    """Returns the mock setup_call function."""
    mock_setup_call = MagicMock()
    mock_setup_call.return_value = [MagicMock() for _ in range(3)] + [{}]
    return mock_setup_call


@patch(
    "mirascope.core.openai._utils.setup_call.convert_message_params",
    new_callable=MagicMock,
)
@patch("mirascope.core.openai._utils.setup_call._utils", new_callable=MagicMock)
def test_setup_call(
    mock_utils: MagicMock,
    mock_convert_message_params: MagicMock,
    mock_base_setup_call: MagicMock,
) -> None:
    """Tests the `setup_call` function."""
    mock_utils.setup_call = mock_base_setup_call
    fn = MagicMock()
    create, prompt_template, messages, tool_types, call_kwargs = setup_call(
        model="gpt-4o",
        client=None,
        fn=fn,
        fn_args={},
        dynamic_config=None,
        tools=None,
        json_mode=False,
        call_params={},
        extract=False,
    )
    assert prompt_template == mock_base_setup_call.return_value[0]
    assert tool_types == mock_base_setup_call.return_value[2]
    assert "model" in call_kwargs and call_kwargs["model"] == "gpt-4o"
    assert "messages" in call_kwargs and call_kwargs["messages"] == messages
    mock_base_setup_call.assert_called_once_with(fn, {}, None, None, OpenAITool, {})
    mock_convert_message_params.assert_called_once_with(
        mock_base_setup_call.return_value[1]
    )
    assert messages == mock_convert_message_params.return_value
    assert inspect.signature(create) == inspect.signature(
        OpenAI().chat.completions.create
    )


@patch(
    "mirascope.core.openai._utils.setup_call.convert_message_params",
    new_callable=MagicMock,
)
@patch("mirascope.core.openai._utils.setup_call._utils", new_callable=MagicMock)
def test_setup_call_json_mode(
    mock_utils: MagicMock,
    mock_convert_message_params: MagicMock,
    mock_base_setup_call: MagicMock,
) -> None:
    """Tests the `setup_call` function with JSON mode."""
    mock_utils.setup_call = mock_base_setup_call
    mock_utils.json_mode_content = MagicMock()
    mock_base_setup_call.return_value[1] = [
        {"role": "user", "content": [{"type": "text", "text": "test"}]}
    ]
    mock_base_setup_call.return_value[-1]["tools"] = MagicMock()
    mock_convert_message_params.side_effect = lambda x: x
    _, _, messages, _, call_kwargs = setup_call(
        model="gpt-4o",
        client=None,
        fn=MagicMock(),
        fn_args={},
        dynamic_config=None,
        tools=None,
        json_mode=True,
        call_params={},
        extract=False,
    )
    assert messages[-1]["content"][-1] == {  # type: ignore
        "type": "text",
        "text": mock_utils.json_mode_content.return_value,
    }
    assert "tools" not in call_kwargs

    mock_base_setup_call.return_value[1] = [
        {"role": "assistant", "content": [{"type": "text", "text": "test"}]}
    ]
    _, _, messages, _, call_kwargs = setup_call(
        model="gpt-4o",
        client=None,
        fn=MagicMock(),
        fn_args={},
        dynamic_config=None,
        tools=None,
        json_mode=True,
        call_params={},
        extract=False,
    )
    assert messages[-1] == {  # type: ignore
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": mock_utils.json_mode_content.return_value,
            }
        ],
    }


@patch(
    "mirascope.core.openai._utils.setup_call.convert_message_params",
    new_callable=MagicMock,
)
@patch("mirascope.core.openai._utils.setup_call._utils", new_callable=MagicMock)
def test_setup_call_extract(
    mock_utils: MagicMock,
    mock_convert_message_params: MagicMock,
    mock_base_setup_call: MagicMock,
) -> None:
    """Tests the `setup_call` function with extraction."""
    mock_utils.setup_call = mock_base_setup_call
    _, _, _, _, call_kwargs = setup_call(
        model="gpt-4o",
        client=None,
        fn=MagicMock(),
        fn_args={},
        dynamic_config=None,
        tools=None,
        json_mode=False,
        call_params={},
        extract=True,
    )
    assert "tool_choice" in call_kwargs and call_kwargs["tool_choice"] == "required"
