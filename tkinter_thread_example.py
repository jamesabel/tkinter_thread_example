
# example tkinter window with a background thread
# author: James Abel
# see the LICENSE file for the license

import datetime
from tkinter import *
import threading


class Background(threading.Thread):
    def __init__(self, text_box):
        super().__init__()
        self._text_box = text_box
        self._exit_event = threading.Event()

    def run(self):
        while not self._exit_event.is_set():
            # display the time, updating once a second
            self._text_box.configure(text="the time is : %s" % datetime.datetime.now())
            self._exit_event.wait(1)  # wait 1 sec, or immediately exit if the exit_event gets set
        print('Background : run() exiting')

    def request_exit(self):
        print('Background : request_exit()')
        self._exit_event.set()


class ExampleTKApp(Tk):
    def __init__(self):
        super().__init__()

        # hook the 'X' button
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.title("tkinter_thread_example")
        self.geometry("400x200")

        # this is where we'll display something to show we're running
        self._text_box = Label(self, text="_")
        self._text_box.grid()

        self.background_task = Background(self._text_box)
        self.background_task.start()

    def on_exit(self):
        print('ExampleTKApp : on_exit() entry')
        self.background_task.request_exit()
        self.background_task.join()
        print('ExampleTKApp : on_exit() : calling self.destroy()')
        self.destroy()
        print('ExampleTKApp : on_exit() exit')


tk_app = ExampleTKApp()
tk_app.mainloop()

