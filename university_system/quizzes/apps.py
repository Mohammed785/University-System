from django.apps import AppConfig


class QuizzesConfig(AppConfig):
    name = 'quizzes'
    def ready(self) -> None:
        import quizzes.signals