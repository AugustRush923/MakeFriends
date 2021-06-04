from django.apps import AppConfig


class ModelConfig(AppConfig):
    name = 'model'

    def ready(self):
        import model.signals
