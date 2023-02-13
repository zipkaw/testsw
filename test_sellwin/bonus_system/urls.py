from django.urls import path, include

from .views import BonusCardListView, BonusCardDetailView , BonusCardDelete
urlpatterns = [
    path('cards/', BonusCardListView.as_view(), name='all-cards'),
    path('cards/<int:pk>', BonusCardDetailView.as_view(), name='card'),
    path('cards/<int:pk>/delete', BonusCardDelete.as_view(), name='delete-card'),
    # path('story/', ), 
    # path('generate/', ), 
]