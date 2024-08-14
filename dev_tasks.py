from typing import List, Iterable

class Dev_tasks:
    def __init__(self, a_story: str, tasklist: List[str]):
        self._story = a_story.strip()
        self.tasklist = tasklist

    def __str__(self):
        return self._story + ': ' + str(self.tasklist)
    
    @property
    def story(self):
        return self._story
    
    @property
    def tasks(self) -> Iterable[str]:
        return iter(self.tasklist)

""" Считать таски по формату: если первый символ строки не Tab, то считать это номером стори,
    иначе - записать текст в список задач под последней попавшейся истории.
"""
def parse_tasks_file(path: str) -> List[Dev_tasks]:
    file1 = open(path, encoding='utf-8', mode='r')
    Lines = file1.readlines()
    
    tasks = []
    tasklist = []
    story = ''
    
    for line in Lines:
        if line[0] in ' \t':
            tasklist.append(line.strip())
        else:
            if tasklist:
                tasks.append(Dev_tasks(story, tasklist))
                tasklist = []
            story = line

    tasks.append(Dev_tasks(story, tasklist))
    return tasks