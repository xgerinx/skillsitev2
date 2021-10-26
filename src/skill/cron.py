from django_cron import CronJobBase, Schedule
import logging
logger = logging.getLogger(__name__)


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # 120 every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'skill.my_cron_job'

    def do(self):
        logger.error('Im cron')