# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.template import loader
from .models import Choice, Question

def index_depr(request):
	latest_question_list = Question.objects.order_by('-pub_date')
	template = loader.get_template('polls/index.html')
	context = {
		'latest_question_list': latest_question_list,
	}
	return HttpResponse(template.render(context, request))

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')
	context = {
		'latest_question_list': latest_question_list,
	}

	return render(request, 'polls/index.html', context)

def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except:
		raise Http404("Question does not exist")
	return render(request, 'polls/detail.html', {'question':question})

def results_depr(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})


def vote_depr(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice."
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return a HttpResponseRedirect,prevents user from double
		# submitting when they hit back
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



