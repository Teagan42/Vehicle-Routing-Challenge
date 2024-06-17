import argparse
import asyncio
from .app import App


def main():
    parser = argparse.ArgumentParser(
        description="Demonstrate a solution to the vehicle routing challenge."
    )
    parser.add_argument(
        "path_to_problem",
        type=str,
        help="The path to the file containing the problem set.",
    )
    args = parser.parse_args()

    app = App()

    asyncio.run(app.run(args.path_to_problem))


if __name__ == "__main__":
    main()
