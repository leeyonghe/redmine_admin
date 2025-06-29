from django.urls import path
from . import views

app_name = 'redmine'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('set-language/', views.set_language, name='set_language'),
    path('performance/', views.performance_view, name='performance'),
    path('weekly-report/', views.weekly_report_view, name='weekly_report'),
    path('weekly-report/<int:year>/<int:week>/', views.weekly_report_view, name='weekly_report_with_week'),
    path('monthly-report/', views.monthly_report_view, name='monthly_report'),
    path('monthly-report/<int:year>/<int:month>/', views.monthly_report_view, name='monthly_report_with_month'),
    path('yearly-report/', views.yearly_report_view, name='yearly_report'),
    path('yearly-report/<int:year>/', views.yearly_report_view, name='yearly_report_with_year'),
] 