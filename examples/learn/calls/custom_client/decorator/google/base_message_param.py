from google.generativeai import GenerativeModel
from mirascope.core import BaseMessageParam, google


@google.call("", client=GenerativeModel(model_name="gemini-1.5-flash"))
def recommend_book(genre: str) -> list[BaseMessageParam]:
    return [BaseMessageParam(role="user", content=f"Recommend a {genre} book")]
