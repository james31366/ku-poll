"""This script is use to test the logic of KU Polls web application.

Test about question model for database.

Author: Vichisorn Wejsupakul
Date: 10/31/2020
"""
import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


def create_question(question_text, date_time):
    """Create a question for using in the test method.

    The question create with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).

    Args:
        question_text: text of the question in the question model.
        date_time: days for public date and end date.

    Returns: the object of question that user need to create from question text and date.

    """
    pub_time = timezone.now() + date_time
    end_time = pub_time + 2 * abs(date_time)
    return Question.objects.create(question_text=question_text, pub_date=pub_time,
                                   end_date=end_time)


class QuestionModelTests(TestCase):
    """Test for model of question that can use correctly or not."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = datetime.timedelta(days=30)
        future_question = create_question(question_text="Future Question", date_time=time)
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
        time = datetime.timedelta(days=30)
        future_question = create_question(question_text="Future Question", date_time=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_after_pub_date(self):
        """is_published() returns True for question whose pub_date was in the past and before end date."""
        pub_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = pub_time + datetime.timedelta(hours=23, minutes=59, seconds=59)
        old_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(old_question.is_published(), True)

    def test_can_vote_with_before_pub_date(self):
        """can_vote() return False for question whose pub_date is in the future."""
        time = datetime.timedelta(days=30)
        future_question = create_question(question_text="Future Question", date_time=time)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_with_after_pub_date(self):
        """can_vote() return True for question whose pub_date was in the past and before end date."""
        pub_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = pub_time + datetime.timedelta(days=2)
        old_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(old_question.can_vote(), True)

    def test_can_vote_with_after_end_date(self):
        """can_vote() return False for the question whose end_date was in the past."""
        pub_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end_time = pub_time + datetime.timedelta(minutes=30)
        close_question = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(close_question.can_vote(), False)
