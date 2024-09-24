from django.contrib import admin

from task_tracker_app.models import ItemModel, ListModel

admin.site.register(ItemModel)
admin.site.register(ListModel)
