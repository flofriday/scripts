import os
import sys
import re
import argparse
from typing import List

replace_block = "████"


def main():
    # Read the input
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="file or directory to modify")
    parser.add_argument("word", nargs="+", help="words to replace")
    args = parser.parse_args()

    target = args.path
    secret_words = args.word

    if not os.path.exists(target):
        print(f"Unable to find the file or directory: {target}")
        sys.exit(1)

    # If the input is just a file, only work on it
    if os.path.isfile(target):
        redact_file(target, secret_words)
        sys.exit(0)

    # If the input is a directory work recursivly on all files in the folder
    for root, dirs, files in os.walk(target):
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            redact_file(os.path.join(root, file), secret_words)


def redact_file(file_name: str, words: List[str]):
    try:
        file = open(file_name, "r")
        data = file.read()
        file.close()
    except OSError as e:
        print(
            f'Unable to read file "{file_name}": {e.strerror}. '
            "(continuing with next file)"
        )
        return
    except UnicodeDecodeError as e:
        print(
            f'Unable to read file "{file_name}": {e.reason}. '
            "(continuing with next file)"
        )
        return

    # Step one relplace all words
    for word in words:
        replace = re.compile(re.escape(word), re.IGNORECASE)
        data = replace.sub(replace_block, data)

    # Step two merge nearby blocks
    replace = re.compile(f"{replace_block}(\\s*{replace_block})+", re.IGNORECASE)
    data = replace.sub(replace_block, data)

    try:
        file = open(file_name, "w")
        file.write(data)
        file.close()
    except OSError as e:
        print(
            f'Unable to write file "{file_name}": {e.strerror}. (continuing with next file)'
        )
        return


if __name__ == "__main__":
    main()
