from mirascope.core import BaseMessageParam
from mirascope import llm


@llm.call(provider="anthropic", model="claude-3-5-sonnet-20240620")
def recommend_book(genre: str) -> list[BaseMessageParam]:
    return [BaseMessageParam(role="user", content=f"Recommend a {genre} book")]


response = recommend_book("fantasy")
print(response.content)

override_response = llm.override(
    recommend_book,
    provider="openai",
    model="gpt-4o-mini",
    call_params={"temperature": 0.7},
)("fantasy")

print(override_response.content)
