# time  "2018-03-14T15:48:14+0000"
# assuming that time is converted from string of time to
# timestamp using datetime strptime and epoch
from random import randrange, choice
from uuid import uuid4

from models import Task, Customer, FIFOScheduler,\
    RoundRobinScheduler, BalancedRoundRobinScheduler

from settings import TOTAL_CUSTOMERS,\
    TOTAL_TIME, TODO, TOTAL_TASKS, MAX_WORKERS

SCHEDULERS = {1: FIFOScheduler,
              2: RoundRobinScheduler,
              3: BalancedRoundRobinScheduler}

if __name__ == "__main__":
    # This assumes, the scheduler will run once every time unit
    # Start time of the system
    # Total number of time units the simulation should run.

    customers = []
    # This code generates various random numbers for the code to run.
    for i in range(0, TOTAL_CUSTOMERS):
        cust = Customer(id=str(uuid4()), min_time=randrange(1, 2),
                        max_time=randrange(2, 4))
        customers.append(cust)
    for i in range(0, TOTAL_TASKS):
        customer = choice(customers)
        task = Task(id=str(uuid4()), cust=customer, in_time=randrange(0, 3))
        TODO.append(task)
    print(' Tasks are loaded and ready to be executed.')
    print("Choose your scheduler \n1.FIFO\n2.Round Robin\n3.Balanced Round Robin")
    try:
        choice = int(input())
        if choice not in [1,2,3]:
            raise Exception("Invalid input")
        scheduler = SCHEDULERS[choice](todo_items=TODO,
                                       total_time=TOTAL_TIME,
                                       max_workers=MAX_WORKERS)
        scheduler.start_scheduler()

    except Exception as err:
        print("Please enter a valid input and run again")







