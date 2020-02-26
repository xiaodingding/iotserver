from django.apps import AppConfig
import sys
from multiprocessing import Process

class MqttConfig(AppConfig):
    name = 'mqtt'
    # def ready(self):
    #     print("mqtt ready")

# django-celery            3.3.1
