from django.urls import path

from apps.promos.views import PromoListCreateView, PromoList, PromoPointsView, AssignPromoView, PromoUpdateDestroyView

urlpatterns = [
    # Admin Operations
    path('promos/', PromoListCreateView.as_view()),
    path('promos/<str:promo_code>/', PromoUpdateDestroyView.as_view()),
    path('users/<int:user_id>/promos/', AssignPromoView.as_view()),
    # Normal user Operations
    path('users/me/promos/', PromoList.as_view()),
    path('users/me/promos/<str:promo_code>/', PromoPointsView.as_view()),
]
