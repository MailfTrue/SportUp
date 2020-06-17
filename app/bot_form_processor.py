import re
from jsonstore import JsonStore
from .green_api import wa
from .utils import get_func_by_path


FORMS = {
    'create_game': {
        'callback': 'app.wa_bot.create_game_callback',
        'before_text': 'Заполните форму:',
        'fields': {
            'title': {
                'question': '1.	Название игры (Футбол на Лужниках, Баскетбол в Черемушках и т.д.)',
            },
            'address': {
                'question': '2.	Адрес (Старая Басманная д. 15 или местоположение)'
            },
            'date': {
                'question': '3.	Дата игры (24.01.2017)',
                'type': 're',
                're': re.compile('[0-3]?[0-9].[0-1][0-9].202[0-9]'),
                'error': 'Введите дату в формате 01.01.2020'
            },
            'start_time': {
                'question': '4.	Время начала игры (21:45)',
                'type': 're',
                're': re.compile('[0-2]?[0-9]:[0-5][0-9]'),
                'error': 'Введите время в формате 9:00'
            },
            'end_time': {
                'question': '5.	Время окончания игры (23:00)',
                'type': 're',
                're': re.compile('[0-2]?[0-9]:[0-5][0-9]'),
                'error': 'Введите время в формате 9:00'
            },
            'members_count': {
                'question': '6.	Количество участников (к примеру «18»)',
                'type': int,
                'error': 'Введите число без лишних символов'
            },
            'team_count': {
                'question': '7.	Количество команд (к примеру 3)',
                'type': int,
                'error': 'Введите число без лишних символов'
            },
            'rent_price': {
                'question': '8.	Укажите стоимость аренды поля ',
                'type': int,
                'error': 'Введите число без лишних символов'
            },
        },
        'after_text': 'Игра успешно создана'
    }
}


class BotFormProcessor:

    def __init__(self):
        self.store = JsonStore('forms.json')

    @staticmethod
    def send_message(user, text):
        wa.send_message(user.chat_id, text)

    @staticmethod
    def get_form_fields(form_key):
        return list(FORMS[form_key]['fields'].keys())

    def get_user_form_key(self, user):
        return self.store[user.store_id].form

    def get_user_form(self, user):
        return FORMS[self.get_user_form_key(user)]

    def get_user_field_key(self, user):
        return self.store[user.store_id].field

    def get_user_field(self, user):
        return self.get_user_form(user)[self.get_user_field_key(user)]

    def get_next_field(self, user):
        fields = self.get_form_fields(self.get_user_form_key(user))
        curr_field = self.get_user_field_key(user)
        curr_field_index = fields.index(curr_field)
        if (curr_field_index + 1) == len(fields):
            return None
        else:
            return fields[curr_field_index + 1]

    def start_form(self, form_key, user, extra_data=None):
        if not extra_data:
            extra_data = {}
        form = FORMS[form_key]
        self.store[user.store_id] = {
            'form': form_key,
            **extra_data
        }
        user.state = 'form'
        user.save()
        self.send_message(user, form['before_text'])

    def send_field(self, user, field):
        form = self.get_user_form(user)
        self.send_message(user, form[field]['question'])

    def send_error_field(self, user):
        field = self.get_user_field(user)
        text = field.get('error') or field.get('question')
        self.send_message(user, text)

    def check_field(self, user, input_):
        field = self.get_user_field(user)
        field_type = field.get('type')
        error_input = False
        if field_type:
            if callable(field_type):
                try:
                    field_type(input_)
                except:
                    error_input = True
            elif field_type == 're':
                error_input = not field['re'].fullmatch(input_)

        if error_input:
            self.send_error_field(user)
        else:
            next_field = self.get_next_field(user)
            if next_field:
                self.send_field(user, next_field)
            else:
                self.end_form(user)

    def end_form(self, user):
        form = self.get_user_form(user)
        callback = get_func_by_path(form['callback'])
        callback(user=user, data=self.store[user.store_id])
        self.send_message(user, form['after_text'])




