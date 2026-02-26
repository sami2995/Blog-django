
from django.contrib import admin
from django.urls import path
from News.views import blog, blog_detail,category_blog,category_list,news_admin,article_edit,delete_news
from CarRental.views import (
    user_login, user_logout, dashboard,
    car_list, car_detail,
    customer_admin, customer_edit, customer_delete,
    car_admin, car_edit, car_delete,
    rental_admin, rental_edit, rental_delete
)
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
    
    # Car Rental URLs
    path('rental/login/', user_login, name='login_url'),
    path('rental/logout/', user_logout, name='logout_url'),
    path('rental/dashboard/', dashboard, name='dashboard_url'),
    path('rental/cars/', car_list, name='car_list_url'),
    path('rental/cars/<int:car_id>/', car_detail, name='car_detail_url'),
    path('rental/admin/customers/', customer_admin, name='customer_admin_url'),
    path('rental/admin/customers/<int:customer_id>/edit/', customer_edit, name='customer_edit_url'),
    path('rental/admin/customers/<int:customer_id>/delete/', customer_delete, name='customer_delete_url'),
    path('rental/admin/cars/', car_admin, name='car_admin_url'),
    path('rental/admin/cars/<int:car_id>/edit/', car_edit, name='car_edit_url'),
    path('rental/admin/cars/<int:car_id>/delete/', car_delete, name='car_delete_url'),
    path('rental/admin/rentals/', rental_admin, name='rental_admin_url'),
    path('rental/admin/rentals/<int:rental_id>/edit/', rental_edit, name='rental_edit_url'),
    path('rental/admin/rentals/<int:rental_id>/delete/', rental_delete, name='rental_delete_url'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
