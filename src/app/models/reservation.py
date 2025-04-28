from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.property import Property
from app.models.user import User


class Reservation(models.Model):
    property = models.ForeignKey(
        verbose_name=_("property"),
        to=Property,
        related_name="reservations",
        on_delete=models.CASCADE,
    )
    patron = models.ForeignKey(
        verbose_name=_("patron"),
        to=User,
        related_name="reservations",
        on_delete=models.CASCADE,
    )
    start_date = models.DateField(verbose_name=_("start date"))
    end_date = models.DateField(verbose_name=_("end date"))
    number_of_nights = models.IntegerField(verbose_name=_("number of nights"))
    guests = models.IntegerField(verbose_name=_("number of guests"))
    total_price = models.FloatField(verbose_name=_("total price"))
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
    )

    def __str__(self):
        return f"patron: {self.patron} - dates: {self.start_date} - {self.end_date}"

    class Meta:
        app_label = "app"
        verbose_name = _("reservation")
        verbose_name_plural = _("reservations")
