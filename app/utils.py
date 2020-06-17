from .green_api import wa
from .models import Game
import importlib
from django.template import engines


def check_is_admin(r):
    return True
    chat_id = r['senderData']['chatId']
    user_id = r['senderData']['sender']
    try:
        group_data = wa.get_group_data(chat_id)
    except Exception as e:
        print('get group data exeption', e)
        return None
    result = False
    for k in group_data['participants']:
        if k['id'] == user_id:
            result = k['isAdmin']
            break
    return result


def get_current_game(chat_id):
    return Game.objects.filter(chat_id=chat_id, voting_started=False).first()


def get_func_by_path(path):
    mod_name, func_name = path.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    result = func()


def get_template(string):
    return engines['django'].from_string(string)


def get_message_text(r):
    try:
        return r['messageData']['textMessageData']['textMessage']
    except KeyError:
        return ''
