from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import ListModel, ItemModel


class ListListView(ListView):
    model = ListModel
    template_name = "task_tracker_app/index.html"


class ListCreate(CreateView):
    model = ListModel
    fields = [
        "title",
        "description"
    ]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Добавить новый список"
        return context


class ListDelete(DeleteView):
    model = ListModel
    success_url = reverse_lazy("index")


class ItemListView(ListView):
    model = ItemModel
    template_name = "task_tracker_app/list.html"

    def get_queryset(self):
        return ItemModel.objects.filter(belong_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["belong_list"] = ListModel.objects.get(id=self.kwargs["list_id"])
        return context


class ItemCreate(CreateView):
    model = ItemModel
    fields = [
        "belong_list",
        "title",
        "description",
        "due_date",
        "done"
    ]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        belong_list = ListModel.objects.get(id=self.kwargs["list_id"])
        initial_data["belong_list"] = belong_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        belong_list = ListModel.objects.get(id=self.kwargs["list_id"])
        context["belong_list"] = belong_list
        context["title"] = "Поставить новую задачу"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.belong_list_id])


class ItemUpdate(UpdateView):
    model = ItemModel
    fields = [
        "belong_list",
        "title",
        "description",
        "due_date",
        "done"
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["belong_list"] = self.object.belong_list
        context["title"] = "Редактировать задачу"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.belong_list_id])


class ItemDelete(DeleteView):
    model = ItemModel

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["belong_list"] = self.object.belong_list
        return context
