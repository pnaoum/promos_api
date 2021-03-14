from django.urls import path

from apps.promos.views import PromoListCreateView, UserPromoList, PromoPointsView, PromoUpdateDestroyView

urlpatterns = [
    # Admin Operations
    path('promos/', PromoListCreateView.as_view()),
    path('promos/<str:promo_code>/', PromoUpdateDestroyView.as_view()),
    # Normal user Operations
    path('users/me/promos/', UserPromoList.as_view()),
    path('users/me/promos/<str:promo_code>/points/', PromoPointsView.as_view()),
]
