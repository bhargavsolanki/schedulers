from typing import List, Dict
import operator
from collections import deque
from itertools import cycle
from random import randrange


class Customer:
    _id: str
    taskMinSeconds: int
    taskMaxSeconds: int

    def __init__(self, id, min_time, max_time):
        self._id = id
        self.taskMinSeconds = min_time
        self.taskMaxSeconds = max_time

    def __repr__(self):
        return "id: " + self._id + ", min: " + \
               str(self.taskMinSeconds) + ", max: " + \
               str(self.taskMaxSeconds)


class Task:
    _id: str
    customer: Customer
    insertedTime: int
    burst_time: int = 0

    def __init__(self, id, cust, in_time):
        self._id = id
        self.customer = cust
        self.insertedTime = in_time

    def gen_burst_time(self):
        # Defining burst time to be inclusive of
        # minSeconds and MaxSeconds
        self.burst_time = randrange(self.customer.taskMinSeconds,
                                    self.customer.taskMaxSeconds + 1)

    def __repr__(self):
        return "Task is --> id: " + self._id + \
               ", customer: " + str(self.customer) + \
               ", inserttime: " + str(self.insertedTime) + \
               ", burst_time" + str(self.burst_time)


class FIFOScheduler:
    to_do: deque
    total_time: int
    max_workers: int = 1

    def __init__(self, todo_items: List,
                 total_time: int, max_workers: int):
        # Storing as a queue after sorting on insert time
        self.to_do = deque(sorted(todo_items, key=operator.attrgetter('insertedTime')))
        self.total_time = total_time
        self.max_workers = max_workers

    def start_scheduler(self):
        end_times = {}
        for i in range(0, self.max_workers):
            if self.to_do:
                task = self.to_do.popleft()
                task.gen_burst_time()
                if not end_times.get(task.burst_time):
                    end_times[task.burst_time] = [task]
                else:
                    end_times[task.burst_time].append(task)
        print("Processing 0th Second")
        print(str(end_times))

        for i in range(1, self.total_time):
            remove_items = []
            if end_times.get(i):
                remove_items = end_times.get(i)
                del end_times[i]
                for rem in remove_items:
                    rem.insertedTime = i
                    self.to_do.append(rem)

            for j in range(0, len(remove_items)):
                if self.to_do:
                    task = self.to_do.popleft()
                    task.gen_burst_time()
                    if not end_times.get(task.burst_time + i):
                        end_times[task.burst_time+ i] = [task]
                    else:
                        end_times[task.burst_time + i].append(task)
            print(f"Processing {i}th Second" )
            print(str(end_times))


class RoundRobinScheduler:
    total_time: int
    max_workers: int = 1
    to_do: Dict = {}

    def __init__(self, todo_items: List,
                 total_time: int, max_workers: int):
        # Storing as a queue after sorting on insert time
        self.total_time = total_time
        self.max_workers = max_workers
        self.to_do = {}
        tasks = deque(sorted(todo_items, key=operator.attrgetter('insertedTime')))
        for task in tasks:
            if not self.to_do.get(task.customer._id):
                self.to_do[task.customer._id] = deque([task])
            else:
                self.to_do[task.customer._id].append(task)

    def start_scheduler(self):
        end_times = {}
        round_robin = cycle(list(self.to_do.keys()))
        for i in range(0, self.max_workers):
            cust_id = round_robin.__next__()
            if self.to_do.get(cust_id):
                task = self.to_do[cust_id].popleft()
                task.gen_burst_time()
                if not end_times.get(task.burst_time):
                    end_times[task.burst_time] = [task]
                else:
                    end_times[task.burst_time].append(task)
        print("Processing 0th Second")
        print(str(end_times))
        for i in range(1, self.total_time):
            remove_items = []
            if end_times.get(i):
                remove_items = end_times.get(i)
                del end_times[i]
                for rem in remove_items:
                    rem.insertedTime =  i
                    self.to_do[rem.customer._id].append(rem)
            cust_id = round_robin.__next__()
            for j in range(0, len(remove_items)):
                if self.to_do.get(cust_id):
                    task = self.to_do[cust_id].popleft()
                    task.gen_burst_time()
                    if not end_times.get(task.burst_time + i):
                        end_times[task.burst_time+ i] = [task]
                    else:
                        end_times[task.burst_time + i].append(task)
                cust_id = round_robin.__next__()
            print(f"Processing {i}th Second" )
            print(str(end_times))


class BalancedRoundRobinScheduler:
    total_time: int
    max_workers: int = 1
    to_do: Dict = {}

    def __init__(self, todo_items: List,
                 total_time: int, max_workers: int):
        # Storing as a queue after sorting on insert time
        self.total_time = total_time
        self.max_workers = max_workers
        self.to_do = {}
        tasks = deque(sorted(todo_items, key=operator.attrgetter('insertedTime')))
        for task in tasks:
            if not self.to_do.get(task.customer._id):
                self.to_do[task.customer._id] = deque([task])
            else:
                self.to_do[task.customer._id].append(task)

    def start_scheduler(self):
        end_times = {}
        processing = 0
        round_robin = cycle(list(self.to_do.keys()))
        for i in range(0, self.max_workers):
            cust_id = round_robin.__next__()
            if self.to_do.get(cust_id):

                task = self.to_do[cust_id].popleft()
                task.gen_burst_time()
                if not end_times.get(task.burst_time):
                    end_times[task.burst_time] = [task]
                else:
                    end_times[task.burst_time].append(task)
                processing = processing + 1
        print("Processing 0th Second")
        print(str(end_times))
        for i in range(1, self.total_time):
            remove_items = []
            if end_times.get(i):
                remove_items = end_times.get(i)
                del end_times[i]
                for rem in remove_items:
                    rem.insertedTime =  i
                    self.to_do[rem.customer._id].append(rem)

            for rem in remove_items:
                cust_id = rem.customer._id
                if self.to_do.get(cust_id):
                    task = self.to_do[cust_id].popleft()
                    task.gen_burst_time()
                    if not end_times.get(task.burst_time + i):
                        end_times[task.burst_time+ i] = [task]
                    else:
                        end_times[task.burst_time + i].append(task)
                processing = processing + 1
                cust_id = round_robin.__next__()
            print(f"Processing {i}th Second" )
            print(str(end_times))
