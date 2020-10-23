from django.contrib import admin

# Register your models here.
from .models import Listing, WatchList,User, Bid, Coments, Category



class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ("items",)

class ListingAdmin(admin.ModelAdmin):
        filter_horizontal = ("bid",)

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("bid",)

admin.site.register(Listing, ListingAdmin)
admin.site.register(WatchList, WatchlistAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Bid)
admin.site.register(Coments)
admin.site.register(Category)
