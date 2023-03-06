from datetime import datetime
from todoist_api_python.api import TodoistAPI
from typing import List
import sys
import argparse

DEFAULT_PROJECT = "University"


class Task:
    def __init__(self, text: str, duedate: datetime):
        self.text = text
        self.duedate = duedate

    def __str__(self):
        return f"{self.text}: {self.duedate.strftime('%Y-%m-%d')}"


def add_tasks_todoist(project_name: str, tasks: List[Task]):
    # Authenticate with the todoist API
    api_token = open("todoist_token.txt").read()
    api = TodoistAPI(api_token)

    # Find the uni project or create it
    projects = api.get_projects()
    projects = list(filter(lambda p: p.name == project_name, projects))
    if len(projects) != 0:
        project_id = projects[0].id
    else:
        procject = api.add_project(name=project_name)
        project_id = procject.id

    # Add the tasks
    for task in tasks:
        api.add_task(
            content=task.text,
            project_id=project_id,
            due_date=task.duedate.strftime("%Y-%m-%d"),
        )
        print(task)


def parse_input(files: List[str]) -> List[Task]:

    # Read all from Stdin
    if files == []:
        lines = sys.stdin.readlines()

    # Read all files
    else:
        lines = []
        for file in files:
            with open(file) as f:
                lines.extend(f.readlines())

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
                date = datetime(date.year + 1, date.month, date.day)
        except Exception:
            try:
                date = datetime.strptime(parts[1], "%d.%m.%Y")
            except Exception:
                raise RuntimeError(f'Parsing Error: "{parts[1]}" is not a valid date!')

        # Add to the output
        output.append(Task(parts[0], date))

    return output


def main():
    # Parse the commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files",
        nargs="*",
        default=[],
        help="Files with tasks to add (default: stdin)",
    )
    parser.add_argument(
        "--project",
        type=str,
        default=DEFAULT_PROJECT,
        help="Project name to which the tasks will be added "
        f"(default: {DEFAULT_PROJECT})",
    )
    args = parser.parse_args()

    # Read the tasks from stdin
    tasks = parse_input(args.files)

    # Connect to the backend and upload the tasks
    add_tasks_todoist(args.project, tasks)


if __name__ == "__main__":
    main()
