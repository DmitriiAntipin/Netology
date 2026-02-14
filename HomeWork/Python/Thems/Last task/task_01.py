from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

TASKS_FILE = "tasks.txt"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.load_tasks()
    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                self.tasks = json.load(file)
                if self.tasks:
                    self.next_id = max(task["id"] for task in self.tasks) + 1
    def save_tasks(self):
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=2)
    def create_task(self, title, priority):
        task = {
            "id": self.next_id,
            "title": title,
            "priority": priority,
            "isDone": False
        }
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task
    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["isDone"] = True
                self.save_tasks()
                return True
        return False

task_manager = TaskManager()


class TodoHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    def do_GET(self):
        if self.path == "/tasks":
            self.send_json(task_manager.tasks)
        else:
            self.send_error(404)
    def do_POST(self):
        if self.path == "/tasks":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            title = data.get("title")
            priority = data.get("priority")
            if not title or not priority:
                self.send_error(400)
                return
            task = task_manager.create_task(title, priority)
            self.send_json(task)
        elif self.path.startswith("/tasks/") and self.path.endswith("/complete"):
            try:
                task_id = int(self.path.split("/")[2])
            except (IndexError, ValueError):
                self.send_error(404)
                return
            if task_manager.complete_task(task_id):
                self.send_response(200)
                self.end_headers()
            else:
                self.send_error(404)
        else:
            self.send_error(404)

def run(server_class=HTTPServer, handler_class=TodoHandler):
    server_address = ("", 8000)
    httpd = server_class(server_address, handler_class)
    print("Server started on port 8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
