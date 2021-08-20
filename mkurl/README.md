# mklink

A simple commandline tool to create .url files.

I use a pretty well structured filesystem, to organize my university lecures,
homeworks, books and scripts. So the most obvious way to store relevant
websites is to store them as `.url` files on the same filesystem.

## Usage

```
usage: mkurl [-h] [-o OUTPUT] URL

positional arguments:
  URL                   URL to be saved

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        File to write the output to (default: stdout)
```

## Examples

```bash
# Both are equal
python3 mkurl.py github.com/flofriday/ > github.url
python3 mkurl.py -o github.url https://github.com/flofriday/
```
