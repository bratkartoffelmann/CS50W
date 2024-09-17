from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # 'username', 'password', 'email' are inherited from AbstractUser
    pass

class Category(models.Model):
    type = models.CharField(max_length=50) # Define the category name

    def __str__(self):
        return self.type

class Bid(models.Model):
    bid = bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")

    def __str__(self):
        return f"{self.bid}"

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(default="")
    image = models.URLField(default="https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg")  # To store image URLs
    active = models.BooleanField(default=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_bid")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='listing_categories')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner") # Seller information
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="buyer") # Seller information

    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listing_watchlist")

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.user} commented on {self.listing}"


