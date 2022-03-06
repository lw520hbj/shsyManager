from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import FoodInfo,FoodBooker
import time
from shsyManager.settings import MEDIA_ROOT
# Create your views here.


def index(request):
    if request.method == "GET":
        return HttpResponseRedirect('/admin/')


def food_booking(request):
    all_food_infos = FoodInfo.objects.all().filter(food_status=True).order_by("food_date")[:5]
    data_list = []
    if request.method == "GET":
        if all_food_infos.exists():
            for food_infos in all_food_infos:
                data_one = dict()
                data_one["food_id"] = food_infos.id
                data_one["food_title"] = food_infos.food_title
                data_one["food_des"] = food_infos.food_description
                data_one["food_loc"] = food_infos.food_location
                data_one["food_num"] = food_infos.food_num
                data_one["food_img_url"] = food_infos.food_img.url
                data_one["food_date"] = food_infos.food_date
                data_list.append(data_one)
            data = {
                "code": 0,
                "message": "0",
                "data_list": data_list
            }
        else:
            data = {
                "code": -1,
                "message": "no food",
                "data_list": data_list
            }
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def food_info(request, food_id):
    if request.method == "GET":
        food = {}
        food_id = int(food_id)
        food_infos = FoodInfo.objects.all().filter(food_status=True).filter(id=food_id)
        if food_infos.exists():
            food["food_id"] = food_infos[0].id
            food["food_title"] = food_infos[0].food_title
            food["food_des"] = food_infos[0].food_description
            food["food_loc"] = food_infos[0].food_location
            food["food_num"] = food_infos[0].food_num
            food["food_img_url"] = food_infos[0].food_img.url
            food["food_date"] = food_infos[0].food_date
            data = {
                "code": 0,
                "message": "0",
                "food_info": food,
            }
        else:
            data = {
                "code": -1,
                "message": "no food",
                "data_list": food
            }
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        food_id = int(food_id)
        food = FoodInfo.objects.all().get(id=food_id)
        all_booker = list(FoodBooker.objects.all().filter(food=food).values_list('name', flat=True))
        booker = request.POST.get("name")
        if booker in all_booker:
            data = {
                "code": -1,
                "message": "您已经预定过",
                "food_id": food_id
            }
        else:
            num = food.food_num
            if num == 0:
                data = {
                    "code": -1,
                    "message": "菜品量不足",
                    "food_id": food_id
                }
            else:
                food.food_num = num - 1
                food.save()
                food_booker = FoodBooker(food=food, name=booker)
                food_booker.save()
                data = {
                    "code": 0,
                    "message": "预定成功",
                    "food_id": food_id
                }
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def cancel_book(request):
    if request.method == "POST":
        booker = request.POST.get("name")
        food_id = request.POST.get("food_id")
        food = FoodInfo.objects.all().get(id=food_id)
        all_booker = list(FoodBooker.objects.all().filter(food=food).values_list('name', flat=True))
        if booker in all_booker:
            food_booker = FoodBooker.objects.all().filter(food=food, name=booker)
            food_booker.delete()
            food.food_num = food.food_num + 1
            food.save()
            data = {
                "code": 0,
                "message": "取消成功",
                "food_id": food_id
            }
        else:
            data = {
                "code": 0,
                "message": "您未预定",
                "food_id": food_id
            }
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def my_book(request, my_name):
    if request.method == "GET":
        my_book_foods = FoodBooker.objects.all().filter(name=my_name)
        if my_book_foods.exists():
            food_list = []
            for my_book_food in my_book_foods:
                food = dict()
                food['food_id'] = my_book_food.food.id
                food["food_title"] = my_book_food.food.food_title
                food["food_des"] = my_book_food.food.food_description
                food["food_loc"] = my_book_food.food.food_location
                food["food_num"] = my_book_food.food.food_num
                food["food_img_url"] = my_book_food.food.food_img.url
                food["food_date"] = my_book_food.food.food_date
                food_list.append(food)
            data = {
                "code": 0,
                "message": "0",
                "food_list": food_list
            }
        else:
            data = {
                "code": 0,
                "message": "您未预定",
                "food_list": []
            }
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})