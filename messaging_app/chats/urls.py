from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import ConversationListView, ConversationViewSet, MessageViewSet


router = routers.DefaultRouter()
router.register('conversations', ConversationViewSet, basename='conversations')

nested_router = NestedDefaultRouter(
    router, 'conversations', lookup='conversation')
nested_router.register('messages', MessageViewSet,
                       basename='conversation-messages')


urlpatterns = [
    path('api/conversations/', ConversationListView.as_view(),
         name='conversation_list'),
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
