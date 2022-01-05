from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from questions.models import Question
from .forms import QuestionForm
from .models import Product, ProductReal


def index(request):
    page = request.GET.get('page', '1')  # 페이지
    search_keyword = request.GET.get('search_keyword', '')  # 검색어

    # 조회
    product_list = Product.objects.order_by('-id')
    if search_keyword:
        product_list = product_list.filter(
            Q(display_name__icontains=search_keyword) |
            Q(name__icontains=search_keyword)
        ).distinct()

    # 페이징처리
    paginator = Paginator(product_list, 8)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'product_list': page_obj, 'page': page, 'search_keyword': search_keyword}
    return render(request, 'products/products_list.html', context)


def detail(request, product_id):
    question_list = Question.objects.order_by('-id')
    question_list = Question.objects.filter(content_type=ContentType.objects.get_for_model(Product),
                                            object_id=product_id)

    product = Product.objects.get(id=product_id)
    product_reals = ProductReal.objects.filter(product=product)
    form = QuestionForm()
    context = {'product': product, 'question_list': question_list, 'product_reals': product_reals, 'form': form}
    return render(request, 'products/products_detail.html', context)


@login_required(login_url='accounts:login')
def question_create(request, product_id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.content_type = ContentType.objects.get_for_model(Product)
            question.object_id = product_id
            question.user = request.user
            question.save()
            messages.success(request, "질문이 등록되었습니다.")
            return redirect('products:detail', product_id=product_id)
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'products/question_form.html', context)


@login_required(login_url='accounts:login')
def question_modify(request, product_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    product = Product.objects.get(id=product_id)
    if request.user != question.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('products:detail', product_id=product_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.update_date = timezone.now()
            question.user = request.user
            question.save()
            messages.success(request, "질문이 수정되었습니다.")
            return redirect('products:detail', product_id=product_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form, 'product': product, 'question': question}
    return render(request, 'products/question_form.html', context)


@login_required(login_url='accounts:login')
def question_delete(request, product_id, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.user:
        messages.error(request, '삭제권한이 없습니다')
    else:
        question.delete()
        messages.success(request, "질문이 삭제되었습니다.")
        return redirect("products:detail", product_id=product_id)

