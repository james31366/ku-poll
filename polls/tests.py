"""This script is use to test the logic of KU Polls web application.

Test about QuestionModel, QuestionIndexView, QuestionDetailView.

Author: Vichisorn Wejsupakul
Date: 10/9/2020
"""
import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    """Test for model of question that can use correctly or not."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        pub_time = timezone.now() + datetime.timedelta(days=30)
        end_time = pub_time + datetime.timedelta(days=30)
        future_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for question whose pub_date is older than 1 day."""
        pub_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        end_time = pub_time + datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        pub_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = pub_time + datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_before_pub_date(self):
        """is_published() returns False for question whose pub_date is in the future."""
        pub_time = timezone.now() + datetime.timedelta(days=30)
        end_time = pub_time + datetime.timedelta(days=30)
        future_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_after_pub_date(self):
        """is_published() returns True for question whose pub_date was in the past and before end date."""
        pub_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = pub_time + datetime.timedelta(hours=23, minutes=59, seconds=59)
        old_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(old_question.is_published(), True)

    def test_can_vote_with_before_pub_date(self):
        """can_vote() return False for question whose pub_date is in the future."""
        pub_time = timezone.now() + datetime.timedelta(days=30)
        end_time = pub_time + datetime.timedelta(days=30)
        future_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_with_after_pub_date(self):
        """can_vote() return True for question whose pub_date was in the past and before end date."""
        pub_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = pub_time + datetime.timedelta(hours=23, minutes=59, seconds=59)
        old_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(old_question.can_vote(), True)

    def test_can_vote_with_after_end_date(self):
        """can_vote() return False for the question whose end_date was in the past."""
        pub_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = pub_time + datetime.timedelta(minutes=30)
        close_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(close_question.can_vote(), False)


def create_question(question_text, days):
    """Create a question for using in the test method.

    The question create with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).

    Args:
        question_text: text of the question in the question model.
        days: days for public date and end date.

    Returns: the object of question that user need to create from question text and date.

    """
    pub_time = timezone.now() + datetime.timedelta(days=days)
    end_time = pub_time + datetime.timedelta(days=abs(days))
    return Question.objects.create(question_text=question_text, pub_date=pub_time,
                                   end_date=end_time + datetime.timedelta(days=days))


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
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")

        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past question 2.>', '<Question: Past question 1.>'])


class QuestionDetailViewTests(TestCase):
    """Test the question inside of detail page that is correctly display."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 404 not found."""
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
