# Python-Memory-Limiter
Memory Limiter allows you to limit memory usage of a function.

## Usage
```
from collections import Counter

 # Limits memory usage to 1mb, if function uses more than that, it raises MemoryUsageExceeded exception
@LimitMemory(1)
def count_prefixes():
    sleep(2)  # Start up time.
    counts = Counter()
    fname = '/usr/share/dict/american-english'
    with open(fname) as words:
        words = list(words)
        for word in words:
            prefix = word[:3]
            counts[prefix] += 1
            sleep(0.0001)
    most_common = counts.most_common(3)
    sleep(3)  # Shut down time.
    return most_common

count_prefixes()
```
