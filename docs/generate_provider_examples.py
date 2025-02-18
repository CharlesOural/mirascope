import re
from pathlib import Path

from mirascope.llm import Provider
from pydantic import BaseModel


class ProviderInfo(BaseModel):
    """Provider information for UI and substitutions."""

    provider: Provider
    title: str
    model: str


PROVIDER_INFO: dict[Provider, ProviderInfo] = {
    "openai": ProviderInfo(provider="openai", title="OpenAI", model="gpt-4o-mini"),
    "anthropic": ProviderInfo(
        provider="anthropic", title="Anthropic", model="claude-3-5-sonnet-latest"
    ),
    "mistral": ProviderInfo(
        provider="mistral", title="Mistral", model="mistral-large-latest"
    ),
    "google": ProviderInfo(provider="google", title="Google", model="gemini-2.0-flash"),
    "groq": ProviderInfo(
        provider="groq", title="Groq", model="llama-3.1-70b-versatile"
    ),
    "cohere": ProviderInfo(provider="cohere", title="Cohere", model="command-r-plus"),
    "litellm": ProviderInfo(provider="litellm", title="LiteLLM", model="gpt-4o-mini"),
    "azure": ProviderInfo(provider="azure", title="Azure AI", model="gpt-4o-mini"),
    "bedrock": ProviderInfo(
        provider="bedrock",
        title="Bedrock",
        model="anthropic.claude-3-haiku-20240307-v1:0",
    ),
}


def substitute_provider_import(content: str, provider: Provider) -> str:
    """Substitute provider in import statement."""
    return re.sub(
        r"(from mirascope.core import .*?)openai(.*?)",
        rf"\1{provider}\2",
        content,
    )


def substitute_provider_cast(content: str, provider: Provider) -> str:
    """Substitute provider in cast statement."""
    provider_name = provider.capitalize()

    if provider == "litellm":
        provider_name = "LiteLLM"
    if provider == "openai":
        provider_name = "OpenAI"

    return re.sub(
        r"cast\(openai\.OpenAICallResponse,",
        f"cast({provider}.{provider_name}CallResponse,",
        content,
    )


def substitute_llm_call_decorator(content: str, provider: Provider) -> str:
    """Substitute provider and model into @llm.call decorator."""
    subs = PROVIDER_INFO[provider]

    # Use regex with re.DOTALL to match across lines
    decorator_pattern = r"@llm\.call\((.*?)\)"

    def replace_decorator(match: re.Match) -> str:
        decorator_args = match.group(1)

        # Check if we found the expected parameters
        if 'provider="openai"' not in decorator_args:
            raise ValueError(
                f"Could not find provider='openai' in decorator: {decorator_args}"
            )
        if 'model="gpt-4o-mini"' not in decorator_args:
            raise ValueError(
                f"Could not find model='gpt-4o-mini' in decorator: {decorator_args}"
            )

        # Make substitutions, preserving whitespace
        updated_args = decorator_args.replace(
            'provider="openai"', f'provider="{subs.provider}"'
        ).replace('model="gpt-4o-mini"', f'model="{subs.model}"')

        return f"@llm.call({updated_args})"

    # Perform substitution with re.DOTALL flag
    new_content, _ = re.subn(
        decorator_pattern, replace_decorator, content, flags=re.DOTALL
    )

    return new_content


def substitute_provider_specific_content(content: str, provider: Provider) -> str:
    """Apply all provider-specific substitutions."""
    if provider not in PROVIDER_INFO:
        raise ValueError(f"Provider {provider} not found in {PROVIDER_INFO}")

    content = substitute_llm_call_decorator(content, provider)
    content = substitute_provider_import(content, provider)
    content = substitute_provider_cast(content, provider)
    return content


SNIPPETS_DIR = Path("build/snippets")


def get_supported_providers() -> list[ProviderInfo]:
    return list(PROVIDER_INFO.values())


def generate_provider_examples(
    *, config: dict, examples_root: Path, snippets_dir: Path
) -> None:
    """Generate provider-specific examples for python files in configured paths."""
    # Clear/create snippets directory
    if snippets_dir.exists():
        for file in snippets_dir.rglob("*.py"):
            file.unlink()
    snippets_dir.mkdir(exist_ok=True, parents=True)
    supported_providers = get_supported_providers()

    example_dirs = config["extra"]["provider_example_dirs"]
    for example_dir in example_dirs:
        source_dir = examples_root / example_dir

        for base_file in source_dir.glob("*.py"):
            content = base_file.read_text()

            # Generate for each provider
            for info in supported_providers:
                # Create provider directory
                output_dir = snippets_dir / example_dir / info.provider

                output_dir.mkdir(parents=True, exist_ok=True)

                # Generate provider-specific version
                substituted = substitute_provider_specific_content(
                    content, info.provider
                )

                # Write to temporary file
                out_file = output_dir / base_file.name
                out_file.write_text(substituted)
