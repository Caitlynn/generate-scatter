import multiprocessing
import threading
import fileinput
import queue
import time


def file_len(fname):
    try:
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    except Exception as e:
        print(fname)
        print(str(e))
        return 0


def count_total_file_lines(*files):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    counts = pool.map(file_len, files)
    return sum(counts)


class LineReader():
    def __init__(self, *files):
        self.files = files
        self.memory_limit = 8 * 1024**3
        self.started = False
        self.reader_thread = threading.Thread(target=self.read_lines)
        self.line_queue = queue.Queue()
        self.finished = False

    def lines(self):
        if not self.started:
            self.started = True
            self.reader_thread.start()
        while not self.finished:
            line = self.line_queue.get(timeout=100)
            yield line

    def read_lines(self):
        with fileinput.input(self.files) as line_iter:
            for line in line_iter:
                self.line_queue.put(line)
        self.finished = True  # race condition: if someone asks to get line between last put and this LOC.


def time_usage(func):
    def wrapper(*args, **kwargs):
        beg_ts = time.time()
        retval = func(*args, **kwargs)
        end_ts = time.time()
        print("elapsed time: %f" % (end_ts - beg_ts))
        return retval
    return wrapper


def chained_file_line_iterator(*files):
    with fileinput.input(files) as line_iter:
        for line in line_iter:
            yield line
