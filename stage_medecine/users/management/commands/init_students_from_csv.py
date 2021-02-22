from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
import pandas as pd
from users.models import Class, Student
from django.core.mail import send_mail, send_mass_mail


def prepare_mail(password, user):
    return (
        'New Account stages-medecine.fr',
        'Hello,\n'
        'An account on stages-medecine.fr has been created for you.\n'
        'Your credentials are :\n'
        '-username : ' + user.username +
        '\n-password : ' + password +
        "\nIf you can't connect now that might be normal until a procedure starts",
        'admin@stages-medecine.fr',
        [user.email],
    )


class Command(BaseCommand):
    help = 'Import a list of stage in the database'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--csv', dest='csv', default=None,
            help='Specify the csv file to parse',
        )
        parser.add_argument(
            '--promo', dest='promo', default=None,
            help='Specify the promo where to put the students',
        )

    def handle(self, *args, **options):
        csv = options.get('csv')
        csv_reader = pd.read_csv(csv)
        promo = options.get('promo')
        promo_object, created = Class.objects.get_or_create(name=promo)
        student_to_create = []
        users = []
        for index, item in csv_reader.iterrows():
            name = item['Name']
            surname = item['Surname']
            mail = item['Mail']
            index = 1
            while True:
                username = name + '-' + surname if index == 1 else name + '-' + surname + '-' + str(index)
                index += 1
                try:
                    User.objects.get(username=username)
                except ObjectDoesNotExist:
                    users.append(User.objects.create_user(username=username,
                                                          first_name=surname,
                                                          last_name=name,
                                                          email=mail,
                                                          password='temp_password1234',
                                                          is_active=False))
                    break
        mails = []
        for user in users:
            student_to_create.append(Student(user=user, promotion=promo_object))
            password = User.objects.make_random_password()
            mails.append(prepare_mail(password, user))
            user.set_password(password)
            user.save()
        Student.objects.bulk_create(student_to_create, ignore_conflicts=True)
        mail_sent = send_mass_mail(mails, fail_silently=False)
        assert mail_sent == len(users)
