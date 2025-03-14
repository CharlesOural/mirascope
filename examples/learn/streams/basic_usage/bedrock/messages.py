from mirascope.core import Messages, bedrock


@bedrock.call("anthropic.claude-3-haiku-20240307-v1:0", stream=True)
def recommend_book(genre: str) -> Messages.Type:
    return Messages.User(f"Recommend a {genre} book")


stream = recommend_book("fantasy")
for chunk, _ in stream:
    print(chunk.content, end="", flush=True)

print(f"Content: {stream.content}")

call_response = stream.construct_call_response()
print(f"Usage: {call_response.usage}")
