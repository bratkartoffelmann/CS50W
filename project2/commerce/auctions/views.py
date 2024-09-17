from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing, Bid, Comment, Category # import models

from .functions import categories # import sorted categories

"""
Functions important for Django Webpage
"""

def index(request):
    """
    Default page:
    Show all currently active listings

    Minimum: Each listings to display title, description, current price, and photo
    """

    # Filter active listings
    listings = Listing.objects.filter(active=True).prefetch_related('price')

    return render(request, "auctions/index.html", {
        "title": f"Active Listings",
        "listings": listings,
        "categories": categories,
    })


def login_view(request):
    """
    Login Page
    """

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    """
    Logout
    """

    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    To register account
    """

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def category(request, category_type):
    """
    Category page:
    Show all currently active listings in the category
    """

    # Get selected category
    selected_category = get_object_or_404(Category, type=category_type)

    # Filter active listings by the selected category
    listings = Listing.objects.filter(active=True, category=selected_category).prefetch_related('price')

    return render(request, "auctions/index.html", {
        "title": f"Filter category: {category_type} ({len(listings)} Active)",
        "listings": listings,
        "categories": categories,
    })


def load_listing(request, listing_id):
    """
    Load listing page
    """

    listing = get_object_or_404(Listing, id=listing_id)
    isUserInWatchlist = request.user in listing.watchlist.all()
    comments = listing.listing_comments.all()
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "categories": categories,
        "isWatchlist": isUserInWatchlist,
        "comments": comments,
    })


def create_listing(request):
    """
    GET method:
    - return create-listing.html
    - if user is not logged in, return login-html

    POST method:
    - obtain basic listing information
    - update Listing database
    - redirect to new listing page
    """

    # Check if user is authenticalted, else redirect to login
    user = request.user
    if not user.is_authenticated:
            return redirect('login')

    if request.method == "GET":

        return render(request, "auctions/create-listing.html", {
            "categories": categories,
        })
    
    else: 
        # Get data from form
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"] if request.POST["image"] != "" else "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg"
        category = request.POST["category"]

        categoryData = Category.objects.get(type=category)

        bid = Bid(float(request.POST["price"]), user=request.user)
        bid.save()

        # Create a new listing object
        new_Listing = Listing(
            title = title,
            description = description,
            image = image,
            price = bid,
            category = categoryData,
            owner = user,
        )

        # Insert the object into database
        new_Listing.save()

        # Redirect to new listing page
        return redirect('listing', listing_id=new_Listing.id)


def watchlist(request):
    """
    Obtain user watchlist
    If user not signed in, redirect to login page
    """

    # 
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    # Obtain watchlist
    watchlist = user.listing_watchlist.all()

    return render(request, "auctions/index.html", {
        "title": f"My Watchlist",
        "listings": watchlist,
        "categories": categories,
    })

def toggleWatchlist(request, listing_id):
    """
    Toggle the watchlist status of the listing.
    """

    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.user.is_authenticated:
        if request.user in listing.watchlist.all():
            listing.watchlist.remove(request.user)
        else:
            listing.watchlist.add(request.user)
    
    return redirect('listing', listing_id=listing_id)



def addComment(request, listing_id):
    """
    Add comment of user
    """

    if request.method == 'POST':
        listing = get_object_or_404(Listing, id=listing_id)
        comment_text = request.POST.get('newComment')
        
        if comment_text and request.user.is_authenticated:
            newComment = Comment(
                listing=listing, 
                user=request.user, 
                comment=comment_text
            )
            newComment.save()

    return redirect('listing', listing_id=listing_id)

def addBid(request, listing_id):
    """
    Add user bid
    """

    # Retrieve and clear messages
    storage = messages.get_messages(request)
    storage.used = set()
    
    listing = get_object_or_404(Listing, id=listing_id)
    bid_amount = request.POST['new_bid']
 
    # Check if new bid is larger than current bid
    if float(bid_amount) > float(listing.price.bid):
        updateBid = Bid(bid=float(bid_amount), user=request.user)
        updateBid.save()
        
        listing.price = updateBid
        listing.buyer = request.user
        listing.save()

        messages.success(request, "Bid is successful!")
    
    else:
        messages.error(request, "Bid amount must be more than current bid!")
    
    return redirect('listing', listing_id=listing_id)
    
def closeAuction(request, listing_id):
    """
    Allow owner to close auction
    """

    # Set listing.active to False
    listing = get_object_or_404(Listing, id=listing_id)
    listing.active = False
    listing.save()

     # Set a success message
    messages.success(request, f"Listing closed. {listing.buyer} won the auction!")

    return redirect('listing', listing_id=listing_id)