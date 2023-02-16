from django.urls import path, include

from .views import (
    BonusCardListView,
    BonusCardDetailView, 
    BonusCardDeleteView, 
    TrashListView, 
    TrashDetailView, 
    SearchListView,
    BonusCardGenerateView, 
)
urlpatterns = [
    path('', BonusCardListView.as_view(), name='all-cards'),
    path('<int:pk>/', BonusCardDetailView.as_view(), name='card'),
    path('<int:pk>/delete', BonusCardDeleteView.as_view(), name='delete-card'),
    path('trash/', include(
        [
            path('', TrashListView.as_view(), name='trash'),
            path('<int:pk>/', TrashDetailView.as_view(), name='trash'),
        ]
    )),
    path('search/', SearchListView.as_view(), name='search'),
    path('generate/', BonusCardGenerateView.as_view(), name='generate'),
]
