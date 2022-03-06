from . import views
from django.urls import path, re_path


urlpatterns = [
    path('', views.food_booking, name='food_manager'),
    re_path('foodId=(?P<food_id>[0-9]+)', views.food_info),
    path('cancel', views.cancel_book),
    re_path('my-book/myName=(?P<my_name>.*)', views.my_book),
]
