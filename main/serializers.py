from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, Tag, Review, Category


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'tags', "reviews"]


class ProductsReviewListSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'reviews']


class ProductsActiveTagsListSerializer(serializers.ModelSerializer):
    activeTags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title activeTags'.split()

    def get_activeTags(self, product):
        tags = Tag.objects.filter(product=product).exclude(is_active=False)
        return TagListSerializer(tags, many=True).data


class ProductCreateValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500)
    price = serializers.IntegerField()
    category = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField())

    def validate_title(self, title):
        product = Product.objects.get(title=title)
        if product.count() > 0:
            raise ValidationError('Продукт с таким именем уже существует!')
        return title

    def validate_price(self, title):
        if int() < 0:
            raise ValidationError('Всымсле отрицательное цисло!')
        return
