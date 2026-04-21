from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Note

User = get_user_model()


class NoteTestCase(TestCase):
    def setUp(self):
        # Создаем двух пользователей
        self.user1 = User.objects.create(email='user1@test.com')
        self.user1.set_password('password123')
        self.user1.save()

        self.user2 = User.objects.create(email='user2@test.com')
        self.user2.set_password('password123')
        self.user2.save()

        # Создаем заметку для первого пользователя
        self.note = Note.objects.create(
            title='Заметка 1',
            content='Секретный текст',
            author=self.user1
        )

    def test_note_list_access(self):
        """Проверка доступа к списку: только свои заметки"""
        self.client.login(email='user1@test.com', password='password123')
        response = self.client.get(reverse('diary:note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Заметка 1')

        # Заходим вторым пользователем
        self.client.login(email='user2@test.com', password='password123')
        response = self.client.get(reverse('diary:note_list'))
        self.assertNotContains(response, 'Заметка 1')  # Второй не должен видеть чужую запись

    def test_note_detail_security(self):
        """Проверка: нельзя открыть чужую заметку по ID"""
        self.client.login(email='user2@test.com', password='password123')
        response = self.client.get(reverse('diary:note_detail', args=[self.note.id]))
        self.assertEqual(response.status_code, 404)

    def test_note_create(self):
        """Проверка создания заметки"""
        self.client.login(email='user1@test.com', password='password123')
        response = self.client.post(reverse('diary:note_create'), {
            'title': 'Новая запись',
            'content': 'Текст новой записи'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title='Новая запись', author=self.user1).exists())

    def test_note_search(self):
        """Проверка поиска"""
        self.client.login(email='user1@test.com', password='password123')
        response = self.client.get(reverse('diary:note_list'), {'q': 'Секретный'})
        self.assertContains(response, 'Заметка 1')

        response = self.client.get(reverse('diary:note_list'), {'q': 'Несуществующий'})
        self.assertNotContains(response, 'Заметка 1')
