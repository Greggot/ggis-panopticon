from typing import List, Iterable

class dev_tasks:
    def __init__(self, us: str, tasklist: List[str]):
        self.us = us.strip()
        self.tasklist = tasklist

    def __str__(self):
        return self.us + ': ' + str(self.tasklist)
    
    @property
    def story(self):
        return self.us
    
    @property
    def tasks(self) -> Iterable[str]:
        return iter(self.tasklist)

def parse_tasks_file(path: str) -> Iterable[dev_tasks]:
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
                tasks.append(dev_tasks(story, tasklist.copy()))
                tasklist.clear()
            story = line

    tasks.append(dev_tasks(story, tasklist))
    return tasks