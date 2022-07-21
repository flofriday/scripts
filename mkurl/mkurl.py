import argparse
import sys
from urllib.parse import urlparse


def write_url(url, filename):
    content = f"[InternetShortcut]\nURL={url}"

    if filename is None:
        sys.stdout.write(content)
        return

    with open(filename, "w") as f:
        f.write(content)


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="URL to be saved")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="File to write the output to (default: stdout)",
    )
    args = parser.parse_args()
    url = args.URL
    filename = args.output

    # Parse url
    url_obj = urlparse(args.URL)
    if url_obj.scheme == "":
        url = "https://" + url

    elif url_obj.scheme == "http":
        print(
            "WARNING: HTTP is insecure, use HTTPS instead if possible!",
            file=sys.stderr,
        )

    # Verify filename
    if filename is not None and not filename.endswith(".url"):
        print(
            "WARNING: The outputfile should end with `.url` to indicate to "
            "the OS that this is a url file.",
            file=sys.stderr,
        )

    # Write the URL to the output file
    write_url(url, filename)


if __name__ == "__main__":
    main()
