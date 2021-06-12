import os
import sys
import re

replace_block = "████"


def main():
    # Read the input
    if len(sys.argv) <= 2:
        usage()
        sys.exit(1)

    target_dir = sys.argv[1]
    secret_words = sys.argv[2:]

    # If the input is just a file, only work on it
    if os.path.isfile(target_dir):
        redact_file(target_dir, secret_words)
        sys.exit(0)

    # If the input is a directory work recursivly on all files in the folder
    for root, dirs, files in os.walk(target_dir):
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            redact_file(os.path.join(root, file), secret_words)


def redact_file(file_name, words):
    try:
        file = open(file_name, "r")
        data = file.read()
        file.close()
    except OSError as e:
        print(
            f'Unable to read file "{file_name}": {e.strerror}. (continuing with next file)'
        )
        return
    except UnicodeDecodeError as e:
        print(
            f'Unable to read file "{file_name}": {e.reason}. (continuing with next file)'
        )
        return

    # Step one relplace all words
    for word in words:
        replace = re.compile(re.escape(word), re.IGNORECASE)
        data = replace.sub(replace_block, data)

    # Step two merge nearby blocks
    replace = re.compile(
        f"{replace_block}(\\s*{replace_block})+", re.IGNORECASE
    )
    data = replace.sub(replace_block, data)

    try:
        file = open(file_name, "w")
        file.write(data)
        file.close()
    except OSError as e:
        print(
            f'Unable to read file "{file_name}": {e.strerror}. (continuing with next file)'
        )
        return


def usage():
    print(f"""Usage: {sys.argv[0]} PATH [WORD...]""")


if __name__ == "__main__":
    main()