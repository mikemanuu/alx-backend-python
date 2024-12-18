from django.contrib import admin
from django.urls import path
from .views import ConversationListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/conversations/', ConversationListView.as_view(),
         name='conversation_list'),
]
