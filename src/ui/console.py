"""Console User Interface for Pyndemic"""
from queue import Queue

from src.controller import MainController


class ConsoleUI:
    def __init__(self, controller=None):
        self.io = ConsoleIO()
        if controller is None:
            self.controller = MainController()
        else:
            self.controller = controller

        self.termination_step = None

    def run(self):
        self.termination_step = False
        with self.io, self.controller:
            while True:
                command = self.io.listen()
                if not command:
                    continue

                controller_response = self.controller.send(command)
                response = self.process_response(controller_response)
                self.io.send(response)

                if self.termination_step:
                    self.io.send('---<<< That\'s all! >>>---')
                    break

    def process_response(self, response):
        if response['type'] == 'termination':
            self.termination_step = True
        return response


class ConsoleIO:
    def __init__(self):
        self.requests = Queue()
        self.responses = Queue()

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def run(self):
        self._loop = self._async_loop()

    def stop(self):
        self.flush_output()

    def listen(self):
        request = self._loop.send(None)
        return request

    def send(self, response):
        self.responses.put(response)

    def _async_loop(self):
        while True:
            self.flush_output()
            self.check_input()

            if not self.requests.empty():
                yield self.requests.get()

    def check_input(self):
        command = input()
        if command:
            self.requests.put(command)

    def flush_output(self):
        while not self.responses.empty():
            response = self.responses.get()
            print(response, flush=True)
