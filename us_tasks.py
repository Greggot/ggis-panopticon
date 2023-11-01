
class US_tasks:
    def __init__(self, us, tasklist):
        self.us = us.strip()
        self.tasklist = tasklist

    def __str__(self):
        return self.us + ': ' + str(self.tasklist)
    
    @property
    def story(self):
        return self.us
    
    @property
    def tasks(self):
        return self.tasklist

def parse_tasks_file(path: str) -> list:
    file1 = open(path,  encoding='utf-8', mode='r')
    Lines = file1.readlines()
    
    tasks = []
    tasklist = []
    story = ''
    
    for line in Lines:
        if line[0] != '\t':
            if tasklist:
                tasks.append(US_tasks(story, tasklist.copy()))
                tasklist.clear()
            story = line
        else:
            tasklist.append(line.strip())

    tasks.append(US_tasks(story, tasklist))
    return tasks