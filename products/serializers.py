from rest_framework import serializers
from products.models import Product, Category, Review
from rest_framework.exceptions import ValidationError


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


# class ObjectCreateSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     is_active = serializers.BooleanField()


class ReviewCreateSerialiser(serializers.Serializer):
    stars = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField(max_length=50)


class ProductCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=10)
    description = serializers.CharField()
    price = serializers.FloatField()
    category = serializers.IntegerField()
    reviews = serializers.ListField(child=ReviewCreateSerialiser())

    # list_ = serializers.ListField(child=serializers.CharField())
    # object_ = ObjectCreateSerializer

    def validate_category_id(self, category_id):
        if Category.objects.filter(id=category_id).count() == 0:
            raise ValidationError(f'Category with id={category_id} not found!')
        return category_id


    # def validate(self, attrs):
    #     id = attrs['category_id']
    #     try:
    #         Category.objects.get(id=id)
    #     except Category.DoesNotExist:
    #         raise ValidationError('Category with id={id} not found!')
    #     return attrs







