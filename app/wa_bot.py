from .green_api import wa
from .utils import check_is_admin, get_template, get_current_game
from .models import Game, GameMember, Vote
from .bot_form_processor import BotFormProcessor
from . import phrases
from random import shuffle


form_processor = BotFormProcessor()


def send_not_admin_error(chat_id, result):
    if result is None:
        wa.send_message(chat_id, 'Не удалось создать игру. Возможно, вы находитесь не в группе')
    else:
        wa.send_message(chat_id, 'У вас нет прав на использование этой команды')


@wa.message_handler(lambda r: r['messageData'].get('textMessageData') == '/create')
def create_handler(r):
    is_admin = check_is_admin(r)
    if not is_admin:
        send_not_admin_error(r['senderData']['chatId'], is_admin)
    form_processor.start_form('create_game', r['user'], extra_data={'chat_id': chat_id})


@wa.message_handler(lambda r: r['messageData'].get('textMessageData') == '/in')
@wa.message_handler(lambda r: r['messageData'].get('textMessageData').startswith('/addguest'))
def join_game(r):
    guest_mode = r['messageData'].get('textMessageData').startswith('/addguest')
    chat_id = r['senderData']['chatId']
    game = get_current_game(chat_id)
    if not game:
        text = 'Игра еще не создана'
    elif game.members.count() >= game.members_count:
        text = f'Извините, но в данный момент занято {game.members.count()} из {game.members_count} мест'
    else:
        if not guest_mode:
            GameMember.objects.create(game=game, user=r['user'])
        else:
            guest_name = ' '.join(r['messageData'].get('textMessageData').split()[1:])
            GameMember.objects.create(game=game, guest_inviter=r['user'], guest_name=guest_name)
        text = get_template(phrases.user_joined).render({
            'user': r['senderData']['senderName'],
            'game': game
        })
    wa.send_message(chat_id, text)


@wa.message_handler(lambda r: r['messageData'].get('textMessageData') == '/out')
@wa.message_handler(lambda r: r['messageData'].get('textMessageData').startswith('/deleteguest'))
def leave_game(r):
    guest_mode = r['messageData'].get('textMessageData').startswith('/deleteguest')
    chat_id = r['senderData']['chatId']
    game = get_current_game(chat_id)
    if not game:
        text = 'Игра еще не создана'
    else:
        if guest_mode:
            guest_name = ' '.join(r['messageData'].get('textMessageData').split()[1:])
            member = GameMember.objects.filter(game=game, guest_name__icontaint=guest_name).first()
            if not member:
                member = GameMember.objects.filter(game=game, guest_name=guest_name, guest_inviter=r['user']).first()
        else:
            member = GameMember.objects.filter(game=game, user=r['user']).first()
        if not member:
            if not guest_mode:
                text = f'Вы не зарегистрированы в текущей игре'
            else:
                text = "Гость не найден"
        else:
            member.delete()
            text = get_template(phrases.user_joined).render({
                'user': r['senderData']['senderName'],
                'game': game
            })
    wa.send_message(chat_id, text)


@wa.message_handler(lambda r: r['messageData'].get('textMessageData') == '/list')
def game_members_list(r):
    chat_id = r['senderData']['chatId']
    game = get_current_game(chat_id)
    text = get_template(phrases.game_members_list).render({'game': game})
    wa.send_message(chat_id, text)


@wa.message_handler(lambda r: r['messageData'].get('textMessageData') == '/randomize')
def game_members_list(r):
    chat_id = r['senderData']['chatId']
    game = get_current_game(chat_id)
    teams = [[]] * game.team_count
    members = list(game.members)
    shuffle(members)
    for k, member in enumerate(members):
        teams[k % game.team_count].append(members)

    text = ""
    for k in range(game.team_count):
        text += f"Команда {k + 1}"
        text += '\n'.join(str(u.user or u.guest_name) for u in teams[k])
    wa.send_message(chat_id, text)


@wa.message_handler(lambda r: r['messageData'].get('textMessageData') == '/stop')
def create_handler(r):
    is_admin = check_is_admin(r)
    chat_id = r['senderData']['chatId']
    if not is_admin:
        text = 'У вас нет прав на выполнение этой операции'
    else:
        game = get_current_game(chat_id)
        if game:
            game.delete()
        text = phrases.game_forced_finished
    wa.send_message(chat_id, text)


def create_game_callback(user, data):
    address = data.pop('address')
    address_text = address
    game = Game(
        creator=user,
        address_text=address_text,
        **data
    )
    game.save()
    text = get_template(phrases.game_template).render({'game': game})
    wa.send_message(game.chat_id, text)


def start_voting(game):
    text = get_template(phrases.start_voting_template).render({'game': game})
    wa.send_message(game.chat_id, text)








