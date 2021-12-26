from itertools import product

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from questions.models import Question
from .forms import QuestionForm
from .models import Product


def index(request):
    product_list = Product.objects.order_by()
    context = {'product_list': product_list}
    return render(request, 'products/products_list.html', context)


def detail(request, product_id):
    question_list = Question.objects.filter(content_type=ContentType.objects.get_for_model(Product),
                                            object_id=product_id)
    product = Product.objects.get(id=product_id)
    context = {'product': product, 'question_list': question_list}
    return render(request, 'products/products_detail.html', context)


def question_create(request, product_id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.content_type = ContentType.objects.get_for_model(Product)
            question.object_id = product_id
            question.user = request.user
            question.save()
            return redirect('products:detail', product_id)
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'products/products_detail.html', context)


def question_modify(request, product_id):
    question = get_object_or_404(Question, pk=product_id)
    if request.user != question.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('products:detail', product_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.update_date = timezone.now()
            question.save()
            return redirect('products:detail', product_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'products/question_form.html', context)
