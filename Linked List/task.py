import datetime

class Task:
    '''
    initialize the Class Task with the __init__ constructor
    '''
    def __init__(self, task_id, description, due_date, completed, priority=10):
        self.task_id = id
        self.description = description
        self.due_date = due_date
        self.completed = completed 
        self.priority = priority

    def __str__(self):
        '''
        __str__ prints the due date, description, priority, and completed date of the created task
        '''
        return f"[{self.due_date}] {self.description} | Priority: {self.priority} | Completed: {self.completed}"

    '''
    Python has a great module for handling dates and times

    The assignment asks to update priority if the due date is less than a week

    See update_priority for this reassignment of priorities 
    '''
    def update_priority(self):
        now = datetime.datetime.now()
        if (self.due_date - now).days <= 7:
            self.priority = 1