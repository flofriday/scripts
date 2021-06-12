# Redact
Simple tool to replace names or sensitive data from text files.

## Usage
```
python3 redact.py PATH WORD...
```

The `PATH` can either be a single file or a directory which will be walked 
recursivly. And `WORD` is a list of words which will be replaced in the order
given.

Each word will be replaced with 4 Unicode. 
["Full-Block"](http://www.unicode-symbol.com/u/2588.html): ████

Also the words are case-insensitve and 

## Example
```
python3 redact.py /home/elon/ elon musk spaace-X tesla
```