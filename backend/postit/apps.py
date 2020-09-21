from django.apps import AppConfig


class PostitConfig(AppConfig):
    name = 'postit'

    def ready(self):
        import postit.signals
