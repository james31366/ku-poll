"""This script is use to test the logic of KU Polls web application.

Test about detail page for website.

Author: Vichisorn Wejsupakul
Date: 10/31/2020
"""
import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .test_question_model import create_question


def create_user(username, email, password):
    user = User.objects.create_user(username, email, password)
    return user


class QuestionDetailViewTests(TestCase):
    """Test the question inside of detail page that is correctly display."""

    def setUp(self) -> None:
        user = create_user('test', 'test@gmail.com', 'testPassword')

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 404 not found."""
        login = self.client.login(username='test', password='testPassword')
        self.assertTrue(login, "Login fail")
        time = datetime.timedelta(days=5)
        future_question = create_question(question_text="Future question.", date_time=time)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        login = self.client.login(username='test', password='testPassword')
        self.assertTrue(login, "Login fail")
        time = datetime.timedelta(days=-5)
        past_question = create_question(question_text="Past Question.", date_time=time)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
