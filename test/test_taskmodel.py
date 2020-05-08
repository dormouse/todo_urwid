import pytest
from pathlib import Path
from models.taskmodel import TaskModel

TEST_DIR = Path(__file__).resolve().parent


def test_load_tasks():
    task_file = TEST_DIR / 'test_tasks.md'
    m = TaskModel(task_file)
    known_value = [
        '- [ ] 1st buy milk',
        '- [X] 2rd clean body',
        '- [ ] 3rd go to school',
        '- [ ] 一二三四五六七八九十一二三四五六七八九十'
        '一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十'
        '一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十'
        '一二三四五六七八九十'
    ]
    m.load_tasks()
    result = m.tasks
    assert result == known_value

if __name__ == '__main__':
    pytest.main(["-vv",])
