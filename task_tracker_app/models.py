from django.db import models
from django.urls import reverse
from django.utils import timezone


class ListModel(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title

    def total_tasks(self):
        return self.itemmodel_set.count()

    def done_tasks(self):
        return self.itemmodel_set.filter(done=True).count()


def one_month():
    return timezone.now() + timezone.timedelta(weeks=4)


class ItemModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(default=one_month)
    belong_list = models.ForeignKey(ListModel, on_delete=models.CASCADE)
    done = models.BooleanField(blank=True, null=False, default=False)

    def get_absolute_url(self):
        return reverse(

            "item-update", args=[str(self.belong_list.id), str(self.id)]

        )

    def __str__(self):
        return f"{self.title}: сделать к {self.due_date} {'✔️' if self.done else '✖️'}"
