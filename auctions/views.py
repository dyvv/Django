from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from shutil import copyfile, copy2
from django.contrib.auth.decorators import login_required

from .models import User
from .models import Listing
from .models import WatchList, Bid, Coments, Category

from .forms import CommentForm, BidForm

def index(request):
    return render(request, "auctions/index.html", {

        "listings" : Listing.objects.all()



    })

@login_required
def watchlist(request):
    user = request.user
    watchlist = WatchList.objects.filter(owner=User.objects.get(username=user)).first()
    if not watchlist:
        watchlist = WatchList (owner=User.objects.get(username=user))
        watchlist.save()
    return render(request, "auctions/watchlist.html", {

                "watchlist" : watchlist.items.all()

            })

@login_required
def create_listing(request):
    if request.method == "POST":
        listing_owner=request.user
        listing_title = request.POST["title"]
        listing_desc = request.POST["description"]
        listing_bid = request.POST["bid"]
        listing_pic = request.POST["picture"]
        listing_category = request.POST["category"]
        category=Category.objects.filter(name = listing_category).first()
        if not category:
            category = Category (name = listing_category)
            category.save()
        listing = Listing (title = listing_title, description = listing_desc, picture_url= listing_pic, createdby=listing_owner, category=category)
        listing.save()
        user=User.objects.get(username=listing_owner)
        bid= Bid (bid = listing_bid)
        bid.save()
        bid.listing_bid.add(listing)
        bid.user_bid.add(user)


    return render (request, "auctions/create.html")


def listing (request, listing_id):
    form = CommentForm()
    b_form = BidForm()

    user = request.user
    is_not_enough=False
    current_user_is_winner=False
    listing = Listing.objects.get(pk=listing_id)
    bids=listing.bid.all()
    max_old_bid=bids.order_by('-bid')[0].bid
    is_active=True

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            print(f"Your comment is :{comment}")
            listing_comment = Coments(text = comment, listing = listing, createdby = user)
            listing_comment.save()
        b_form = BidForm(request.POST)
        if b_form.is_valid():
            new_bid = b_form.cleaned_data['bid']
            listing = Listing.objects.get(pk=listing_id)
            user = request.user
            bids=listing.bid.all()
            message=None
            if int(new_bid) > int(max_old_bid):
                newbid= Bid (bid = new_bid)
                newbid.save()
                newbid.listing_bid.add(listing)
                newbid.user_bid.add(user)
            elif int(new_bid) < int(max_old_bid):
                is_not_enough=True

    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    if user.is_authenticated:
        watchlist = WatchList.objects.filter(owner=User.objects.get(username=user)).first()
        if not watchlist:
            watchlist = WatchList (owner=User.objects.get(username=user))
            watchlist.save()
        is_listing_in_watchlist = watchlist.items.filter(title = listing.title)

        if listing.createdby == user:
            is_owner=True
        else:
            is_owner=False


        if listing.winner == user.username and listing.is_active == False:
                current_user_is_winner='True'
    else:
        is_listing_in_watchlist = None
        is_owner = False


    return render (request, "auctions/listing.html", {

        "comment_form": form,
        "bid_form": b_form,
        "is_listing_in_watchlist": is_listing_in_watchlist,
        "listing": listing,
        "is_not_enough": is_not_enough,
        "max_bid": max_old_bid,
        "bids_count": Bid.objects.filter(listing_bid__title=listing.title).count(),
        "is_owner": is_owner,
        "current_user_is_winner": current_user_is_winner,
        "comments": Coments.objects.filter(listing__title = listing.title),
        "bid_already_placed": Bid.objects.filter(user_bid__username=user).filter(listing_bid__title=listing.title).first(),
        "starting_bid": Bid.objects.filter(user_bid__username=listing.createdby).filter(listing_bid__title=listing.title).first().bid

        } )

@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_active = False
    bids=listing.bid.all()
    max_bid=bids.order_by('-bid')[0]
    winner=max_bid.user_bid.first().username
    listing.winner=winner
    listing.save()
    return HttpResponseRedirect (reverse("index"))

@login_required
def add_watchlist (request, listing_id):
    listing=Listing.objects.get(pk=listing_id)
    user = request.user
    watchlist = WatchList.objects.get(owner=User.objects.get(username=user))
    is_listing_in_watchlist = watchlist.items.filter(title = listing.title)
    if watchlist and not is_listing_in_watchlist:
        watchlist.items.add(listing)
    else:
        watchlist = WatchList (owner=User.objects.get(username=user))
        watchlist.save()
        watchlist.items.add(listing)
    return HttpResponseRedirect(reverse("listing", args=[listing.id]))

@login_required
def remove_watchlist (request, listing_id):
    listing=Listing.objects.get(pk=listing_id)
    user = request.user
    watchlist = WatchList.objects.get(owner=User.objects.get(username=user))
    is_listing_in_watchlist = watchlist.items.filter(title = listing.title)
    if watchlist and is_listing_in_watchlist:
        watchlist.items.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))
    else :
        return HttpResponse ("No listing {listing.title} was found")
    

def category(request):
    category = Category.objects.all()
    return render (request, "auctions/category.html", {

        "categories": category

       })




def list_by_category (request, category_name):
    listing_by_category=Listing.objects.filter(category=Category.objects.get(name=category_name).id)
    return render (request, "auctions/category_items.html", {

        "listing_by_category": listing_by_category

        })

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
