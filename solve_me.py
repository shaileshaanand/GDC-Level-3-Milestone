from http.server import BaseHTTPRequestHandler, HTTPServer


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            lines = file.readlines()
            file.close()
            return lines
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def runserver(self):
        address = "127.0.0.1"
        port = 8000
        server_address = (address, port)
        httpd = HTTPServer(server_address, TasksServer)
        print(f"Started HTTP Server on http://{address}:{port}")
        httpd.serve_forever()

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "runserver":
            self.runserver()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics
$ python tasks.py runserver # Starts the tasks management server"""
        )

    def shift_items(self, priority):
        if priority + 1 in self.current_items:
            self.shift_items(priority + 1)
        self.current_items[priority + 1] = self.current_items[priority]

    def add(self, args):
        priority = int(args[0])
        task_text = args[1]
        self.read_current()
        if priority in self.current_items:
            self.shift_items(priority)
        self.current_items[priority] = task_text
        self.write_current()
        print(f'Added task: "{task_text}" with priority {priority}')

    def done(self, args):
        priority = int(args[0])
        self.read_current()
        if priority in self.current_items:
            self.completed_items.append(self.current_items[priority])
            del self.current_items[priority]
            self.write_current()
            self.write_completed()
            print(f"Marked item as done.")
        else:
            print(f"Error: no incomplete item with priority {priority} exists.")

    def delete(self, args):
        priority = int(args[0])
        self.read_current()
        if priority in self.current_items:
            del self.current_items[priority]
            self.write_current()
            print(f"Deleted item with priority {priority}")
        else:
            print(
                f"Error: item with priority {priority} does not exist. Nothing deleted."
            )

    def ls(self):
        self.read_current()
        for i, key in enumerate(sorted(self.current_items.keys()), 1):
            print(f"{i}. {self.current_items[key]} [{key}]")

    def report(self):
        print("Pending :", len(self.current_items))
        self.ls()
        print()
        print("Completed :", len(self.completed_items))
        for i, item in enumerate(self.completed_items, 1):
            print(f"{i}. {item}")

    def render_pending_tasks(self):
        self.read_current
        tasks = (
            "<h1> Completed</h1>\n<ul>\n"
            + "\n".join(
                [
                    f"<li>{self.current_items[priority]} [{priority}]</li>"
                    for priority in sorted(self.current_items.keys())
                ]
            )
            + "\n</ul>"
        )
        return tasks

    def render_completed_tasks(self):
        self.read_completed()
        tasks = (
            "<h1> Completed</h1>\n<ul>\n"
            + "\n".join([f"<li>{task}</li>" for task in self.completed_items])
            + "\n</ul>"
        )
        return tasks


class TasksServer(TasksCommand, BaseHTTPRequestHandler):
    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())
