from django.test import TestCase
from django.utils import timezone

from task_tracker_app.models import ListModel, ItemModel


class ListModelTest(TestCase):
    def setUp(self):
        ListModel.objects.create(title="Title1", description="Some description")

    def test_title_label(self):
        task_list = ListModel.objects.get(id=1)
        field_label = task_list._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_label(self):
        task_list = ListModel.objects.get(id=1)
        field_label = task_list._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_title_max_length(self):
        task_list = ListModel.objects.get(id=1)
        max_length = task_list._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_title(self):
        task_list = ListModel.objects.get(id=1)
        expected_object_name = task_list.title
        self.assertEqual(str(task_list), expected_object_name)

    def test_get_absolute_url(self):
        task_list = ListModel.objects.get(id=1)
        self.assertEqual(task_list.get_absolute_url(), '/list/1/')


class ItemModelTest(TestCase):
    def setUp(self):
        ItemModel.objects.create(
            title="Title1",
            description="Some description",
            belong_list=ListModel.objects.create(title="Title1", description="Some description")
        )

    def test_title_label(self):
        task_item = ItemModel.objects.get(id=1)
        field_label = task_item._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_label(self):
        task_item = ItemModel.objects.get(id=1)
        field_label = task_item._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_done_field(self):
        task_item = ItemModel.objects.get(id=1)
        field = task_item.done
        self.assertEqual(field, False)

    def test_due_date_field(self):
        task_item = ItemModel.objects.get(id=1)
        field = task_item.due_date
        created_at = task_item.created_at
        self.assertEqual(field, created_at + timezone.timedelta(weeks=4))

    def test_title_max_length(self):
        task_item = ItemModel.objects.get(id=1)
        max_length = task_item._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_due_date(self):
        task_item = ItemModel.objects.get(id=1)
        expected_object_name = f"{task_item.title}: сделать к {task_item.due_date} {'✔️' if task_item.done else '✖️'}"
        self.assertEqual(str(task_item), expected_object_name)

    def test_get_absolute_url(self):
        task_item = ItemModel.objects.get(id=1)
        self.assertEqual(task_item.get_absolute_url(), '/list/1/item/1/')
