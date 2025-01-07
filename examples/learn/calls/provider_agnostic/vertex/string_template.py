from mirascope.core import prompt_template

from mirascope import llm


@llm.call(provider="vertex", model="gemini-1.5-flash")
@prompt_template("Recommend a {genre} book")
def recommend_book(genre: str): ...


response = recommend_book("fantasy")
print(response.content)

override_response = llm.override(
    recommend_book,
    provider_override="anthropic",
    model_override="claude-3-5-sonnet-20240620",
    call_params_override={"temperature": 0.7},
)("fantasy")

print(override_response.content)
