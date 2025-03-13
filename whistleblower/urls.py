from django.urls import include, path
from . import views

app_name = "whistleblower"
urlpatterns = [
    path('', views.home, name='home'),
    path('level-select/', views.level_select, name='level_select'),
    path('level-admin/', views.level_admin, name='level_admin'),
    path('level-user/', views.level_user, name='level_user'),
    path('home-anon/', views.anon_home, name='home_anon'),
    path('home-admin/', views.home_admin, name='home_admin'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('neighbor-form/', views.neighbor_complaint, name='n-complaint'),
    path('building-form/', views.building_complaint, name='b-complaint'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    path('view-report/<int:pk>/', views.ReportView.as_view(), name='report_view'),
    path('create-group/', views.create_building_group_page, name='create_group_page'),
    path('create-group/confirm', views.create_building_group, name='create_group'),
    path('join-group/', views.join_building_group_page, name='join_group_page'),
    path('join-group/confirm/', views.join_building_group, name="join_group"),
    path('mark_as_resolved/<int:report_id>/', views.mark_as_resolved, name='mark_as_resolved'),
    path('reopen_report/<int:report_id>/', views.reopen_report, name='reopen_report'),
    path('no-access/', views.no_access, name='no_access'),
    path('leave-group/<int:code>/', views.leave_building_group, name='leave_building_group'),
    path('neighbor-anonymous-form/', views.neighbor_anon_complaint, name='n-a-complaint'),
    path('building-anonymous-form/', views.building_anon_complaint, name='b-a-complaint'),
    path('delete/<int:report_id>/', views.delete_complaint, name='delete'),
]