from time import sleep
from threading import Thread


class Progress:
    def __init__(self):
        self.status = 0

    def start(self, title: str):
        print(title + ": [" + "-" * 40 + "]" + chr(8) * 41, flush=True, end="")
        self.status = 0

    def percentage(self, total: int, current: int) -> float:
        return (100 * current) / total

    def progress(self, total: int, current: int):
        quantity = self.percentage(total, current)
        x = int(quantity * 40 // 100)
        print("#" * (x - self.status), flush=True, end="")
        self.status = x

    def end(self):
        print("#" * (40 - self.status) + "]", flush=True)
        self.status = 0


class IndefiniteLoadingBar:
    def __init__(self):
        self.bar_size = 40
        self.direction = 1
        self.actual_position = 0
        self.finish = False
        self.thread = None

    def __print(self, *args, **kwargs):
        print(*args, **kwargs, flush=True, end="")

    def progress(self):
        self.__print("\r")
        spaces = (self.bar_size - self.actual_position)
        bar = f"[{'-' * self.actual_position}#{'-' * spaces}]"
        self.__print(bar)
        self.actual_position += self.direction
        if self.actual_position >= self.bar_size or self.actual_position <= 0:
            self.direction *= -1

    def inifite(self):
        while not self.finish:
            self.progress()
            sleep(0.1)

    def start(self):
        self.thread = Thread(target=self.inifite, name="IProgressBarThread")
        self.thread.start()
    
    def end(self):
        self.finish = True
        self.thread.join()
        self.thread = None
        print()

    
        
