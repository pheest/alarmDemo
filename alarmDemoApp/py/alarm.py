import devsup.ptable as PT
from devsup.ptable import _ONPROC
from devsup.hooks import addHook
from devsup import NO_ALARM, MINOR_ALARM, MAJOR_ALARM, INVALID_ALARM, COMM_ALARM, READ_ALARM, WRITE_ALARM
from devsup.db import getRecord
import signal
from threading import Thread, Event


class AlarmTest(PT.TableBase):
    # Out paramaneters
    out_pini_no = PT.Parameter()
    out_pini_yes = PT.Parameter()
    # Input parameters
    in_pini_no = PT.Parameter(iointr=True)
    in_pini_yes = PT.Parameter(iointr=True)

    def __init__(self, name):
        super().__init__(name=name)
        self.stop = False
        self.count = None
        self.onproc_event = Event()
        self.out_pini_no.addAction(self.proc_out_pini_no, _ONPROC)
        self.out_pini_yes.addAction(self.proc_out_pini_yes, _ONPROC)
        self.run_thread = Thread(target=self._run)

    def start(self):
        self.run_thread.start()

    def stop_threads(self):
        print("stopping threads")
        self.stop = True
        self.onproc_event.set()
        self.run_thread.join()

    def set_alarms(self, PV1, PV2):
        """
        This method sets the alarm status on two PVs in alternation.
        These two PVs would be either the inputs and driven from the _run thread,
        or output PVs and driven from the onproc method(s).
        """
        if self.count > 10:
            PV1.stat = READ_ALARM
            PV2.stat = WRITE_ALARM
            
        if self.count % 2:
            PV1.alarm = MAJOR_ALARM
            PV1.amsg = "odd number"
            PV2.alarm = NO_ALARM
            PV2.amsg = None
        else:
            PV1.alarm = NO_ALARM
            PV1.amsg = None
            PV2.alarm = MAJOR_ALARM
            PV2.amsg = "even number"
        
    def _run(self):
        while True:
            if self.onproc_event.wait():
                self.onproc_event.clear()
            if self.stop:
                break
            if self.count is None:
                continue
            self.in_pini_no.value = self.count
            self.in_pini_yes.value = self.count
            self.set_alarms(self.in_pini_no, self.in_pini_yes)
            self.in_pini_no.notify()
            self.in_pini_yes.notify()
            print("in_pini_no", self.in_pini_no.value)
            print("in_pini_yes", self.in_pini_yes.value)

    def proc_out_pini_no(self):
        """
        This method is called in response to timer scanning within the database scan.
        This drives the application timing.
        """
        if self.count is not None:
            self.onproc_event.set()

            out_pini_no = getRecord("OUT_PINI:NO")
            # This cannot work here to update alarm status.
            # If this call scanned the (own) record it would cause an infinite number of calls.
            out_pini_no.VAL = self.count
            out_pini_yes = getRecord("OUT_PINI:YES")
            # I believe this only works correctly for waveform records.
            # The record is scanned to update the scan status.
            out_pini_yes.VAL = [self.count]
            out_pini_yes.scan(sync=False, force=0)
            self.count += 1
        
    def proc_out_pini_yes(self):
        if self.count is None:
            if len(self.out_pini_yes.value) > 0:
                self.count = self.out_pini_yes.value[0]
        if self.count is not None:
            # This is in setting the alarm status on what is an output record.
            # This is - in effect - asyn:readback.
            self.set_alarms(self.out_pini_no, self.out_pini_yes)
            print("out_pini_yes", self.out_pini_yes.value)


def build():
    sup = AlarmTest(name="alarm")

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    addHook('AfterIocRunning', sup.start)
    addHook('AtIocExit', sup.stop_threads)

    return sup
