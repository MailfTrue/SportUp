import requests
from .models import BotUser
from django.conf import settings


class WhatsAppApi:

    def __init__(self, instance_id, token):
        self.instance_id = instance_id
        self.token = token
        self._message_handlers = []

    def message_handler(self, condition=lambda r: True):

        def wrapper(func):
            self._message_handlers.append({"condition": condition, "func": func})
            return func

        return wrapper

    def process_message(self, request):
        user, new = BotUser.objects.get_or_create(
            defaults={'chat_id': request['senderData']['sender']},
            name=request['senderData']['senderName'])
        setattr(user, 'new', new)
        request['user'] = user

        counter = 0
        for handler in self._message_handlers:
            if handler["condition"](request):
                handler["func"](request)
                return
            counter += 1

    def get_method_url(self, method):
        return f"https://api.green-api.com/waInstance{self.instance_id}/{method}/{self.token}"

    def send_message(self, chat_id, text):
        url = self.get_method_url('sendMessage')
        response = requests.post(url, json={'chatId': chat_id, 'message': text})
        return response.json()

    def send_file(self, **kwargs):
        url = self.get_method_url('sendFileByUrl')
        response = requests.post(url, json=kwargs)
        return response.json()

    def get_group_data(self, group_id):
        url = self.get_method_url('getGroupData')
        response = requests.post(url, json={'groupId': group_id})
        return response.json()


wa = WhatsAppApi(settings.WA_INSTANCE_ID, settings.WA_TOKEN)

