from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Bid, Category


def index(request):
    listings = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories
        })
    
def watchlist(request):
    User = request.user
    listings = User.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def removeFromWatchlist(request, listing_id):
    listingData = Listing.objects.get(id=listing_id)
    User = request.user
    listingData.watchlist.remove(User)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def addToWatchlist(request, listing_id):
    listingData = Listing.objects.get(id=listing_id)
    User = request.user
    listingData.watchlist.add(User)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

    
def categories(request):
    if request.method == "POST":
        chosenCategory = request.POST["category"]
        if chosenCategory == "All":
            return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(active=True),
            "categories": Category.objects.all()
            })
        else:
            category = Category.objects.get(categoryName=chosenCategory)
            listings = Listing.objects.filter(active=True, category=category)
            categories = Category.objects.all()
            return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories
            })
        
def listing(request, listing_id):
    listingInfo = Listing.objects.get(id=listing_id)
    ListingInWatchlist = request.user in listingInfo.watchlist.all()
    listingComments = Comment.objects.filter(listing = listingInfo)
    return render(request, "auctions/listing.html", {
        "listing": listingInfo,
        "ListingInWatchlist": ListingInWatchlist,
        "listingComments": listingComments
    })
    
def addComment(request, listing_id):
    currentUser = request.user
    listingData = Listing.objects.get(id=listing_id)
    text = request.POST["text"]
    
    newComment = Comment(
        user=currentUser, 
        listing=listingData, 
        text=text)
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def login_view(request):
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
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
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
    
def create(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    elif request.method =="POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.POST.get("image")
        starting_price = request.POST.get("starting_price")
        category_name=request.POST.get("category")
        category = Category.objects.get(categoryName = category_name)
        user = request.user
        
        #creating a bid object
        bid = Bid(price = float(starting_price), user = user)
        bid.save()
        
        listing = Listing(
            title=title, 
            description=description, 
            image=image, 
            price=bid,
            category=category,
            user=user)
        listing.save()
        
    return render(request, "auctions/create.html")

def placeBid(request, listing_id):
    if request.method=="POST":
        newBid = float(request.POST.get("newBid"))
        listingData = Listing.objects.get(id=listing_id)
        oldBid = float(listingData.price.price)
        if newBid >= oldBid:
            updateBid = Bid(price = float(newBid), user = request.user)
            updateBid.save()
            listingData.price = updateBid
            listingData.save()
            return render(request, "auctions/listing.html", {
                "listing": listingData,
                "message": "Bid placed successfully",
                "updateBid": True
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listingData,
                "message": "Bid must be higher than current bid",
                "updateBid": False
            })
            
def endAuction(request, listing_id):
    listingData = Listing.objects.get(id=listing_id)
    listingData.active = False
    listingData.save()
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "message": "Auction ended successfully"
    })
    