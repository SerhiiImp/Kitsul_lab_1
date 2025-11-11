from django.urls import path
from .views import HomePageView, ArticleDetail, ArticleList, ArticleCategoryList

urlpatterns = [
    path(r'', HomePageView.as_view(), name='home'),
    path(r'articles', ArticleList.as_view(), name='articles-list'),
    path(r'articles/category/<slug:slug>/', ArticleCategoryList.as_view(), name='articles-category-list'),
    path(r'articles/<int:year>/<int:month>/<int:day>/<slug:slug>/', ArticleDetail.as_view(), name='news-detail'),
]
