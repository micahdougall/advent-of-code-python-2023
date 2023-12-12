from argparse import ArgumentParser
import logging
import os


# logging.basicConfig(filename="log.txt", filemode="a", level=logging.INFO)
logging.basicConfig(level=logging.INFO)
RESOURCES = "res"


def args() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "-d", "--day",
        type=str,
        help="The day to run as a string.",
        required=True,
    )
    parser.add_argument(
        "-p", "--part",
        type=str,
        help="The part to run.",
    )
    parser.add_argument(
        "-r", "--runtime",
        type=str,
        help="The execution type.",
        choices=["test", "main"],
        default="main",
    )
    parser.add_argument(
        "--debug",
        help="Run in debug mode.",
        action="store_const",
        const="DEBUG",
    )
    parser.add_argument(
        "-i", "--data-import",
        help="Run in debug mode.",
        default="get_string_data",
        type=str,
    )
    return parser.parse_args()



if __name__ == "__main__":
    args = args()
    os.environ["RUNTIME"] = args.runtime
    os.environ["DAY"] = args.day
    os.environ["PART"] = args.part or ""
    os.environ["DATA_IMPORT"] = args.data_import
    os.environ["DEBUG"] = args.debug or ""

    from run import run_day
    run_day()
