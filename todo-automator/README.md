# TODO-Automator

Import tasks into [Todoist](https://todoist.com/).

## Setup

1. [Install Python](https://www.python.org/downloads/)
2. Install the requirements `pip install todoist-python notion-client`

### Todoist Setup

1. Get yourself an API token [here](https://todoist.com/prefs/integrations)
2. Create a local file called `todoist-token.txt` and write your token to it.

## Usage

```
usage: main.py [-h] [--project PROJECT] [files ...]

positional arguments:
  files              Files with tasks to add (default: stdin)

options:
  -h, --help         show this help message and exit
  --project PROJECT  Project name to which the tasks will be added (default: University)
```

## Examples

```bash
echo "A new task: 04.03.2021" | python3 main.py
python3 main.py < WE.txt
```

The script reads the file each line of the input must be in the format `<taskname>: <deadline-date>`. The date can be either in the european format `DD.MM` or `DD.MM.YYYY`. All `.txt` files in this directory are examples.
