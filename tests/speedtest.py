# nth fib. num

import time

str_time = time.time()

def fibonacci(num):
    if num == 0 or num == 1:
        return 1
    else:
        return fibonacci(num - 1) + fibonacci(num - 2)

print(fibonacci(100))

print(time.time() - str_time)