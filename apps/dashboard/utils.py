from datetime import timedelta

from django.conf import settings
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ProductPerformance:
    def __init__(self, model, date_field_name):
        self.model = model
        self.date_field_name = date_field_name

    def get_all_weekdays(self):
        return [_("Monday"), _("Tuesday"), _("Wednesday"), _("Thursday"), _("Friday"), _("Saturday"), _("Sunday")]

    def get_labels(self):
        end_date = timezone.localtime(timezone.now())

        start_date = end_date - timedelta(days=27)
        labels = []
        labels.append(start_date)
        for _i in range(1, 28):
            start_date += timedelta(days=1)
            labels.append(start_date)

        labels = [str(_(i.strftime("%A"))) for i in labels]
        return labels

    def get_data(self):
        end_date = timezone.localtime(timezone.now())
        start_date = (end_date - timedelta(days=27)).replace(hour=0, minute=0, second=0, microsecond=0)
        data = (
            self.model.objects.filter(**{f"{self.date_field_name}__range": (start_date, end_date)})
            .annotate(day=TruncDay(self.date_field_name))
            .values("day")
            .annotate(count=Count("id"))
        )

        data_dict = {day["day"]: day["count"] for day in data}
        date_list = [start_date + timedelta(days=i) for i in range(0, 28)]
        result_data = [data_dict.get(day, 0) for day in date_list]
        return result_data

    def get_avg(self):
        data = self.get_data()
        result_avg = [sum(data[:i]) / len(data[:i]) for i in range(1, len(data) + 1)]
        return result_avg


def environment_callback(request):
    if settings.DEBUG:
        return [_("Development"), "info"]

    return [_("Production"), "warning"]
