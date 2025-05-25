"""
URL configuration for LITReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import authentication.views
import reviews.views
import reviews.models
import authentication.forms


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('inscription_message/', reviews.views.inscription_message, name='inscription_message'),
    path('dashboard/', reviews.views.dashboard, name='dashboard'),
    path('review/create/', reviews.views.create_ticket, name='create_ticket'),
    path('review/create/<int:ticket_id>/', reviews.views.create_review, name='create_review_for_ticket'),
    path('follow/', reviews.views.follow_user, name='follow_user'),
    path('subscriptions/', reviews.views.subscriptions, name='subscriptions'),
    path('ticket-and-review/create/', reviews.views.create_ticket_and_review, name='create_ticket_and_review'),
    path('ticket/<int:ticket_id>/edit/', reviews.views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete/', reviews.views.delete_ticket, name='delete_ticket'),
    path('unfollow/<int:follow_id>/', reviews.views.unfollow_user, name='unfollow_user'),
    path('review/<int:review_id>/edit/', reviews.views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', reviews.views.delete_review, name='delete_review'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
