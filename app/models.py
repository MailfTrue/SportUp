from django.db import models


class BotUser(models.Model):
    chat_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=255, default='main')

    def __str__(self):
        return f"{self.name} ({self.chat_id})"

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class Game(models.Model):
    chat_id = models.CharField(max_length=64, editable=False)
    creator = models.ForeignKey('BotUser', on_delete=models.SET_NULL, null=True)
    title = models.CharField('Название игры', max_length=32)
    address_text = models.TextField('Адрес')
    address_location = models.TextField('Адрес')
    date = models.DateField('Дата игры')
    start_time = models.TimeField('Время начала игры')
    end_time = models.TimeField('Время окончания игры')
    members_count = models.PositiveSmallIntegerField('Кол-во участников')
    team_count = models.PositiveSmallIntegerField('Кол-во команд')
    rent_price = models.PositiveIntegerField('Стоимость аренды поля')
    mvp = models.ForeignKey('GameMember', on_delete=models.CASCADE, verbose_name='Лучший игрок матча',
                            null=True, blank=True, related_name='game_mvp')
    voting_started = models.BooleanField('Голосование начато', default=False)
    voting_finished = models.BooleanField('Голосование окончено', default=False)

    @property
    def members(self):
        return GameMember.objects.filter(game=self).order_by('id')

    def __str__(self):
        return f"Игра {self.title}"

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class GameMember(models.Model):
    user = models.ForeignKey('BotUser', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    guest_name = models.CharField('Имя гостя', max_length=32, null=True, blank=True)
    guest_inviter = models.ForeignKey('BotUser', null=True, blank=True, related_name='inviter',
                                      on_delete=models.SET_NULL, verbose_name='Кто пригласил гостя')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='Игра')

    def __str__(self):
        return f"Участник {self.user.name} в игре {self.game}"

    class Meta:
        verbose_name = 'Участник игры'
        verbose_name_plural = 'Участники игры'


class Vote(models.Model):
    owner = models.ForeignKey('GameMember', on_delete=models.CASCADE, verbose_name='Кто голосовал',
                              related_name='vote_owner')
    member = models.ForeignKey('GameMember', on_delete=models.CASCADE,
                               verbose_name='Участник, за которого проголосовали',
                               related_name='vote_member')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='Игра')

