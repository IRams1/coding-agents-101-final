from argparse import ArgumentParser
from src.file_handler import FileHandler
from src.parsers import (
    IRSParser
)

providers = {
    "IRS": IRSParser,
}


def main(provider, filename):
    provider_key = provider.upper()

    provider = providers[provider_key](
        file_handler=FileHandler(),
        filename=filename,
    )
    return provider.process_file()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-r", "--provider", required=True)
    parser.add_argument("-f", "--filename", required=True)

    args = parser.parse_args()
    main(
        args.provider,
        args.filename,
    )
