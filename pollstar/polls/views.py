from .models import Question,Choice
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    lql = Question.objects.order_by('-pub_date')[:5]
    
    context = {
        'lql':lql,
    }
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/result.html',{'question':question})

def vote(request,question_id):
   # print(request.POST['choice'])
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,'error_message':"You didnt select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save() 
    return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))