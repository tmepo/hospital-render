from django.urls import path,re_path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('index/', views.index, name='index'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('home/',views.index,name='home'),
    path('login/',views.login_user,name='login_user'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('edit/<int:patient_id>/',views.update_patient,name='update_patient'),
    path('delete/<int:patient_id>/',views.delete_patient,name='delete_patient'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('show_doctors/',views.show_doctors,name='show_doctors'),
    path('edit_doctors/<int:doctor_id>/',views.update_doctor,name='update_doctor'),
    path('delete_doctors/<int:doctor_id>/',views.delete_doctor,name='delete_doctor'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('update_appointment/<int:appointment_id>/',views.update_appointment,name='update_appointment'),
    path('delete_appointment/<int:appointment_id>/',views.delete_appointment,name='delete_appointment'),
    path('add_service/', views.add_service, name='add_service'),
    path('update_service/<int:service_id>/', views.update_service, name='update_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('add_billing/', views.add_billing, name='add_billing'),
    path('update_billing/<int:billing_id>/', views.update_billing, name='update_billing'),
    path('delete_billing/<int:billing_id>/', views.delete_billing, name='delete_billing'),
    path('make_appointment/', views.make_appointment, name='make_appointment'),
    path('view_appointment/',views.view_appointments,name='viewappointment'),


    



    


]
