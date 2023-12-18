from django.contrib import admin
from django.urls import path
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_page),
    path('about/',views.about_page),
    path('blog/',views.blog_page),
    path('single-blog/',views.single_blog_page),
    path('contact/',views.contact_page),
]
