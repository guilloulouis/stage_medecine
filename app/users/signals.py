from django.db.models import Sum


def stage_added_to_student(sender, **kwargs):
    if kwargs['action'] == 'post_add':
        kwargs['instance'].stage_points = kwargs['instance'].stages_done.all().aggregate(total=Sum('value')).get('total') or 0.0
        kwargs['instance'].save()
