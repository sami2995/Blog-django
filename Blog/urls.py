
from django.contrib import admin
from django.urls import path
from News.views import blog, blog_detail,category_blog,category_list,news_admin,article_edit,delete_news
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('act-admin/', admin.site.urls),
    path('',blog, name="news_url"),
    path('news/<str:title1>/',blog_detail, name="news_detail_url"),
    path('category/<str:category_name>/',category_blog, name="category_blog_url"),
    path('category_list/',category_list,name="category_list_url"),
    path('news_admin/',news_admin, name="news_admin_url"),
    path('article_edit/<int:news_id>/',article_edit, name="article_edit_url"),
    path('delete_news/<int:news_id>/',delete_news, name="delete_news_url"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
