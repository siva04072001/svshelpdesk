from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('superadmin/', views.superadmin, name='superadmin'),
    path('superadminview/', views.superadminview, name='superadminview'),
    path('update_user/<int:Id>/', views.update_user, name='update_user'),
    path('delete_user/<int:Id>/', views.delete_user, name='delete_user'),
    path('assign_user/<int:Id>/', views.assign_user, name='assign_user'),
    path('adminHelpdesk/', views.admin, name='admin'),
    path('adminclosed/', views.adminclosed, name='adminclosed'),
    path('close_ticket/<int:Id>/', views.close_ticket, name='close_ticket'),
    path('assign_ticket/<int:Id>/', views.assign_ticket, name='assign_ticket'),
    path('update_ticket/<int:Id>/', views.update_ticket, name='update_ticket'),
    path('engassign_ticket/<int:Id>/', views.engassign_ticket, name='engassign_ticket'),
    path('engupdate_ticket/<int:Id>/', views.engupdate_ticket, name='engupdate_ticket'),
    path('engineer/', views.engineerticket, name='engineer'),
    path('engineerclosed/', views.engineerticketclosed, name='engineerclosed'),
    path('employee/', views.userticket, name='employee'),
    path('employee_status/', views.statusticket, name='employee_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)