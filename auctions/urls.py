from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("categories/", views.categories, name="categories"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("removeFromWatchlist/<int:listing_id>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("addToWatchlist/<int:listing_id>", views.addToWatchlist, name="addToWatchlist"),
    path("addComment/<int:listing_id>", views.addComment, name="addComment"),
    path("placeBid/<int:listing_id>", views.placeBid, name="placeBid"),
    path("endAuction/<int:listing_id>", views.endAuction, name="endAuction"),
]
