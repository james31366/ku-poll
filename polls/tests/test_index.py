"""This script is use to test the logic of KU Polls web application.

Test about index page for website.

Author: Vichisorn Wejsupakul
Date: 10/31/2020
"""
import datetime

from django.test import TestCase
from django.urls import reverse

from polls.tests.test_question_model import create_question


class QuestionIndexViewTests(TestCase):
    """Test the view of question that it correctly display in the index pages."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        time = datetime.timedelta(days=-30)
        create_question(question_text="Past question.", date_time=time)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        time = datetime.timedelta(days=30)
        create_question(question_text="Future question.", date_time=time)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")

        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        time1 = datetime.timedelta(-30)
        time2 = datetime.timedelta(30)
        create_question(question_text="Past question.", date_time=time1)
        create_question(question_text="Future question.", date_time=time2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        time1 = datetime.timedelta(-30)
        time2 = datetime.timedelta(-5)
        create_question(question_text="Past question 1.", date_time=time1)
        create_question(question_text="Past question 2.", date_time=time2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past question 2.>', '<Question: Past question 1.>'])
