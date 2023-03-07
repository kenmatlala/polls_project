from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import QuestionDetailView

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='IndexView'),
    # ex: /polls/5/
    path('<int:pk>/', QuestionDetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    path('<int:poll_id>/results/', views.result_views, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path("login/", views.login_request, name="login"),

    path('register/', views.register_request, name="register"),

    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
