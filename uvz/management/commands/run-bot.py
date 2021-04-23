from uvz.bot.bot import bot_run
from django.core.management.base import BaseCommand, CommandParser

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
class Command(BaseCommand):

    help = 'Runs the cronjobs'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-p", "--port", type=int, help="Port to run server on")
        parser.add_argument("-r", "--repeat", type=int, help="Time after which cron job repeats")
    def handle(self, *args, **options):
        self._log_info("Configuring jobs")
        scheduler = BackgroundScheduler()
        scheduler.add_job(bot_run, "interval", seconds=int(options.get("repeat") or "10"), jitter=10)
        port = options.get("port") or "8000"
        try:
            self._log_info("Running scheduler")
            scheduler.start()
            self._log_info("Starting server")
            call_command("runserver", f"0.0.0.0:{port}")
        except KeyboardInterrupt:
            self._log_info("Stoping background job")
            scheduler.remove_all_jobs()
            return

    def _log_info(self, *msg):
        full_msg = ' '.join(msg)
        self.stdout.write(self.style.SUCCESS(full_msg))