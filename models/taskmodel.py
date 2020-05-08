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

    def create(self, txt):
        self.tasks.append(txt)

    def save_tasks(self):
        text = '\n'.join(self.tasks)
        self.task_file.write_text(text)

    def task_switch_mark_done(self, index):
        mark_postion = 3
        task = self.tasks[index]
        new_mark = 'X' if task[mark_postion] == ' ' else ' '
        new_task = task[:mark_postion] + new_mark + task[mark_postion + 1:]
        self.tasks[index] = new_task
