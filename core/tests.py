from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from core.models import Category, Item

User = get_user_model()


class CoreTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        # Создаем категории
        self.first_category = Category.objects.create(title='First')
        self.second_category = Category.objects.create(title='Second')

        # Создаем для каждой категории по товару
        self.item_data = {
            'price': 100,
            'description': 'Test'}
        self.item_from_first = Item.objects\
            .create(category=self.first_category, title='First',
                    article='First', **self.item_data)
        self.item_from_second = Item.objects\
            .create(category=self.second_category, title='Second',
                    article='Second', **self.item_data)

        # Создаем пользователей и выдаем разрешения на соответствующие катег.
        self.first_manager = User.objects\
            .create_user(username='first_manager')
        self.first_manager.allowed_categories.add(self.first_category)

        self.second_manager = User.objects \
            .create_user(username='second_manager')
        self.second_manager.allowed_categories.add(self.second_category)

        # Логиним менеджеров
        self.first_manager_client = Client()
        self.first_manager_client.force_login(self.first_manager)

        self.second_manager_client = Client()
        self.second_manager_client.force_login(self.second_manager)

    def get_available_data_for_managers(self) -> dict[User: (Client, Item)]:
        return {
            self.first_manager: (self.first_manager_client, self.item_from_first),
            self.second_manager: (self.second_manager_client, self.item_from_second)}

    def get_unavailable_data_for_managers(self) -> dict[User: (Client, Item)]:
        return {
            self.first_manager: (self.first_manager_client, self.item_from_second),
            self.second_manager: (self.second_manager_client, self.item_from_first)}

    def test_managers_cannot_view_products_from_another_category(self):
        managers = self.get_unavailable_data_for_managers()
        for manager, manager_data in managers.items():
            manager_client, unavailable_item = manager_data
            response = manager_client\
                .get(reverse('item-detail', kwargs={
                    'category_slug': unavailable_item.category.slug,
                    'item_slug': unavailable_item.slug}))
            self.assertEquals(response.status_code, 404)

    def test_managers_can_view_products_from_its_category(self):
        managers = self.get_available_data_for_managers()
        for manager, manager_data in managers.items():
            manager_client, available_item = manager_data
            response = manager_client\
                .get(reverse('item-detail', kwargs={
                    'category_slug': available_item.category.slug,
                    'item_slug': available_item.slug}))
            self.assertEquals(response.status_code, 200)

    def test_managers_cannot_change_items_from_another_category(self):
        managers = self.get_unavailable_data_for_managers()
        for manager, manager_data in managers.items():
            manager_client, unavailable_item = manager_data
            response = manager_client\
                .get(reverse('item-update', kwargs={
                    'category_slug': unavailable_item.category.slug,
                    'item_slug': unavailable_item.slug}))
            self.assertEquals(response.status_code, 404)

    def test_managers_can_change_items_from_category(self):
        managers = self.get_available_data_for_managers()
        for manager, manager_data in managers.items():
            manager_client, available_item = manager_data
            response = manager_client\
                .get(reverse('item-update', kwargs={
                    'category_slug': available_item.category.slug,
                    'item_slug': available_item.slug}))
            self.assertEquals(response.status_code, 200)

    def test_managers_cannot_delete_unavailable_items(self):
        managers = self.get_unavailable_data_for_managers()
        for manager, manager_data in managers.items():
            manager_client, unavailable_item = manager_data
            response = manager_client\
                .get(reverse('item-delete', kwargs={
                    'item_slug': unavailable_item.slug}))
            self.assertEquals(response.status_code, 404)

    def test_managers_can_delete_available_items(self):
        managers = self.get_available_data_for_managers()
        for manager, manager_data in managers.items():
            manager_client, available_item = manager_data
            response = manager_client\
                .get(reverse('item-delete', kwargs={
                    'item_slug': available_item.slug}))
            self.assertEquals(response.status_code, 200)

    def test_admin_can_view_all_categories(self):
        categories = [self.first_category, self.second_category]
        self.first_manager.allowed_categories.add(self.second_category)

        for category in categories:
            response = self.first_manager_client.get(
                reverse('category', kwargs={'category_slug': category.slug}))
            self.assertEquals(response.status_code, 200)
