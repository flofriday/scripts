# TODO-Automator

Import tasks into [todoist](https://todoist.com/)

## Setup

At the moment this scripts supports [Notion](https://www.notion.so/)
and [Todoist](https://todoist.com/) as backends, and their
setups are slightly different.

However there are some things you need to do either way:

1. [Install Python](https://www.python.org/downloads/)
2. Install the requirements `pip install todoist-python notion-client`

### Todoist Setup

1. Get yourself an API token [here](https://todoist.com/prefs/integrations)
2. Create a local file called `todoist-token.txt` and write your token to it.

### Notion Setup

1. Get yourself an API token [Guide](https://developers.notion.com/docs#step-1-create-an-integration).
2. Create a local file called `notion-token.txt` and write your token to it.
3. Create a new page, name it `University` (or anything else but you will need to
   set the `project` argument in the CLI).
4. The page must be a Table.
5. Share the page with the integration you created in step one.

## Usage

```
usage: main.py [-h] [--backend {todoist,notion}] [--project PROJECT]

optional arguments:
  -h, --help            show this help message and exit
  --backend {todoist,notion}
                        The backend to be used (default: notion)
  --project PROJECT     Project name to which the tasks will be added (default: University)
```

## Examples

```bash
echo "A new task: 04.03.2021" | python3 main.py
python3 main.py < WE.txt
```

The script reads from stdin and each line of the input must be in the format `<taskname>: <deadline-date>`. The date can be either in the european format `DD.MM` or `DD.MM.YYYY`.
