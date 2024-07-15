import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from utils.decorators import custom_auto_schema
from .models import FoodItem, Restaurant, RestaurantReview
from rest_framework.response import Response
from rest_framework import status
    
@api_view(['GET'])
@custom_auto_schema(
    operation_description="get all restaurants",
    responses={200: 'OK'}
)
def get_restaurants(request):
    if request.method == 'GET':
        restaurants = Restaurant.objects.all()
        restaurant_data = [
            {
                'name': restaurant.name,
                'address': restaurant.address,
                'description': restaurant.description,
                'contact_info': restaurant.contact_info,
                'cafe':restaurant.cafe,
                'bakery':restaurant.bakery,
                'website': restaurant.website,
                'location': restaurant.location,
                'reviews': restaurant.reviews,
                'tags': restaurant.tags,
                'rating': restaurant.rating,
                'opening_time': restaurant.opening_time.strftime('%H:%M') if restaurant.opening_time else None,
                'closing_time': restaurant.closing_time.strftime('%H:%M') if restaurant.closing_time else None,
            }
            for restaurant in restaurants
        ]
        return JsonResponse({'restaurants': restaurant_data}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

@api_view(['POST'])
@custom_auto_schema(
    operation_description="add a new restaurant",
    responses={201: 'Created'}
)
@csrf_exempt
def create_restaurant(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        address = data.get('address')
        description = data.get('description')
        contact_info = data.get('contact_info')
        cafe = data.get('cafe')
        bakery = data.get('bakery')
        website = data.get('website')
        location = data.get('location')
        rating = data.get('rating')
        opening_time = data.get('opening_time')
        closing_time = data.get('closing_time')

        restaurant = Restaurant.objects.create(
            name=name,
            address=address,
            description=description,
            contact_info=contact_info,
            cafe=cafe,
            bakery=bakery,
            website=website,
            location=location,
            rating=rating,
            opening_time=opening_time,
            closing_time=closing_time
        )

        return JsonResponse({'message': 'Restaurant created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@api_view(['GET'])
@custom_auto_schema(
    operation_description="get all dishes",
    responses={200: 'OK'}
)
def get_fooditems(request):
    if request.method == 'GET':
        fooditems = FoodItem.objects.all()
        fooditem_data = [
            {
                'id': fooditem.id,
                'name': fooditem.name,
                'type': fooditem.type,
                'veg': fooditem.veg
            }
            for fooditem in fooditems
        ]
        return JsonResponse({'fooditems': fooditem_data}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    
@api_view(['GET'])
@custom_auto_schema(
    operation_description="get all open restaurants",
    responses={200: 'OK'}
)
def open_restaurants(request):
    if request.method == 'GET':
        current_time = datetime.now().time()
        open_restaurants = Restaurant.objects.filter(opening_time__lte=current_time, closing_time__gt=current_time, cafe=False, bakery=False)
        restaurant_data = [
            {
                'id': restaurant.restaurant_id,
                'name': restaurant.name,
                'address': restaurant.address,
                'description': restaurant.description,
                'contact_info': restaurant.contact_info,
                'website': restaurant.website,
                'cafe': restaurant.cafe,
                'bakery': restaurant.bakery,
                'location': restaurant.location,
                'rating': restaurant.rating,
                'opening_time': restaurant.opening_time.strftime('%H:%M') if restaurant.opening_time else None,
                'closing_time': restaurant.closing_time.strftime('%H:%M') if restaurant.closing_time else None
            }
            for restaurant in open_restaurants
        ]
        return JsonResponse({'fooditems': restaurant_data}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    
@api_view(['GET'])
@custom_auto_schema(
    operation_description="get all open veg restaurants",
    responses={200: 'OK'}
)
def veg_restaurants(request):
    if request.method == 'GET':
        veg_restaurants = Restaurant.objects.filter(veg=True)
        restaurant_data = [
            {
                'id': restaurant.restaurant_id,
                'name': restaurant.name,
                'address': restaurant.address,
                'description': restaurant.description,
                'contact_info': restaurant.contact_info,
                'website': restaurant.website,
                'cafe': restaurant.cafe,
                'bakery': restaurant.bakery,
                'location': restaurant.location,
                'rating': restaurant.rating,
                'opening_time': restaurant.opening_time.strftime('%H:%M') if restaurant.opening_time else None,
                'closing_time': restaurant.closing_time.strftime('%H:%M') if restaurant.closing_time else None
            }
            for restaurant in veg_restaurants
        ]
        return JsonResponse({'restaurants': restaurant_data}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    
@api_view(['GET'])
@custom_auto_schema(
    operation_description="get all open veg restaurants",
    responses={200: 'OK'}
)
def nonveg_restaurants(request):
    if request.method == 'GET':
        nonveg_restaurants = Restaurant.objects.filter(veg=False)
        restaurant_data = [
            {
                'id': restaurant.restaurant_id,
                'name': restaurant.name,
                'address': restaurant.address,
                'description': restaurant.description,
                'contact_info': restaurant.contact_info,
                'website': restaurant.website,
                'cafe': restaurant.cafe,
                'bakery': restaurant.bakery,
                'location': restaurant.location,
                'rating': restaurant.rating,
                'opening_time': restaurant.opening_time.strftime('%H:%M') if restaurant.opening_time else None,
                'closing_time': restaurant.closing_time.strftime('%H:%M') if restaurant.closing_time else None
            }
            for restaurant in nonveg_restaurants
        ]
        return JsonResponse({'restaurants': restaurant_data}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    
@api_view(['GET'])
@custom_auto_schema(
    operation_description="get all cafes",
    responses={200: 'OK'}
)
def get_cafes(request):
    if request.method == 'GET':
        cafes = Restaurant.objects.filter(cafe=True)
        restaurant_data = [
            {
                'id': restaurant.restaurant_id,
                'name': restaurant.name,
                'address': restaurant.address,
                'description': restaurant.description,
                'contact_info': restaurant.contact_info,
                'website': restaurant.website,
                'cafe': restaurant.cafe,
                'bakery': restaurant.bakery,
                'location': restaurant.location,
                'rating': restaurant.rating,
                'opening_time': restaurant.opening_time.strftime('%H:%M') if restaurant.opening_time else None,
                'closing_time': restaurant.closing_time.strftime('%H:%M') if restaurant.closing_time else None
            }
            for restaurant in cafes
        ]
        return JsonResponse({'cafes': restaurant_data}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    
@api_view(['GET'])
@custom_auto_schema(
    operation_description="get all bakeries",
    responses={200: 'OK'}
)
def get_bakeries(request):
    if request.method == 'GET':
        bakeries = Restaurant.objects.filter(bakery=True)
        restaurant_data = [
            {
                'id': restaurant.restaurant_id,
                'name': restaurant.name,
                'address': restaurant.address,
                'description': restaurant.description,
                'contact_info': restaurant.contact_info,
                'website': restaurant.website,
                'cafe': restaurant.cafe,
                'bakery': restaurant.bakery,
                'location': restaurant.location,
                'rating': restaurant.rating,
                'opening_time': restaurant.opening_time.strftime('%H:%M') if restaurant.opening_time else None,
                'closing_time': restaurant.closing_time.strftime('%H:%M') if restaurant.closing_time else None
            }
            for restaurant in bakeries
        ]
        return JsonResponse({'cafes': restaurant_data}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    
@api_view(['POST'])
@custom_auto_schema(
    operation_description="create restaurant specific review",
    responses={201: 'Created'}
)
def create_restaurantreview(request):
    if request.method == 'POST':
        data = request.data
        restaurant_id = data.get('restaurant')
        user_name = data.get('user_name')
        food_quality_rating = data.get('food_quality_rating')
        service_rating = data.get('service_rating')
        ambiance_rating = data.get('ambiance_rating')

        if None in [restaurant_id, user_name, food_quality_rating, service_rating, ambiance_rating]:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            review = RestaurantReview.objects.create(
                restaurant_id=restaurant_id,
                user_name=user_name,
                food_quality_rating=food_quality_rating,
                service_rating=service_rating,
                ambiance_rating=ambiance_rating
            )
            return Response({'message': 'Review created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@custom_auto_schema(
    operation_description="get restaurant specific review",
    responses={200: 'OK'}
)
def restaurant_reviews(request, restaurant_id):
    if request.method == 'GET':
        reviews = RestaurantReview.objects.filter(restaurant_id=restaurant_id)
        review_data = [
            {
                'user_name': review.user_name,
                'food_quality_rating': review.food_quality_rating,
                'service_rating': review.service_rating,
                'ambiance_rating': review.ambiance_rating,
                'created_at': review.created_at
            }
            for review in reviews
        ]
        return Response({'reviews': review_data})