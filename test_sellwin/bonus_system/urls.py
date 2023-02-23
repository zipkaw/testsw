from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    BonusCardListView,
    BonusCardDetailView,
    BonusCardDeleteView,
    BonusCardGenerateView,
    TrashListView,
    TrashDetailView,
    SearchListView,
)

urlpatterns = [
    path('', BonusCardListView.as_view(), name='all-cards'),
    path('<int:pk>/', BonusCardDetailView.as_view(), name='card'),
    path('<int:pk>/delete', BonusCardDeleteView.as_view(), name='delete-card'),
    path('trash/', include(
        [
            path('', TrashListView.as_view(), name='trash'),
            path('<int:pk>/', TrashDetailView.as_view(), name='trash_detail'),
        ]
    )),
    path('search/', SearchListView.as_view(), name='search'),
    path('generate/', BonusCardGenerateView.as_view(), name='generate'),

]
