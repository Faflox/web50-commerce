from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# class for categories
class Category(models.Model):
    categoryName=models.CharField(max_length=100)
    def __str__(self):
        return self.categoryName
    
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    price = models.FloatField(default=0)
    def __str__(self):
        return str(self.price)


#class for listings with a foreign key from Category
class Listing(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=500, blank=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    def __str__(self):
        return self.title
    
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentUser")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=500)
    def __str__(self):
        return self.text
    
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourites")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="favourites")