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
    path('delete-receipt/<int:id>/',views.delete_receipt),
    path('total-receipt/',views.total_receipt),
    path('branch/',views.branch_page),
    path('add-branch/',views.add_branch),
    path('update-branch/<int:id>/',views.update_branch),
    path('delete-branch/<int:id>/',views.delete_branch),

    #Branch Operation
    path('branch-home/',views.branch_home),
    path('add-branch-receipt/',views.add_branch_receipt),
    path('branch-total-receipt/',views.branch_total_receipt),
    path('employee/',views.employee_page),
    path('add-employee/',views.add_employee),
    path('update-employee/<int:id>/',views.update_employee),
    path('delete-employee/<int:id>/',views.delete_employee),

    #Employee Operation
    path('employee-home/',views.employee_home),
    path('add-employee-receipt/',views.add_employee_receipt),
    path('employee-total-receipt/',views.employee_total_receipt),

    #Admin Filter Data
    path('filter-branch-data/<str:email>/',views.admin_filter_receipt),
    path('filter-employee-data/<str:email>/',views.branch_filter_employee_receipt),
    #Pag Not Found
    path('<str:name>/',views.not_found)

]
