import functools
import tracemalloc
from queue import Queue, Empty
from threading import Thread
from time import sleep
import _thread

class MemoryUsageExceeded(Exception):
    pass

def __memory_monitor(command_queue: Queue, poll_interval=1, memory_limit=512):
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    
    while True:
        try:
            command_queue.get(timeout=poll_interval)
            return
        except Empty:
            snapshot2 = tracemalloc.take_snapshot()
            top_stats = snapshot2.compare_to(snapshot1, 'lineno')
            total = sum(stat.size for stat in top_stats) / (1024 * 1024) # bytes to mb
            print(total)
            if total > memory_limit:
                command_queue.put(total)
                return _thread.interrupt_main()

def LimitMemory(mem_limit, poll_interval = 1):
    def limit_memory(func):
        @functools.wraps(func)
        def limiter(*args, **kwargs):
            queue = Queue()
            exception = False
            monitor_thread = Thread(target=__memory_monitor, args=(queue, poll_interval, mem_limit))
            monitor_thread.start()
            try:
                val = func(*args, **kwargs)
                return val
            except KeyboardInterrupt:
                exception = True
            finally:
                queue.put('stop')
                monitor_thread.join()
            if exception: raise MemoryUsageExceeded('Your limit was {} mb, but the function consumed {} mb memory'.format(mem_limit, queue.get()))
        return limiter
    return limit_memory
