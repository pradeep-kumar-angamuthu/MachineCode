# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Machine
from asgiref.sync import async_to_sync

class MachineConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        machines = Machine.objects.all().values('machine_id', 'axis_id', 'tool_offset', 'feedrate', 'tool_in_use')
        async_to_sync(self.channel_layer.group_send)(
            'machine_group', {
                'type': 'machine_message',
                'message': list(machines)
            }
        )

    def machine_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'machines': message
        }))
