"""This script is use to handle view page of mysite.

Author: Vichisorn Wejsupakul
Date: 10/9/2020
"""
from django.shortcuts import redirect


def index(request):
    """Redirect to the polls index."""
    return redirect("polls:index")
