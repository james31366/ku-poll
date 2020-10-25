"""This script is use to handle view page of the KU Polls web application.

Author: Vichisorn Wejsupakul
Date: 10/9/2020
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import CreateUserForm
from .models import Choice, Question


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('polls:index')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'polls/login.html', context)


def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for " + user)

            return redirect('polls:login')

    context = {'form': form}
    return render(request, 'polls/registration.html', context)


def logout_user(request):
    logout(request)
    return redirect('polls:login')


class IndexView(generic.ListView):
    """Class that handle how the question display in the index page of ku poll web application.

    It will display the question that create by admin in a list of question at index page.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return all published questions (not including those set to be published in the future).

        Returns: all published questions.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    """Class that handle how the polls display in detail page."""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet.

        Returns: the filter for the question that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Class that handle how the polls display in result page."""
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id: int):
    """This function need to handle the vote system and not let the user vote the question that after the end date.

    Args:
        request: A HttpRequest object, which contains data about the request.
        question_id: The id of each question that create by the admin.

    Returns: the vote page that let the user vote a polls that come form the detail page.

    """
    question = get_object_or_404(Question, pk=question_id)
    if question.can_vote():
        try:
            select_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form
            return render(request, 'polls/detail.html',
                          {'question': question, 'error_message': "You didn't select a choice.", })
        else:
            select_choice.votes += 1
            select_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    else:
        messages.error(request, "Polls not published yet or does not exist")
        return redirect('polls:index')
