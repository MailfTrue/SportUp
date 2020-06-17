from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from .wa_bot import wa
import json


@csrf_exempt
def hook(request):
    if request.method == 'POST':
        json_string = request.body.decode('utf-8')
        json_data = json.loads(json_string)
        if json_data['typeWebhook'] == 'incomingMessageReceived':
            wa.process_message(json_data)
    return HttpResponse(status=200)
