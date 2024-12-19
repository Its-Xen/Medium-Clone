from django.urls import path
from .views import *

urlpatterns = [
    path("search/", ArticleElasticSearchView.as_view({"get": "list"}), name = "article_search"),
]
