from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from crispy_forms.helper import FormHelper
from .files import NewUserForm, LoginForm
from .models import Choice, Question
from django.contrib.auth.mixins import LoginRequiredMixin


# The IndexView class inherits from the generic.ListView class, which is a generic view that displays
# a list of objects. 
# 
# The IndexView class overrides the get_queryset() method to return the last five published questions
# (not including those set to be published in the future)
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


# The QuestionDetailView class is a generic view that displays a question text, with pub_date and
# was_published_recently properties if the question is published
class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


@login_required(login_url='login')
    """
    A function that is called when a user votes on a question.
    
    :param request: The original HttpRequest object
    :param question_id: The primary key of the question whose results we want to display
    :return: The user is being redirected to the results page.
    """
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


    """
    It takes a request and a poll_id, gets the Question object with the given poll_id, and passes it to
    a template called results.html
    
    :param request: The request object is the first parameter to the view function. It contains
    information about the current request
    :param poll_id: The primary key of the poll we're interested in
    :return: The question and the choices
    """
def result_views(request, poll_id):
    templates_name = 'results.html'
    temp = Question.objects.get(pk=poll_id)
    return render(request, templates_name, {'temp': temp})


    """
    If the request is a POST request, then validate the form and save the user. If the form is not
    valid, then display an error message. If the request is not a POST request, then display the form
    
    :param request: The request object
    :return: The render function is being returned.
    """
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("polls:login")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()

    # Use the Crispy Forms helper to add Bootstrap styling to the form
    form.helper = FormHelper()
    form.helper.form_class = 'form-group'
    form.helper.label_class = 'form-label'
    form.helper.field_class = 'form-control'

    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    """
    If the request is a POST request, then validate the form and log the user in. If the request is a
    GET request, then just render the login page
    
    :param request: The request object is passed to the view by Django. It contains all the information
    about the current request
    :return: The login.html template is being returned.
    """
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polls:IndexView')
    else:
        form = LoginForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_view(request):
    """
    It logs out the user and redirects to the IndexView
    
    :param request: The full HTTP request object for this page load
    :return: The logout_view function is returning a redirect to the IndexView.
    """
    logout(request)
    return redirect('polls:IndexView')
