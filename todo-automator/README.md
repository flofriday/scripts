# TODO-Automator

Import tasks into todoist

## Setup

1. Get yourself an API token [here](https://todoist.com/prefs/integrations)
2. create a local file called `token.txt` and write your token to it.
3. Create in todoist a project called `Universität`. (You can also use another name but than you have to change the variable `PROJECT_NAME` in `main.py`)
4. Install the [todoist library](https://github.com/Doist/todoist-python) `pip install todoist-python`

## Usage

```bash
echo "A new task: 04.03.2021" | python3 main.py
python3 main.py < WE.txt
```

The script reads from stdin and each line of the input must be in the format `<taskname>: <deadline-date>`. The date can be either in the european format `DD.MM` or `DD.MM.YYYY`.
