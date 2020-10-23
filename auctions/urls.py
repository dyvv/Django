from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create", views.create_listing, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("close/<int:listing_id>", views.close_listing, name="close_listing"),
    path("auctions/<str:category_name>", views.list_by_category, name="category_name"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_wl"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_wl"),

]
