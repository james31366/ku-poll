"""This script is use to handle the model of question and choice of the KU Polls web application.

Author: Vichisorn Wejsupakul
Date: 10/9/2020
"""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Class that create the model of question for using in database layout and at admin index page."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date')

    def __str__(self):
        """To display the text or content of the question."""
        return self.question_text

    def was_published_recently(self):
        """Check the question that just published in that day or not.

        If publish date is in the future and the published date
        is older than one day it isn't just published but if the
        publish date is in that day it is just published.

        Returns: True = if the question just published
                 False = the question published
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check the question is already published or not.

        If the question is in the past it already published
        but if the question is that need to release in the future.
        It means that the question is not published yet.

        Returns: True = if the question is already published.
                 False = if the question is not published.

        """
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Check the question can vote or not.

        If the question is in the vote time or after published date and before end date of that vote.
        the question is can vote. and in the other hand the question is cannot vote.

        Returns: True = if the current time is at publish date and before end date of the question.
                 False = if the current time is before the publish date and after the end date of the question.

        """
        now = timezone.now()
        return self.pub_date <= now <= self.end_date

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    is_published.short_description = 'Published?'
    is_published.boolean = True
    is_published.admin_order_field = 'pub_date'


class Choice(models.Model):
    """Class that create the model of choice for using in database layout and at admin index page."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """To display the choice of a poll."""
        return self.choice_text
