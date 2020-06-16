game_template = '''
{{ game.date }} {{ game.title }} {{ game.address_text }} \
{{ game.start_time }} — {{ game.end_time }} \
{{ game.members_count }} участников {{ game.team_count }} команды

Отпишитесь об участии в мероприятии
/in - Если вы будете участвовать в событии
/out Если вы не хотите участвовать в событии
/results Чтобы посмотреть текущий список участников
'''
members_list = '''
{% for member in game.members %}\
№{{ forloop.counter }} - {% if member.user %}{{ member.user.name }}{% else %}{{ member.guest_name }}{% endif %}
{% endfor %}
'''
start_voting_template = '''
Спасибо, что используете SportUp! Выберите лучшего игрока прошедшего матча. \
Для этого отправьте номер, стоящий рядом с игроком, \
например /vote4, если хотите проголосовать за игрока под №4
''' + members_list
game_members_list = '''
В данный момент на событие \
{{ game.date }} {{ game.title }} {{ game.address_text }} \
{{ game.start_time }} — {{ game.end_time }} \
{{ game.members_count }} участников {{ game.team_count }} команды идут \
{{ game.members.count }}/{{ game.members_count }}
''' + members_list
user_joined = "{{ user }} будет присутствовать в {{ game.date }} {{ game.title }}. \
                Участвует {{ game.members.count }}/{{ game.members_count }}"
user_leaved = "{{ user }} не будет присутствовать в {{ game.date }} {{ game.title }}. \
                Участвует {{ game.members.count }}/{{ game.members_count }}"
game_forced_finished = "Предыдущая игра успешно завершена. Вы можете создать новую"
