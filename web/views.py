from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# from .models import Question

def index(request):
    content = {
        'title': 'Welcome'
    }
    return render(request, 'web/index.html', content)

def about(request):
    content = {
        'title': 'About'
    }
    return render(request, 'web/about.html', content)

# def detail(request, question_id):
#     # question = get_object_or_404(Question, pk=question_id)
#     render(request, 'web/detail.html', {'hi': 'things'})
#
# def results(request, question_id):
#     # question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': 'question'})
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
#