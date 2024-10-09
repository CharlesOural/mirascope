import asyncio

from mirascope.core import BaseTool, bedrock, prompt_template


class FormatBook(BaseTool):
    title: str
    author: str

    async def call(self) -> str:
        # Simulating an async API call
        await asyncio.sleep(1)
        return f"{self.title} by {self.author}"


@bedrock.call(model="anthropic.claude-3-haiku-20240307-v1:0", tools=[FormatBook])
@prompt_template("Recommend a {genre} book")
async def recommend_book(genre: str): ...


async def main():
    response = await recommend_book("fantasy")
    if tool := response.tool:
        if isinstance(tool, FormatBook):
            output = await tool.call()
            print(output)
    else:
        print(response.content)


asyncio.run(main())
