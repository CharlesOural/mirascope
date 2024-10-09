from mirascope.core import vertex
from vertexai.generative_models import Content, Part


@vertex.call("gemini-1.5-flash")
def recommend_book(genre: str) -> vertex.VertexDynamicConfig:
    return {
        "messages": [
            Content(role="user", parts=[Part.from_text(f"Recommend a {genre} book")])
        ]
    }


response = recommend_book("fantasy")
print(response.content)
