from datetime import datetime
from todoist import TodoistAPI
from typing import List, Tuple
import sys

PROJECT_NAME = "Universität"


def add_task(api: TodoistAPI, project_id: int, text: str, duedate: datetime):
    task = api.items.add(
        text,
        project_id=project_id,
        due={"date": duedate.strftime("%Y-%m-%d")},
    )
    print(task)


def parse_stdin() -> List[Tuple[str, datetime]]:

    # Read all from Stdin
    lines = sys.stdin.readlines()
    output = []
    for line in lines:
        # Ignore empty lines
        if line.strip() == "":
            continue

        # Split the line at the :
        parts = list(map(lambda x: x.strip(), line.split(":")))
        if len(parts) != 2:
            raise RuntimeError(f'Parsing Error: line "{line}" has no doublepoint!')

        # Parse the date
        try:
            date = datetime.strptime(parts[1], "%d.%m")
            date = date.replace(datetime.now().year)
            if date < datetime.now():
                date.year = date.replace(datetime.now().year + 1)
        except Exception:
            try:
                date = datetime.strptime(parts[1], "%d.%m.%Y")
            except Exception:
                raise RuntimeError(f'Parsing Error: "{parts[1]}" is not a valid date!')

        # Add to the output
        output.append((parts[0], date))

    return output


def main():
    # Authenticate
    api_token = open("token.txt").read()
    api = TodoistAPI(api_token)
    api.sync()

    # Find the uni project
    for project in api.state["projects"]:
        if project["name"] != PROJECT_NAME:
            continue
        uni_project_id = project["id"]

    # Parse the input
    tasks = parse_stdin()

    # Add the tasks to todoist
    for task in tasks:
        text, date = task
        add_task(api, uni_project_id, text, date)

    api.commit()


if __name__ == "__main__":
    main()
