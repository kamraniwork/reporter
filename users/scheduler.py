import math
from datetime import datetime
from celery import schedules
from celery.beat import Scheduler, ScheduleEntry
from celery.task import PeriodicTask


class ModelEntry(ScheduleEntry):
    def is_due(self):
        if self.start_date is not None and self.now() < self.start_date:
            delay = math.ceil(
                (self.model.start_time - datetime.now()).total_seconds()
            )
            return schedules.schedstate(False, delay)  # try again in 20 seconds
        return schedules.schedstate(False, 100000)


class DatabaseScheduler(Scheduler):
    """Database-backed Beat Scheduler."""

    Entry = ModelEntry
    Model = PeriodicTask

# class myschedule(schedule):
#
#     def __init__(self, *args, **kwargs):
#         super(myschedule, self).__init__(*args, **kwargs)
#         self.start_date = kwargs.get('start_date', None)
#
#     def is_due(self, last_run_at):
#         if self.start_date is not None and self.now() < self.start_date:
#             return (False, 20)  # try again in 20 seconds
#         return super(myschedule, self).is_due(last_run_at)
#
#     def __reduce__(self):
#         return self.__class__, (self.run_every, self.relative, self.nowfun, self.start_date)