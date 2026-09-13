from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate


import logging
import json

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)

    data = {"userName": username}

    if user is not None:
        login(request, user)
        data = {
            "userName": username,
            "status": "Authenticated"
        }

    return JsonResponse(data)


# logout request
def logout_request(request):
    logout(request)
    return HttpResponseRedirect("/")


# registration request
@csrf_exempt
def registration(request):

    data = json.loads(request.body)

    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exists = User.objects.filter(username=username).exists()

    if username_exists:
        return JsonResponse({
            "userName": username,
            "error": "Already Registered"
        })

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    login(request, user)

    return JsonResponse({
        "userName": username,
        "status": "Authenticated"
    })


# dealership list
def get_dealerships(request):
    return render(request, "Home.html")


# dealer reviews
def get_dealer_reviews(request, dealer_id):
    return render(
        request,
        "Home.html",
        {"dealer_id": dealer_id}
    )


# dealer details
def get_dealer_details(request, dealer_id):
    return JsonResponse(
        {"dealer_id": dealer_id}
    )


# add review
def add_review(request):
    return render(request, "Home.html")


# get cars
def get_cars(request):

    count = CarMake.objects.filter().count()

    print(count)

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')

    cars = []

    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})