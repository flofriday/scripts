import argparse
import shutil
import subprocess
import os


def get_lang(ext):
    mapping = {
        "c": "c",
        "cpp": "c++",
        "cs": "c#",
        "cxx": "c++",
        "ex": "elixir",
        "exs": "elixir",
        "h": "c",
        "hpp": "c++",
        "hs": "haskell",
        "hxx": "c++",
        "js": "javascript",
        "kt": "kotlin",
        "md": "markdown",
        "ps": "powershell",
        "py": "python",
        "rb": "ruby",
        "rb": "ruby",
        "rs": "rust",
        "ts": "typescript",
        "txt": "",
    }

    if ext in mapping:
        return mapping[ext]

    # Assume that the file extension is the full name of the language
    # (like in java, go, xml, json and many more).
    return ext


def main():
    parser = argparse.ArgumentParser(description="Bring code to paper.")
    parser.add_argument(
        "files", type=str, nargs="+", help="Paths of the files to include"
    )
    parser.add_argument(
        "--out",
        default="code.pdf",
        help="File to write the output to.",
    )
    parser.add_argument(
        "--title",
        default="code.pdf",
        help="Title of the document.",
    )

    args = parser.parse_args()
    files = args.files
    title = args.title
    out = args.out

    # Pandoc has to be installed
    if not shutil.which("pandoc"):
        print(
            "ERROR: pandoc has to be installed (maybe it is but it is not in the path)\n"
            "You can download it here: https://pandoc.org/installing.html"
        )
        exit(1)

    # All files have to exist
    if not all(map(lambda f: os.path.isfile(f), files)):
        missing = ", ".join(filter(lambda f: not os.path.isfile(f)))
        print(f"ERROR: These file(s) do not exist: {missing}")
        exit(1)

    # Create a markdown
    markdown = f"""# {title}"""

    for file in files:
        markdown += f"## {file}\n"
        ext = file.split(".")[-1]
        lang = get_lang(ext)
        markdown += f"````{lang}\n"
        markdown += open(file).read()
        markdown += "\n"
        markdown += "````\n"

    # Pipe the markdown to pandoc
    pandoc = subprocess.run(
        [
            "pandoc",
            "--from",
            "gfm",
            "--to",
            "pdf",
            "--output",
            out,
        ],
        # shell=True,
        input=markdown,
        capture_output=True,
        text=True,
    )

    if pandoc.returncode != 0:
        print(
            f"ERROR: '{' '.join(pandoc.args)}' failed with error code {pandoc.returncode}\n"
            "Visit this for more information: https://pandoc.org/MANUAL.html#exit-codes\n"
            "Pandocs error: ",
            pandoc.stderr,
        )
        exit(1)


if __name__ == "__main__":
    main()
