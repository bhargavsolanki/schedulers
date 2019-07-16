# Schedulers

This task required to build different schedulers namely
1) FIFOScheduler
2) RoundRobinScheduler
3) BalancedRoundRobinScheduler

## Assumptions
a) Each iteration of the loop for each can be considered as 1 second. i.e the quantum
can be considered as 1.

b) The execution for a given list of todo tasks  will finish executing after 
TOTAL_TIME variable is entirely looped.

c) For the cases where Random values are generated, we could have used, SQLAlchemy,
a database, and read from the table.

d) We have managed to convert datetime string to datetime in epoch.

## Modifications in the input classes
a) Customer - no modifications

b) Task - Along with cust_id, a reference to the Customer object is also
a data member

## Environment and dependencies

This code is written in python 3.7 environment. No additional dependenices are
needed.


## Structure
### Models 
1) Task
2) Customer
3) FIFOScheduler
4) RoundRobinScheduler
5) BalancedRoundRobinScheduler

### Files
models.py - Contains all the classes

settings.py - Contains the environment constants that can be set

schedulers.py - this is the entry point/handler and also generates fake input
 

## How to run?
Load the project in pycharm, or run from Parent folder which is ~YOUR_PATH/schedulers
The file to run is schedulers.py 


