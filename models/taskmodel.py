from pathlib import Path
from prj_conf import PRJ_DIR

class TaskModel(object):
    def __init__(self, task_file=None):
        if task_file is None:
            self.task_file = PRJ_DIR / 'tasks.md'
        else:
            self.task_file = Path(task_file)
        self.tasks = None

    def all(self):
        return self.tasks

    def load_tasks(self):
        text = self.task_file.read_text()
        self.tasks = list(filter(lambda x: x.strip(), text.split('\n')))
        print(self.tasks)

