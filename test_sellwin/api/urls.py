from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    api_root,
    CardDetail,
    CreateOrders,
    CardList,
    OrderList,
    OrderDetail,
    ProductList,
)

urlpatterns = format_suffix_patterns([
    path('', api_root, name='api'),
    path('', include(
        [

            path('cards/', include(
                [
                    path('', CardList.as_view(), name='card-list'),
                    path('<str:number>/', CardDetail.as_view(),
                         name='get-info-about-card'),

                ]
            )),
            path('orders/', include(
                [
                    path('', OrderList.as_view(), name='order-list'),
                    path('<int:pk>/', OrderDetail.as_view(),
                         name='order-detail'),
                    path('create/<str:number>',
                         CreateOrders.as_view(), name='create-order'),
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
