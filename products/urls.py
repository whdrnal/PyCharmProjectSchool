
from django.urls import path, include

from products import views

app_name = 'products'

urlpatterns = [
    path('list/', views.index, name='list'),
    path('<int:product_id>/', views.detail, name='detail'),
    path('<int:product_id>/question/create', views.question_create, name='question_create'),
    path('question/<int:question_id>/modify', views.question_modify, name='question_modify'),
]
