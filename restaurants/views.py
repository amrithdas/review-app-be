import datetime
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
import json
from django.db.models import Count

from .serializers import RestaurantReviewSerializer
from geopy.distance import distance
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage
from utils.decorators import custom_auto_schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from django.db import connection
from .models import FoodItem, Restaurant, RestaurantReview
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
    
@api_view(['GET'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([AllowAny])
@csrf_exempt
def get_restaurants(request):
    page = request.GET.get('page', 1)
    page_size = 10
    sort_by = request.GET.get('sort_by', 'recommended')
    user_lat = float(request.GET.get('lat', 0))
    user_lng = float(request.GET.get('lng', 0))
    
    categories = request.GET.get('category', '')
    categories_list = categories.split(",") if categories else []
    
    restaurants = Restaurant.objects.all()
    
    if categories_list:
        query = Q()
        for category in categories_list:
            query |= Q(tags__icontains=category)
        restaurants = restaurants.filter(query)
    
    if sort_by == 'nearest' and user_lat and user_lng:
        def calculate_distance(restaurant):
            restaurant_lat, restaurant_lng = map(float, restaurant.location.split(','))
            return distance((user_lat, user_lng), (restaurant_lat, restaurant_lng)).km
        restaurants = sorted(restaurants, key=calculate_distance)
    elif sort_by == 'rating':
        restaurants = restaurants.order_by('-rating')

    paginator = Paginator(restaurants, page_size)
    
    try:
        page_obj = paginator.page(page)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    restaurant_data = [
        {
            'name': restaurant.name,
            'address': restaurant.address,
            'description': restaurant.description,
            'contact_info': restaurant.contact_info,
            'website': restaurant.website,
            'location': restaurant.location,
            'reviews': restaurant.reviews,
            'tags': restaurant.tags,
            'rating': restaurant.rating,
            'opening_time': restaurant.opening_time.strftime('%H:%M') if restaurant.opening_time else None,
            'closing_time': restaurant.closing_time.strftime('%H:%M') if restaurant.closing_time else None,
            'image_urls': restaurant.image_urls,
        }
        for restaurant in page_obj.object_list
    ]

    return JsonResponse({
        'restaurants': restaurant_data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    }, status=200)

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
        open_restaurants = Restaurant.objects.filter(opening_time__lte=current_time, closing_time__gt=current_time)
        restaurant_data = [
            {
                'id': restaurant.restaurant_id,
                'name': restaurant.name,
                'address': restaurant.address,
                'description': restaurant.description,
                'contact_info': restaurant.contact_info,
                'website': restaurant.website,
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
    
@api_view(['POST'])
@custom_auto_schema(
    operation_description="create restaurant specific review",
    responses={201: 'Created'}
)
def create_restaurantreview(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        restaurant_name = data.get('restaurant_name')
        rating = data.get('rating')
        description = data.get('description', '')

        if None in [restaurant_name, rating]:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            review = RestaurantReview.objects.create(
                restaurant_name=restaurant_name,
                user_name=request.user.name,
                rating=rating,
                description=description
            )
            return Response({'message': 'Review created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Get reviews for a specific restaurant",
    responses={
        200: openapi.Response('Success', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'reviews': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'user_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'rating': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                            'restaurant_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME)
                        }
                    )
                )
            }
        )),
        404: 'Not Found'
    }
)
def restaurant_reviews(request, restaurant_name):
    if request.method == 'GET':
        reviews = RestaurantReview.objects.filter(restaurant_name=restaurant_name).order_by('-created_at')[:10]
        review_data = [
            {
                'user_name': review.user_name,
                'rating': review.rating,
                'description': review.description,
                'restaurant_name': review.restaurant_name,
                'created_at': review.created_at.isoformat()
            }
            for review in reviews
        ]
        return Response({'reviews': review_data})

@api_view(['GET'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([AllowAny])
@csrf_exempt
@custom_auto_schema(
    operation_description="Restaurant list based on search",
    responses={200: 'OK'}
)
def search_restaurants(request):
    if request.method == 'GET':
        search_term = request.GET.get('search', '')
        if search_term:
            businesses = Restaurant.objects.filter(
                Q(name__icontains=search_term)
            )
        else:
            businesses = Restaurant.objects.all()

        businesses_list = list(businesses.values('restaurant_id','name', 'address'))
        return Response(businesses_list)
    
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Get the latest reviews with pagination",
    responses={
        200: openapi.Response('Success', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'reviews': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'restaurant_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                            'user_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'rating': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME)
                        }
                    )
                )
            }
        )),
        404: 'Not Found'
    }
)
def recent_reviews(request):
    page = int(request.GET.get('page', 1))
    page_size = 12
    start = (page - 1) * page_size
    end = start + page_size
    
    reviews = RestaurantReview.objects.order_by('-created_at')[start:end]
    review_data = [
        {
            'restaurant_name': review.restaurant_name,
            'description': review.description,
            'user_name': review.user_name,
            'rating': review.rating,
            'created_at': review.created_at
        }
        for review in reviews
    ]
    return Response({'reviews': review_data})

@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Get details of a specific restaurant",
    responses={
        200: openapi.Response('Success', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'restaurant': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'restaurant_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'address': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'contact_info': openapi.Schema(type=openapi.TYPE_STRING),
                        'website': openapi.Schema(type=openapi.TYPE_STRING),
                        'location': openapi.Schema(type=openapi.TYPE_STRING),
                        'rating': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'closing_time': openapi.Schema(type=openapi.TYPE_STRING),
                        'opening_time': openapi.Schema(type=openapi.TYPE_STRING),
                        'reviews': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'tags': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'image_urls': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                    }
                )
            }
        )),
        404: 'Not Found'
    }
)
def restaurant_details(request, restaurant_name):
    try:
        restaurant = Restaurant.objects.get(name=restaurant_name)
        restaurant_data = {
            'restaurant_id': restaurant.restaurant_id,
            'name': restaurant.name,
            'address': restaurant.address,
            'description': restaurant.description,
            'contact_info': restaurant.contact_info,
            'website': restaurant.website,
            'location': restaurant.location,
            'rating': restaurant.rating,
            'closing_time': restaurant.closing_time,
            'opening_time': restaurant.opening_time,
            'reviews': restaurant.reviews,
            'tags': restaurant.tags,
            'image_urls': restaurant.image_urls,
        }
        return Response({'restaurant': restaurant_data}, status=200)
    except Restaurant.DoesNotExist:
        return Response({'error': 'Restaurant not found'}, status=404)
    
@api_view(['GET'])
@swagger_auto_schema(
    operation_description="Get count of reviews for a specific restaurant",
    responses={
        200: openapi.Response('Success', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'review_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Total number of reviews for the restaurant")
            }
        )),
        404: 'Not Found'
    }
)
def review_count(request, restaurant_name):
    try:
        review_count = RestaurantReview.objects.filter(restaurant_name=restaurant_name).count()
        return Response({'review_count': review_count}, status=status.HTTP_200_OK)
    except RestaurantReview.DoesNotExist:
        return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def rating_counts(request, restaurant_name):
    rating_counts = RestaurantReview.objects.filter(restaurant_name=restaurant_name).values('rating').annotate(count=Count('rating')).order_by('rating')

    counts_dict = {i: 0 for i in range(1, 6)}
    for entry in rating_counts:
        counts_dict[entry['rating']] = entry['count']

    return JsonResponse(counts_dict)

class ReviewPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100
    
@api_view(['GET'])
def recent_reviews_by_restaurant(request, restaurant_name):
    try:
        reviews = RestaurantReview.objects.filter(restaurant_name=restaurant_name).order_by('-created_at')
        paginator = ReviewPagination()
        result_page = paginator.paginate_queryset(reviews, request)
        serializer = RestaurantReviewSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except RestaurantReview.DoesNotExist:
        return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_distinct_tags(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT ON (LOWER(unnested_tag)) unnested_tag
                FROM (
                    SELECT UNNEST(tags) AS unnested_tag
                    FROM public.restaurants_restaurant
                ) AS subquery
                ORDER BY LOWER(unnested_tag), unnested_tag;
            """)
            tags = cursor.fetchall()
        
        distinct_tags = [tag[0] for tag in tags]

        return Response({'distinct_tags': distinct_tags}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_user_reviews_count(request):
    user = request.user
    review_count = RestaurantReview.objects.filter(user_name=user).count()
    return Response({'review_count': review_count})

@login_required
@api_view(['GET'])
def get_user_reviews(request):
    user_reviews = RestaurantReview.objects.filter(user_name=request.user).order_by('-id')
    serializer = RestaurantReviewSerializer(user_reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@login_required
@api_view(['PUT', 'DELETE'])
def reviews_edit(request, id):
    review = get_object_or_404(RestaurantReview, id=id, user_name=request.user)

    if request.method == 'PUT':
        new_content = request.data.get('content', '')
        review.description = new_content
        review.save()
        return Response({'message': 'Review updated successfully'}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        review.delete()
        return Response({'message': 'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)