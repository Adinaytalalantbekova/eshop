from rest_framework import serializers
from products.models import Product, Category, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # fields = 'id title price category reviews product'.split()
        fields = '__all__'

    def get_category(self, product):
        try:
            return product.category.name
        except:
            return "No category"

    def get_reviews(self, product):
        serializer = ReviewSerializer(Review.objects.filter(author__isnull=False,
                                                            product=product), many=True)
        return serializer.data


