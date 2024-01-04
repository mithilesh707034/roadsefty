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
    #Admin Operation
    path('login/',views.login_page),
    path('admin-home/',views.admin_home),
    path('logout/',views.logout_page),
    path('vehicle/',views.vehicle_page),
    path('add-vehicle/',views.add_vehicle),
    path('update-vehicle/<int:id>/',views.update_vehicle),
    path('delete-vehicle/<int:id>/',views.delete_vehicle),

    path('receipt-page/',views.receipt_page),
    path('add-receipt/',views.add_receipt),
    path('receipt/',views.receipt_page),
    

]
