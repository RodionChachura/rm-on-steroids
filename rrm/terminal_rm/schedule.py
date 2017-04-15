import getpass

from crontab import CronTab

from ..config.config import CRON_COMMENT, CRON_COMMAND


def setup_clear_schedule(execute):
    username = getpass.getuser()
    cron = CronTab(user=username)
    job = next((c for c in cron.crons if c.comment == CRON_COMMENT), None)
    if execute == 'never' and job:
        cron.remove(job)
    else:
        if not job:
            job = cron.new(command=CRON_COMMAND, comment=CRON_COMMENT)
        if execute == 'minute':
            job.every().minute()
        elif execute == 'hour':
            job.every().hour()
        elif execute == 'day':
            job.every().dom()
        elif execute == 'month':
            job.every().month()

    cron.write()