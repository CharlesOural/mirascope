from mirascope.core import BaseMessageParam, openai
from pydantic import BaseModel


class Librarian(BaseModel):
    history: list[openai.OpenAIMessageParam] = []

    @openai.call("gpt-4o-mini")
    def _call(self, query: str) -> list[openai.OpenAIMessageParam]:
        return [
            BaseMessageParam(role="system", content="You are a librarian"),
            *self.history,
            BaseMessageParam(role="user", content=query),
        ]

    def run(self) -> None:
        while True:
            query = input("(User): ")
            if query in ["exit", "quit"]:
                break
            print("(Assistant): ", end="", flush=True)
            response = self._call(query)
            print(response.content)
            self.history += [
                BaseMessageParam(role="user", content=query),
                response.message_param,
            ]


Librarian().run()
