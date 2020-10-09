"""This script is use to handle admin page of KU Polls web application.

Author: Vichisorn Wejsupakul
Date: 10/9/2020
"""
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Class that initial the choice for admin to write text and add more choice to vote."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Class that let admin put the question public date and end date.

    For that vote and also display the list of question to admin index page.
    """
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'],
                              'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'end_date', 'is_published')
    list_filter = ['pub_date', 'end_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
