from datetime import datetime
from computer import computer
from expRand import expRand
from queue import Queue
import threading

file = open("log.txt", 'w')

devices = Queue(maxsize=10)
for i in range(10):
    devices.put(computer(1*60))

tasks = Queue()
tasksTime = Queue()
life = 5*60 # hrs

lock = threading.Lock()

delay = datetime.now()
delay -= delay
length = 0
count = 0
tasksCount = 0

def TaskProg():
    global life, tasks, length, tasksCount
    while life > 0:
        time = expRand(1/35) # Average inter-arrival time = 35 sec
        if(time > life): # if the interarival time will be after the contest ends
            life = 0
            break # end program
        with lock:
            file.write('time est to get task = ' + str(time) + '\n')
            file.flush()
        
        threading.Event().wait(time)
        task = expRand(1/42) # Average service time = 42 sec
        tasks.put(task)
        tasksTime.put(datetime.now())
        length += tasks.qsize()
        tasksCount += 1
        with lock:
            file.write('new task is inserted with time: ' + str(task) + ' queue lengh: ' + str(tasks.qsize()) + '\n')
            file.flush()
        life -= time


def ProcessProg(comp, task):
    global delay,count
    now = datetime.now()
    wait = now - tasksTime.get()
    delay += wait
    count += 1
    current_time = now.strftime("%H:%M:%S")
    with lock:
        file.write("computer took task that lasts " + str(task) + " secs, life: " + str(comp.life) + ' at ' + str(current_time) + ". waiting time: " + str(wait)[:7] + '\n')
        file.flush()
    threading.Event().wait(task)
    devices.put(comp)

    current_time = datetime.now().strftime("%H:%M:%S")
    with lock:
        file.write("computer fininshed task that lasts " + str(task) + " secs, life: " + str(comp.life) + ' at ' + str(current_time) + '\n')
        file.flush()

TaskThread = threading.Thread(target=TaskProg, name="Task Thread")

def MainProg():
    global tasks
    TaskThread.start()

    failed = 0
    while life or not tasks.empty():
        if not tasks.empty() and not devices.empty():
            comp = devices.get()
            task = tasks.queue[0]

            if comp.work(task):
                tasks.get()
                process = threading.Thread(target=ProcessProg, args=[comp, task], name="Processing Thread")
                process.start()
                failed = 0
            else:
                failed += 1
                devices.put(comp)
            
            # check if all computers failed to handle the task then skip it
            if failed == 10:
                tasks.get()
                tasksTime.get()
                with lock:
                    file.write('all computer cant run this task. time needed: ' + str(task) + '\n')
                    file.write('task discarded\n')
                    file.flush()
                failed = 0

file.write('simulation start\n')
file.write('log:\n')
MainThread = threading.Thread(target=MainProg, name="Main Thread")
MainThread.start()
MainThread.join()
with lock:
    file.write('\ncontest finished\n\n')
    file.flush()

# join all active threads (wait till all computers finished)
for thread in threading.enumerate():
    if thread is threading.current_thread():
        continue
    thread.join()

file.write('\n---------------------------- ANALYSIS ----------------------------\n\n')
file.write('average delay time = ' + str(delay/count)[:7] + '\n')
file.write('average queue length = ' + str(length/tasksCount)[:7] + '\n')
file.flush()

# Calculate the average delay time, waiting time, average queue length when you run your simulator for 5 hours.