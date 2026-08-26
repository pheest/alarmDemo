import devsup.ptable as PT
from devsup.hooks import addHook
from devsup import NO_ALARM, MINOR_ALARM, MAJOR_ALARM, INVALID_ALARM, COMM_ALARM, READ_ALARM
import signal
import time
from threading import Thread


class AlarmTest(PT.TableBase):
    pini_no = PT.Parameter(iointr=True)
    pini_yes = PT.Parameter(iointr=True)

    def __init__(self, name):
        super().__init__(name=name)
        self.stop = False
        self.run_thread = Thread(target=self._run)

    def start(self):
        self.run_thread.start()

    def stop_threads(self):
        print("stopping threads")
        self.stop = True
        self.run_thread.join()

    def _run(self):
        count = 0
        while not self.stop:
            self.pini_yes.value = count
            if count % 2:
                self.pini_yes.alarm = NO_ALARM
                self.pini_yes.amsg = None
            else:
                self.pini_yes.alarm = MAJOR_ALARM
                self.pini_yes.amsg = "odd number"

            self.pini_yes.notify()
            print(count)

            #self.pini_no.value = count
            #self.pini_no.notify()

            count += 1
            time.sleep(5)

def build():
    sup = AlarmTest(name="alarm")

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    addHook('AfterIocRunning', sup.start)
    addHook('AtIocExit', sup.stop_threads)

    return sup
