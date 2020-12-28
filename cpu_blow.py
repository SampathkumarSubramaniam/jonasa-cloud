from multiprocessing import Pool
from multiprocessing import cpu_count
import signal
from time import sleep

stop_loop = 0


def exit_chld():
    global stop_loop
    stop_loop = 1
    sleep(10)


def f(x):
    global stop_loop
    count = 0
    while not stop_loop:
        x * x
        count += 1
        if count == 300:
            exit_chld()


def execute_cpu_blow():
    processes = cpu_count()
    print('-' * 20)
    print('Running load on CPU(s)')
    print('Utilizing %d cores' % processes)
    print('-' * 20)
    pool = Pool(processes)
    pool.map(f, range(processes))
