import datetime
from ToDoLinkedList import ToDoLinkedList
from task import Task 


def main():

    '''
    to_do_list is the object of ToDoLinkedList class required as mentioned in this portion of the assignment
    '''
    to_do_list = ToDoLinkedList()

    '''
    I've used a for loop to add nodes to the linked list for our test 

    Node class requires a due date, i've created a var with datetime.datetime module

    date is created (year, month, day, hour, minute)
    
    The range is 1,11 as python recognizes the last integer as n-1

    I remember this from previous iterations ^

    '''
    for i in range(1, 11):
        due_date = datetime.datetime(2025, 10, i+1, 12, 0) # influenced my Prof.Domino's example of datetime.datetime
        task = Task(
            task_id=i,
            description=f"{i}",
            due_date=due_date,
            completed=i % 2 == 1,
            priority=i
        )
        to_do_list.add_to_back(task)

    '''
    in order to test if the code works, we have to implement filter, conditional_str and change priority

    here is the filter and conditional_str tests

    the lambda will print True always, an easy way to test the whole linked list
    '''
    print("linked list:")
    print(to_do_list.conditional_str(lambda n: True))
    filtered = to_do_list.filter(lambda n: n.data.priority <= 8)
    if filtered:
        print(filtered.conditional_str(lambda n: True))
    

    '''
    created a lambda case for change_priority

    here is the test case for change_priority

    to make the linked list 
    '''
    to_do_list.change_priority(7)  
    print("Test for change_priority")
    if to_do_list.head:
        print(to_do_list.conditional_str(lambda n: n.data.completed))


if __name__ == "__main__":
    main()