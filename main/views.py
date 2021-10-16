from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import Product, Category, ConfirmCode
# Create your views here.


@api_view(['GET', 'POST'])
def product_list_view(request):
    product = Product.objects.all()
    data = ProductListSerializer(product, many=True).data
    return Response(data=data)


@api_view(['GET', 'PUT', 'DELETE'])
def products_item_view(request, pk):
    try:
        products = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(data={'message': "Product not Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        products.delete()
        return Response(data={'massage': 'Product removed!!!'})
    elif request.method == 'PUT':
        serializer = ProductCreateValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                "massage": "error",
                "errors": serializer.errors
            }, status=status.HTTP_404_NOT_FOUND)
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category = Category.objects.get(id=request.data.get('category'))
        product = Product.objects.create(title=title, description=description, price=price, category=category)
        product.tags.set(request.data['tags'])

        products.save()
        return Response(data={'massage': 'Product updated',
                              'products': ProductListSerializer(product).data})
    products = Product.objects.all()
    data = ProductListSerializer(products, many=False).data
    return Response(data=data)


@api_view(['GET', 'POST'])
def reviews_list_view(request):
    products = Product.objects.all()
    data = ProductsReviewListSerializer(products, many=True).data
    return Response(data=data)


@api_view(['GET', 'POST'])
def active_tags_list_view(request):
    products = Product.objects.all()
    data = ProductsActiveTagsListSerializer(products, many=True).data
    return Response(data=data)


@api_view(['GET', 'POST'])
def categories_list_view(request):
    category = Category.objects.all()
    data = CategoryListSerializer(category).data

    return data


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response(data={
                'token': token.key
            })
        else:
            return Response(data={
                'message': 'User not found!!!'
            }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = User.objects.create_user(username=username,
                                        email=username,
                                        password=password,
                                        is_active=False)
        # ConfirmCode.objects.create(user=user, code='asdfasd',
        #                            valid_until='')
        # send_to_email(email, code)
        return Response(data={'message': 'User created'})
