import os
import unittest

from solve_me import TasksCommand


def reset_files():
    try:
        os.remove(TasksCommand.TASKS_FILE)
    except OSError:
        pass
    try:
        os.remove(TasksCommand.COMPLETED_TASKS_FILE)
    except OSError:
        pass


def load_tasks_file():
    current_items = {}
    try:
        file = open(TasksCommand.TASKS_FILE, "r")
        for line in file.readlines():
            item = line[:-1].split(" ")
            current_items[int(item[0])] = " ".join(item[1:])
        file.close()
    except Exception:
        pass
    return current_items


def load_completed_file():
    tasks = []
    try:
        file = open(TasksCommand.COMPLETED_TASKS_FILE, "r")
        tasks = [i[:-1] for i in file.readlines()]
        file.close()
    except Exception:
        pass
    return tasks


class SimpleTest(unittest.TestCase):
    def setUp(self):
        reset_files()
        self.command_object = TasksCommand()

    def test_add_tasks(self):
        self.command_object.add(["5", "Test Task 5"])
        tasks = load_tasks_file()
        self.assertEqual(tasks[5], "Test Task 5")

    def test_add_same_tasks(self):
        self.command_object.add(["2", "Task 3"])
        self.command_object.add(["2", "Task 2"])
        tasks = load_tasks_file()
        self.assertEqual(tasks[3], "Task 3")

    def test_add_complete_tasks(self):
        self.command_object.add(["10", "Task 10"])
        self.command_object.done(["10"])
        tasks = load_tasks_file()
        self.assertFalse("10" in tasks)
        completed = load_completed_file()
        self.assertTrue("Task 10" in completed)

    def test_delete_tasks(self):
        self.command_object.add(["15", "Task 15"])
        self.command_object.delete(["15"])
        tasks = load_tasks_file()
        self.assertFalse("15" in tasks)
        completed = load_completed_file()
        self.assertFalse("Task 15" in completed)


unittest.main()
