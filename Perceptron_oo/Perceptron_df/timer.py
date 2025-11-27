import time

class Timer:
    '''
    inspiration of passed creation of Timer in class

    prints the elapsed time to fully execute a given function (or run)
    '''
    def __enter__(self):
        self.start = time.time()
        return self
    
    '''
    def __exit__ allows for the with() block to end and for the time to terminate

    exec_type, exec_val, exec_tb are required for the context manager

    python will throw a protocol error if not included - thus needed for compare.py
    
    see instance of with Timer() in compare.py

    '''
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        self.elapsed = end - self.start
        print(f"Elapsed time: {end - self.start} in seconds")
