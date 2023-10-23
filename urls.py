from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name="login"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('admin_home', views.admin_home, name='admin_home'),
    path('register_category_link', views.register_categoryform, name='register_categoryform'),
    path('register_category', views.register_category, name='register_category'),
    path('view_category', views.view_category,name='view_category'),
    path('edit_categoryform/<int:id>', views.edit_categoryform, name='edit_categoryform'),
    path('update_category', views.update_category, name='update_category'),
    path('delete_category/<int:id>', views.delete_category, name='delete_category'),
    path('register_bookform/<int:id>', views.register_bookform, name='register_bookform'),
    path('register_book', views.register_book, name='register_book'),
    path('view_book/<int:id>',views.view_book, name='view_book'),
    path('view_index/<int:id>', views.view_index, name='view_index'),
    path('edit_index/<int:id>', views.edit_index, name='edit_index'),
    path('update_index/<int:id>', views.update_index, name='update_index'),
    path('add_index/<int:id>', views.add_index, name='add_index'),
    path('reg_index/<int:id>', views.reg_index, name='reg_index'),
    path('example', views.example, name='example'),

    path('upload_page/<int:id>', views.upload_page, name='upload_page'),
    path('delete_page/<int:id>', views.delete_page, name= 'delete_page'),
    path('remove_page', views.remove_page, name='remove_page'),
    path('view_content/<int:id>', views.view_content, name='view_content'),
    path('update_content/<int:pgno>', views.update_content, name='update_content'),
    path('view_pages/<int:id>', views.view_pages, name='view_pages'),
    path('add_page', views.add_page, name='add_page'),
    path('edit_book/<int:id>',views.edit_book, name='edit_book'),
    path('update_book',views.update_book, name='update_book'),
    path('delete_book/<int:id>', views.delete_book, name='delete_book'),
    path('add_cart/<int:id>', views.add_cart, name='add_cart'),
    path('add_image_cart', views.add_image_cart, name='add_image_cart'),
]