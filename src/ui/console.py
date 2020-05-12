"""Console User Interface for Pyndemic"""
import sys
from queue import Queue


class ConsoleUI:
    def __init__(self, controller):
        self.io = ConsoleIO()
        self.controller = controller

        self.termination_step = None

    def run(self):
        self.termination_step = False
        with self.io, self.controller:
            while True:
                self.io.send('Waiting for command...')
                try:
                    command = self.io.listen()
                except KeyboardInterrupt:
                    self.io.send('You decided to exit the game...')
                    command = 'quit'

                if not command:
                    continue

                controller_response = self.controller.send(command)
                response = self.process_response(controller_response)
                self.io.send(response)

                if self.termination_step:
                    self.io.send('Finishing program...')
                    break

    def process_response(self, response):
        if response['type'] == 'termination':
            self.termination_step = True
        return response


class ConsoleIO:
    def __init__(self):
        self.responses = Queue()

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def run(self):
        pass

    def stop(self):
        self.flush_output()

    def listen(self):
        request = sys.stdin.readline().rstrip()
        return request

    def send(self, response):
        self.responses.put(response)
        self.flush_output()

    def flush_output(self):
        while not self.responses.empty():
            response = self.responses.get()
            print(response, flush=True)
