from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from .green_api import wa
import json


@csrf_exempt
def hook(request):
    json_string = request.body.decode('utf-8')
    json_data = json.loads(json_string)
    if json_data['typeWebhook'] == 'incomingMessageReceived':
        wa.process_message(json_data)
    return HttpResponse(status=200)
