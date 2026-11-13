from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
    path('my-results/', views.my_results, name='my_results'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher-dashboard/create-test/',views.create_test,name='create_test'),
    path('teacher-dashboard/<int:test_id>/add-question/',views.create_question,name='create_question'),
    path('teacher-dashboard/edit-question/<int:question_id>/',views.edit_question,name='edit_question'),
    path('teacher-dashboard/delete-question/<int:question_id>/',views.delete_question,name='delete_question'),
    path('teacher-dashboard/results/',views.teacher_results,name='teacher_results'),
    path('teacher-dashboard/results/',views.teacher_results,name='teacher_results'),
    path('teacher-dashboard/edit-test/<int:test_id>/',views.edit_test,name='edit_test'),
    path('teacher-dashboard/delete-test/<int:test_id>/',views.delete_test,name='delete_test'),
    path('teacher-dashboard/attempt/<int:attempt_id>/',views.attempt_detail,name='attempt_detail'),
    
]