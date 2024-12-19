from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationListView, ConversationViewSet, MessageViewSet


router = DefaultRouter()
router.register('conversations', ConversationViewSet, basename='conversations')
router.register('messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/conversations/', ConversationListView.as_view(),
         name='conversation_list'),
    path('', include(router.urls)),
]
