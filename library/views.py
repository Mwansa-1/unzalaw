from django.shortcuts import render , redirect , get_object_or_404
from .models import Candidate , ForumPost , User , Comments , Contact , CartItem ,BorrowingHistory , Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from . import forms
from django.utils import timezone
from .forms import SearchForm
from django.db.models import Count


# Create your views here.
@login_required(login_url='/accounts/signup/')
def index(request):
    return render(request , "library/index.html",{
        "books" : Candidate.objects.all(),
        "forums" : ForumPost.objects.all()
    })


@login_required(login_url='/accounts/signup/')
def books(request):
    return render(request , "library/books.html" ,{
        "books" : Candidate.objects.all()
    })
 

###Cart Items
@login_required(login_url='/accounts/signup/')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'library/cart.html', {'cart_items': cart_items})

@login_required(login_url='/accounts/signup/')
def add_to_cart(request, book_id):
    book = Candidate.objects.get(id=book_id)
    cart_item = CartItem(user=request.user, book=book)
    cart_item.save()
    return redirect('view_cart')

@login_required(login_url='/accounts/signup/')
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

###### Borrowing books


@login_required(login_url='/accounts/signup/')
def borrow_books(request):
    cart_items = CartItem.objects.filter(user=request.user)
    current_date = timezone.now().date()
    due_date = current_date + timezone.timedelta(days=14)  # You can adjust the due date as needed.

    for cart_item in cart_items:
        book = cart_item.book
        BorrowingHistory.objects.create(user=request.user, book=book, borrowed_date=current_date, due_date=due_date)
        book.availability = False
        book.save()

    # Clear the user's cart after borrowing.
    cart_items.delete()

    return redirect('view_borrowing_history')  # You can create a view for viewing borrowing history.

###### Borrowing History
@login_required(login_url='/accounts/signup/')
def view_borrowing_history(request):
    # Retrieve the borrowing history for the current user
    borrowing_history = BorrowingHistory.objects.filter(user=request.user).order_by('-borrowed_date')

    # Render the borrowing history in a template
    return render(request, 'library/borrowing_history.html',{'borrowing_history': borrowing_history})



def results(request):
    # Query the database to get the total items borrowed for each candidate
    candidates = Candidate.objects.annotate(total_borrowed=Count('borrowinghistory'))
    
    # Pass the candidates data to the template
    return render(request, 'library/results.html', {'candidates': candidates})