"""This script is use to test the logic of KU Polls web application.

Test about detail page for website.

Author: Vichisorn Wejsupakul
Date: 10/31/2020
"""
import datetime

from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse

from .test_detail import create_user, create_question


class TestAuth(TestCase):

    def setUp(self) -> None:
        user = create_user('test', 'test@gmail.com', 'testPassword')

    def test_detail_auth(self):
        time = datetime.timedelta(days=-5)
        past_question = create_question(question_text="Past Question.", date_time=time)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_vote_auth(self):
        time = datetime.timedelta(days=1)
        question = create_question(question_text="Auth Question", date_time=time)
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_can_login(self):
        user = authenticate(username='test', password='testPassword')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='testPassword')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)
