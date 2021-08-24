from datetime import datetime
from todoist import TodoistAPI
from notion_client import Client as NotionClient
from typing import List
import sys
import argparse

DEFAULT_PROJECT = "University"
BACKENDS = ["todoist", "notion"]
DEFAULT_BACKEND = "notion"


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
    api.sync()

    # Find the uni project or create it
    projects = api.state["projects"]
    projects = list(filter(lambda p: p["name"] == project_name, projects))
    if len(projects) != 0:
        project_id = projects[0]["id"]
    else:
        procject = api.projects.add(project_name)
        api.commit()
        project_id = procject["id"]

    # Add the tasks
    for task in tasks:
        api.items.add(
            task.text,
            project_id=project_id,
            due={"date": task.duedate.strftime("%Y-%m-%d")},
        )
        print(task)
    api.commit()


def add_tasks_notion(project_name: str, tasks: List[Task]):
    # Authenticate with the notion API
    notion = NotionClient(auth=open("notion_token.txt").read())

    # Find the database
    databases = notion.databases.list()["results"]
    databases = list(
        filter(
            lambda d: d["title"][0]["text"]["content"] == project_name,
            databases,
        )
    )

    # The database is no where to be found
    # tell the user to create it since notion bots are not allowed to create
    # top-level (workspace is parent) databases
    if databases == []:
        print(
            f"ERROR: No Notion Database with the name '{project_name}' is "
            "accessable by this script.\n"
            "To fix this issue do the folowing:\n"
            f"\t1) Create a new database and name it '{project_name}'.\n"
            f"\t2) Share the database with the integration this script "
            "uses.\n\n"
            "More infos at: "
            "https://developers.notion.com/docs"
            "#step-2-share-a-database-with-your-integration"
        )
        exit(1)

    # Multiple databases match the name so tell the user to delete one
    if len(databases) != 1:
        print(
            "ERROR: There are multiple Notion Databases "
            f"called '{project_name}'.\n"
            "This script can impossible know which one is the correct one so "
            "please delete one."
        )
        exit(1)

    database = databases[0]

    # Check if the database has all the required properties (just checking the
    # names and not the types)
    if sorted(database["properties"].keys()) != ["Done", "Duedate", "Name"]:
        # Delete all the properties
        properties = dict()
        for key in database["properties"].keys():
            if key in ["Done", "Duedate", "Name"]:
                continue
            properties[key] = None
        database = notion.databases.update(
            database["id"], properties=properties
        )

        # Add the correct properties
        properties = {
            "Done": {
                "checkbox": {},
            },
            "Duedate": {
                "date": {},
            },
            "Name": {
                "title": {},
            },
        }
        database = notion.databases.update(
            database["id"], properties=properties
        )

        # TODO: If the API allows it in the future, this should be automated
        print(
            "Hey, I just added some missing properties to your database.\n"
            "However, there are some things I cannot do, "
            "so please do the following:\n"
            "\t1) Add a filter to only show not completed tasks\n"
            "\t2) Sort the tasks by duedate\n"
            "\tThat's all 🎉\n"
        )

    # Add the tasks
    for task in tasks:
        page = {
            "Done": {
                "checkbox": False,
            },
            "Duedate": {
                "date": {
                    "start": task.duedate.strftime("%Y-%m-%d"),
                    "end": None,
                },
            },
            "Name": {
                "title": [
                    {"text": {"content": task.text}},
                ],
            },
        }
        notion.pages.create(
            parent={"database_id": database["id"]}, properties=page
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
            raise RuntimeError(
                f'Parsing Error: line "{line}" has no doublepoint!'
            )

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
                raise RuntimeError(
                    f'Parsing Error: "{parts[1]}" is not a valid date!'
                )

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
        "--backend",
        type=str,
        choices=BACKENDS,
        default=DEFAULT_BACKEND,
        help=f"The backend to be used (default: {DEFAULT_BACKEND})",
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
    if args.backend == "todoist":
        add_tasks_todoist(args.project, tasks)
    elif args.backend == "notion":
        add_tasks_notion(args.project, tasks)
    else:
        raise RuntimeError(f"Unknown backend '{args.backend}'")


if __name__ == "__main__":
    main()
