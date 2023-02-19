from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    BonusCardListView,
    BonusCardDetailView,
    BonusCardDeleteView,
    TrashListView,
    TrashDetailView,
    SearchListView,
    BonusCardGenerateView,
    InfoAboutCard,
    CreateOrders,
    api_root,
    CardList,
    OrderList,
    OrderDetail,
    ProductList,
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

urlpatterns += format_suffix_patterns([
    path('api/', include(
        [
            path('', api_root),
            path('cards/', include(
                [
                    path('', CardList.as_view(), name='card-list'),
                    path('<str:number>/', InfoAboutCard.as_view(),
                         name='get-info-about-card'),

                ]
            )),
            path('orders/', include(
                [
                    path('', OrderList.as_view(), name='order-list'),
                    path('<int:pk>/', OrderDetail.as_view(), name='order-detail'),
                    path('create/<str:number>', CreateOrders.as_view(), name='create-order'),  
                ]
            )),
            path('products/', include(
                [
                    path('', ProductList.as_view(), name='product-list'),
                ]
            )),
        ]
    )),

])
