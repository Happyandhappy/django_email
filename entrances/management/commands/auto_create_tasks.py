from django.core.management.base import BaseCommand
from entrances.models import Entrance
from tasks.models import Task
from nomenclatures.models import Priority, TaskType
from vhodove.helper import first_day_of_month, last_day_of_month


class Command(BaseCommand):
    def handle(self, *args, **options):
        entrances = Entrance.objects.filter(active=True, auto_assign_monthly_tasks=True)
        for e in entrances:
            me = e.monthlyexpence_set.all()
            for m in me:
                if not Task.objects.filter(task_type=m.task_type, entrance=e, apartment__isnull=True, from_date=first_day_of_month(), to_date=last_day_of_month()).exists():
                    t = Task()
                    t.title = m.task_type.title
                    t.task_type = m.task_type
                    t.priority = Priority.objects.get(default=True)
                    t.entrance = e
                    t.from_date = first_day_of_month()
                    t.to_date = last_day_of_month()
                    t.date = first_day_of_month()
                    t.price = m.price if m.price else 0
                    t.assignee = m.assignee
                    t.save()

            apartments = e.apartment_set.all()
            task_type_fee = task_type_fee = TaskType.objects.get(default_fee=True)
            for a in apartments:
                if not Task.objects.filter(task_type=task_type_fee, entrance=e, apartment=a, from_date=first_day_of_month(), to_date=last_day_of_month()).exists():
                    t = Task()
                    t.title = task_type_fee.title
                    t.task_type = task_type_fee
                    t.priority = Priority.objects.get(default=True)
                    t.entrance = e
                    t.apartment = a
                    t.from_date = first_day_of_month()
                    t.to_date = last_day_of_month()
                    t.date = first_day_of_month()
                    t.price = a.monthly_fee
                    t.save()
