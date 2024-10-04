import logfire
from mirascope.core import Messages, cohere
from mirascope.integrations.logfire import with_logfire
from pydantic import BaseModel

logfire.configure()


class Book(BaseModel):
    title: str
    author: str


@with_logfire()
@cohere.call("command-r-plus", response_model=Book)
def recommend_book(genre: str) -> Messages.Type:
    return Messages.User(f"Recommend a {genre} book")


print(recommend_book("fantasy"))
