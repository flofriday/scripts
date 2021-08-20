import argparse
import sys
import os
from PIL import Image
from functools import reduce


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="+", help="Image files to merge")
    parser.add_argument(
        "-v",
        "--vertical",
        help="Merge the images vertically",
        action="store_true",
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        help="Overwrite the first image and delete all others",
        action="store_true",
    )
    args = parser.parse_args()

    if len(args.file) == 1:
        print(
            "Cannot merge an image with itself. Provide at least two images."
        )
        sys.exit(1)

    # Open the input files
    filenames = args.file
    images = list(map(lambda f: Image.open(f), filenames))
    print(images)
    heights = list(map(lambda i: i.height, images))
    widths = list(map(lambda i: i.width, images))

    # Merge the images
    if args.vertical:
        width = max(widths)
        height = sum(heights)
    else:
        width = sum(widths)
        height = max(heights)

    result = Image.new("RGBA", (width, height), color="#000000FF")

    x, y = 0, 0
    for img in images:
        result.paste(img, (x, y))

        if not args.vertical:
            x += img.width
        else:
            y += img.height

        img.close()

    # Save the image
    if args.overwrite:
        for file in filenames[1:]:
            os.remove(file)
        result.save(filenames[0])

    else:
        result.save("out.png")


if __name__ == "__main__":
    main()
