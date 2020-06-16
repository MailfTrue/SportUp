from time import sleep
from .models import Game
from .wa_bot import start_voting
from django.utils import timezone
from datetime import timedelta


class Watcher:

    def __init__(self):
        self.run()

    def run(self):
        while True:
            now = timezone.localtime(timezone.now())
            for game in Game.objects.filter(date__lt=now.date(), end_time__lt=now.time(), voting_started=False):
                start_voting(game)
                game.voting_started = True
                game.save()

            vote_finishing_date = now - timedelta(hours=2)
            for game in Game.objects.filter(
                    date__lt=vote_finishing_date.date(),
                    end_time__lt=vote_finishing_date.time(),
                    voting_finished=False
            ):
                start_voting(game)
                game.voting_started = True
                game.save()
            sleep(60)
