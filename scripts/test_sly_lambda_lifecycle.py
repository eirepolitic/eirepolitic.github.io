import anyio

from src.lambda_entry import build_app


async def main() -> None:
    first = build_app()
    async with first.router.lifespan_context(first):
        pass

    second = build_app()
    async with second.router.lifespan_context(second):
        pass

    assert first is not second


if __name__ == "__main__":
    anyio.run(main)
