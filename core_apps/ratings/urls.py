from .views import RatingCreateView
from django.urls import path

urlpatterns = [
    path('rate_article/<uuid:article_id>/', RatingCreateView.as_view(), name = 'rating-create')
]