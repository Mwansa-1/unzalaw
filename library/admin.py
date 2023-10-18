from django.contrib import admin
from django.utils import timezone  # Import the timezone module
from datetime import timedelta
from .models import  Candidate, BorrowingHistory, UserRecommendation, ForumPost , Comments , Contact , Profile , CartItem


# Register your models here.

admin.site.register(Candidate)

