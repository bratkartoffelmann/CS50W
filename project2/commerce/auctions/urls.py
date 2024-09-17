from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category/<str:category_type>", views.category, name="category"),
    path("listing/<str:listing_id>", views.load_listing, name='listing'),
    path('create-listing/', views.create_listing, name='create-listing'),
    path("listing/<int:listing_id>/toggle-watchlist", views.toggleWatchlist, name='toggle-watchlist'),
    path("listing/<int:listing_id>/add-comment", views.addComment, name='add-comment'),
    path("listing/<int:listing_id>/add-bid", views.addBid, name='add-bid'),
    path("listing/<int:listing_id>/close-auction", views.closeAuction, name='close-auction'),
    path("watchlist", views.watchlist, name='watchlist'),
]
