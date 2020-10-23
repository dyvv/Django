from django.contrib.auth.models import AbstractUser
from django.db import models


class Category (models.Model):
    name = models.CharField(max_length=64, unique = 'True', blank = 'True')
    def __str__(self):
        return f"{self.name}"


class Bid (models.Model):
    bid = models.IntegerField()


    def __str__(self):
        return f"Title: {self.bid}"

class User(AbstractUser):
    #pass
    bid = models.ManyToManyField(Bid, related_name="user_bid")

    def __str__(self):
        return f"{self.username}"

class Listing (models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    createdby=models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner")
    bid=models.ManyToManyField(Bid, related_name="listing_bid")
    picture_url=models.URLField(max_length=64, blank='True')
    is_active = models.BooleanField(default=True)
    winner= models.CharField(max_length=64, blank='True')
    category = models.ForeignKey(Category, related_name = "listing_category", on_delete=models.SET_NULL, null='True')

    def __str__(self):
        return f"Title: {self.title}"


class Coments (models.Model):
    text = models.CharField(max_length=64)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment")
    createdby=models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_owner")

    def __str__(self):
        return f"{self.text}"



class WatchList (models.Model):
    items = models.ManyToManyField(Listing, blank=True, related_name="saved_items")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list_owner", blank=True)

    def __str__(self):
        return f"WatchList Owner: {self.owner}"
