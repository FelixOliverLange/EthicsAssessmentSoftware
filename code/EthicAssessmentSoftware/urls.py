from django.urls import path
from EthicAssessmentSoftware import views
# This follows
#  https://docs.djangoproject.com/en/3.1/topics/http/urls/
#  https://www.laravelcode.com/post/django-3-crud-tutorial-example-with-mysql-and-bootstrap
#  https://docs.djangoproject.com/en/3.1/intro/tutorial03/
# Not the Tutorial followed at
#  https://bezkoder.com/django-crud-mysql-rest-framework/#:~:text=First%2C%20we%20setup%20Django%20Project,operations%20(including%20custom%20finder).
# So in case of any issues, use the REGEX approach proposed there
urlpatterns = [
    path('anwendung/', views.anwendung_list),
    path('anwendung/<str:anwendung_name>/', views.anwendung_details),
    path('anwendung/<str:anwendung_name>/stakeholder/', views.anwendung_stakeholder_list),
    path('anwendung/<str:anwendung_name>/stakeholder/<str:stakeholder_name>/', views.anwendung_stakeholder_details),
    path('anwendung/<str:anwendung_name>/motivation/', views.anwendung_motivation_list),
    path('anwendung/<str:anwendung_name>/motivation/<str:motivation_name>/', views.anwendung_motivation_details),
    path('anwendung/<str:anwendung_name>/motivation/<str:motivation_name>/konsequenz/', views.anwendung_motivation_konsequenz_list),
    path('anwendung/<str:anwendung_name>/motivation/<str:motivation_name>/konsequenz/<str:konsequenz_name>/', views.anwendung_motivation_konsequenz_details),
    path('anwendung/<str:anwendung_name>/ansatz/', views.anwendung_ansatz_list),
    path('anwendung/<str:anwendung_name>/ansatz/<str:ansatz_name>/', views.anwendung_ansatz_details),
    path('anwendung/<str:anwendung_name>/ansatz/<str:ansatz_name>/anforderung/', views.anwendung_ansatz_anforderung_list),
    path('anwendung/<str:anwendung_name>/ansatz/<str:ansatz_name>/anforderung/<str:anforderung_name>/', views.anwendung_ansatz_anforderung_details)
]