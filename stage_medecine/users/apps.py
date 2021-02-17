from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from django.contrib.auth.models import User
        from django.db.models.signals import m2m_changed, post_save
        from users.models import Student
        from users.signals import stage_added_to_student, create_user_student, save_user_student
        m2m_changed.connect(stage_added_to_student, sender=Student.stages_done.through)
        post_save.connect(create_user_student, sender=User)
        post_save.connect(save_user_student, sender=User)
