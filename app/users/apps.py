from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from django.db.models.signals import m2m_changed
        from users.models import Student
        from users.signals import stage_added_to_student
        m2m_changed.connect(stage_added_to_student, sender=Student.stages_done.through)
