from django.db import models
from django.urls import reverse
from django.utils import timezone


class ABSModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ListModel(ABSModel):
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


class ItemModel(ABSModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    belong_list = models.ForeignKey(ListModel, on_delete=models.CASCADE)
    done = models.BooleanField(blank=True, null=False, default=False)

    def get_absolute_url(self):
        return reverse(

            "item-update", args=[str(self.belong_list.id), str(self.id)]

        )

    def __str__(self):
        return f"{self.title}: сделать к {self.due_date} {'✔️' if self.done else '✖️'}"

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        if not self.due_date:
            self.due_date = self.created_at + timezone.timedelta(weeks=4)
            super().save(update_fields=['due_date'])
        else:
            super().save(*args, **kwargs)
