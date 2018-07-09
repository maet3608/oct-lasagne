"""
Timer to measure time taken for annotating a scan.
"""

from datetime import datetime, timedelta
from threading import Thread, Event


class AnnotationTimer(Thread):
    def __init__(self, f_display, f_stop):
        """
        Constructor
        :param function f_display: Function that takes duration in float seconds
               and is called every 0.5 sec provided is_timing == True.
               Typically used to update the display.
        :param function f_stop: Function that takes duration in seconds
               and is called when the timing is stopped .
        """
        Thread.__init__(self)
        self.event = Event()
        self.f_display = f_display
        self.f_stop = f_stop
        self.reset_timing(do_callback=False)
        self.start()  # start thread

    def get_duration(self):
        """Return absolute measured duration as float seconds"""
        return self.tdelta.total_seconds()

    def _curr_diff(self):
        """Return current time difference as timedelta"""
        return datetime.now() - self.starttime

    def reset_timing(self, do_callback=True, seconds=0.0):
        """Reset the timer to the given float seconds"""
        self.is_timing = False
        self.starttime = None
        self.tdelta = timedelta(seconds=seconds)
        if do_callback:
            self.f_display(self.tdelta.total_seconds())

    def toggle_timing(self):
        """Start or stop timer"""
        if self.is_timing:
            self.stop_timing()
        else:
            self.start_timing()

    def stop_timing(self):
        """Stop timer"""
        if self.starttime is not None and self.is_timing:
            self.is_timing = False
            self.tdelta += self._curr_diff()
            self.f_stop(self.tdelta.total_seconds())

    def start_timing(self):
        """Start timer"""
        self.starttime = datetime.now()
        self.is_timing = True

    def run(self):
        """Main loop of thread"""
        while not self.event.wait(0.5):  # every 0.5 sec
            if self.is_timing:
                td = self.tdelta + self._curr_diff()
                self.f_display(td.total_seconds())
