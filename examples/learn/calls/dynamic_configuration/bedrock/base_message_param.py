from mirascope.core import BaseDynamicConfig, BaseMessageParam, bedrock


@bedrock.call("anthropic.claude-3-haiku-20240307-v1:0")
def recommend_book(genre: str) -> BaseDynamicConfig:
    return {
        "messages": [
            BaseMessageParam(role="user", content=f"Recommend a {genre} book")
        ],
        "call_params": {"max_tokens": 512},
        "metadata": {"tags": {"version:0001"}},
    }


response = recommend_book("fantasy")
print(response.content)
