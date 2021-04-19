from uvz.bot.bot import bot_run
from apscheduler.executors.base import MaxInstancesReachedError
from django.core.management.base import BaseCommand

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
class Command(BaseCommand):

    help = 'Runs the cronjobs'

    def handle(self, *args, **options):
        self._log_info("Configuring jobs")
        scheduler = BackgroundScheduler()
        scheduler.add_job(bot_run, "interval", seconds=10, jitter=10)
        try:
            self._log_info("Running scheduler")
            scheduler.start()
            self._log_info("Starting server")
            call_command("runserver")
        except KeyboardInterrupt:
            self._log_info("Stoping background job")
            scheduler.remove_all_jobs()
            return

    def _log_info(self, *msg):
        full_msg = ' '.join(msg)
        self.stdout.write(self.style.SUCCESS(full_msg))