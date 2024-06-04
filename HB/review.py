# Review 1
def add_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list
'''
issue: don't set the defualt empty list variable,  it is the local variable in the function, each time call the function, 
will append value to the same local list variable.
should use None as the default value.
'''
# fix
def add_to_list(value, my_list=None):
    if my_list is None:
        my_list=[]
    my_list.append(value)
    return my_list



# Review 2
def format_greeting(name, age):
    return "Hello, my name is {name} and I am {age} years old."
'''
issue: should use f-strings to interpolate variable strings
'''
# fix
def format_greeting(name, age):
    return f"Hello, my name is {name} and I am {age} years old."



# Review 3
class Counter:
    count = 0

    def __init__(self):
        self.count += 1

    def get_count(self):
        return self.count

'''
issue: should use class variable instead of instance variable, 
otherwise only change the count of the counter instance other than the class count value.
'''
# fix
class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1

    def get_count(self):
        return Counter.count
    


# Review 4
import threading

class SafeCounter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

def worker(counter):
    for _ in range(1000):
        counter.increment()

counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()


'''
issue: multiple thread access and modify the same resouce at almost same time, it will casue the data race, 
likely get the inconsistent value,  should use thread-safe mechanism with lock.
'''
# fix
import threading

class SafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        self.count += 1

def worker(counter):
    for _ in range(1000):
        with counter.lock:
            counter.increment()

counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
print(counter.count)    



# Review 5
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] =+ 1
        else:
            counts[item] = 1
    return counts


'''
issue: use += instead of =+ for self increment 
'''
# fix
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts.keys():
            counts[item] += 1
        else:
            counts[item] = 1   
    return counts
 