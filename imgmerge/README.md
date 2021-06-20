# imgmerge
A super simple script to merge 2 or more images side by side.

## Usage
```
usage: imgmerge.py [-h] [-v] [-o] file [file ...]

positional arguments:
  file             Image files to merge

optional arguments:
  -h, --help       show this help message and exit
  -v, --vertical   Merge the images vertically
  -o, --overwrite  Overwrite the first image and delete all others
```

The output image will be in the current working directory as `out.png`

## Example
```
python3 imgmerge.py gopher.png gopher_buisness.png
```