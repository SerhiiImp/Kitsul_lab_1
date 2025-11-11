from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
from datetime import datetime

from .views import HomePageView, ArticleList, ArticleCategoryList, ArticleDetail
from .models import Category, Article


class HomeURLTests(TestCase):
    """Тести для головної сторінки (home)"""
    
    def test_home_url_resolves_home_view(self):
        """Перевірка що URL '/' резолвиться до HomePageView"""
        view = resolve('/')
        self.assertEqual(view.func.view_class, HomePageView)
    
    def test_home_view_status_code(self):
        """Перевірка що головна сторінка повертає статус 200"""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_uses_correct_template(self):
        """Перевірка що головна сторінка використовує правильний шаблон"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class ArticlesListURLTests(TestCase):
    """Тести для списку статей (articles-list)"""
    
    def test_articles_list_url_resolves_article_list_view(self):
        """Перевірка що URL '/articles' резолвиться до ArticleList"""
        view = resolve('/articles')
        self.assertEqual(view.func.view_class, ArticleList)
    
    def test_articles_list_view_status_code(self):
        """Перевірка що список статей повертає статус 200"""
        url = reverse('articles-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_articles_list_view_uses_correct_template(self):
        """Перевірка що список статей використовує правильний шаблон"""
        response = self.client.get(reverse('articles-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles_list.html')
    
    def test_articles_list_with_articles(self):
        """Перевірка що список статей відображає статті"""
        category = Category.objects.create(category='Test Category', slug='test-category')
        article = Article.objects.create(
            title='Test Article',
            description='Test Description',
            slug='test-article',
            pub_date=timezone.now(),
            category=category
        )
        response = self.client.get(reverse('articles-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(article, response.context['items'])


class ArticlesCategoryListURLTests(TestCase):
    """Тести для списку статей за категорією (articles-category-list)"""
    
    def setUp(self):
        """Налаштування тестових даних"""
        self.category = Category.objects.create(
            category='Test Category',
            slug='test-category'
        )
        self.article = Article.objects.create(
            title='Test Article',
            description='Test Description',
            slug='test-article',
            pub_date=timezone.now(),
            category=self.category
        )
    
    def test_articles_category_list_url_resolves_category_list_view(self):
        """Перевірка що URL '/articles/category/<slug>/' резолвиться до ArticleCategoryList"""
        view = resolve('/articles/category/test-category/')
        self.assertEqual(view.func.view_class, ArticleCategoryList)
    
    def test_articles_category_list_view_status_code(self):
        """Перевірка що список статей за категорією повертає статус 200"""
        url = reverse('articles-category-list', kwargs={'slug': self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_articles_category_list_view_uses_correct_template(self):
        """Перевірка що список статей за категорією використовує правильний шаблон"""
        url = reverse('articles-category-list', kwargs={'slug': self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles_list.html')
    
    def test_articles_category_list_filters_by_category(self):
        """Перевірка що список статей фільтрує по категорії"""
        # Створюємо іншу категорію та статтю
        other_category = Category.objects.create(
            category='Other Category',
            slug='other-category'
        )
        other_article = Article.objects.create(
            title='Other Article',
            description='Other Description',
            slug='other-article',
            pub_date=timezone.now(),
            category=other_category
        )
        
        # Перевіряємо що тільки статті з потрібної категорії відображаються
        url = reverse('articles-category-list', kwargs={'slug': self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.article, response.context['items'])
        self.assertNotIn(other_article, response.context['items'])
    
    def test_articles_category_list_with_nonexistent_category(self):
        """Перевірка поведінки з неіснуючою категорією"""
        url = reverse('articles-category-list', kwargs={'slug': 'nonexistent-category'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Список має бути порожнім
        self.assertEqual(len(response.context['items']), 0)


class NewsDetailURLTests(TestCase):
    """Тести для деталей статті (news-detail)"""
    
    def setUp(self):
        """Налаштування тестових даних"""
        self.category = Category.objects.create(
            category='Test Category',
            slug='test-category'
        )
        self.pub_date = timezone.now()
        self.article = Article.objects.create(
            title='Test Article',
            description='Test Description',
            slug='test-article',
            pub_date=self.pub_date,
            category=self.category
        )
        self.year = self.pub_date.year
        self.month = self.pub_date.month
        self.day = self.pub_date.day
    
    def test_news_detail_url_resolves_article_detail_view(self):
        """Перевірка що URL '/articles/<year>/<month>/<day>/<slug>/' резолвиться до ArticleDetail"""
        url = f'/articles/{self.year}/{self.month:02d}/{self.day:02d}/{self.article.slug}/'
        view = resolve(url)
        self.assertEqual(view.func.view_class, ArticleDetail)
    
    def test_news_detail_view_status_code(self):
        """Перевірка що деталі статті повертають статус 200"""
        url = reverse('news-detail', kwargs={
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'slug': self.article.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_news_detail_view_uses_correct_template(self):
        """Перевірка що деталі статті використовують правильний шаблон"""
        url = reverse('news-detail', kwargs={
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'slug': self.article.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_detail.html')
    
    def test_news_detail_view_displays_article(self):
        """Перевірка що деталі статті відображають правильну статтю"""
        url = reverse('news-detail', kwargs={
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'slug': self.article.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['item'], self.article)
    
    def test_news_detail_with_nonexistent_article(self):
        """Перевірка поведінки з неіснуючою статтею"""
        url = reverse('news-detail', kwargs={
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'slug': 'nonexistent-article'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_news_detail_with_wrong_date(self):
        """Перевірка поведінки з неправильною датою"""
        url = reverse('news-detail', kwargs={
            'year': 2020,
            'month': 1,
            'day': 1,
            'slug': self.article.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class URLReverseTests(TestCase):
    """Тести для перевірки правильності reverse() функцій"""
    
    def test_home_reverse(self):
        """Перевірка reverse для home"""
        url = reverse('home')
        self.assertEqual(url, '/')
    
    def test_articles_list_reverse(self):
        """Перевірка reverse для articles-list"""
        url = reverse('articles-list')
        self.assertEqual(url, '/articles')
    
    def test_articles_category_list_reverse(self):
        """Перевірка reverse для articles-category-list"""
        url = reverse('articles-category-list', kwargs={'slug': 'test-slug'})
        self.assertEqual(url, '/articles/category/test-slug/')
    
    def test_news_detail_reverse(self):
        """Перевірка reverse для news-detail"""
        url = reverse('news-detail', kwargs={
            'year': 2024,
            'month': 1,
            'day': 15,
            'slug': 'test-article'
        })
        self.assertEqual(url, '/articles/2024/1/15/test-article/')

