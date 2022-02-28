from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.serializers import ProductSerializers, ProductCreateUpdateSerializer
from products.models import Product, Review


@api_view(['GET'])
def test(request):
    contex = {
        'integer': 160,
        'string': "Hello World",
        'boolean': True,
        'list': [
            1, 2, 3
        ]
    }
    return Response(data=contex)


@api_view(["GET", "POST"])
def product_list_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductSerializers(products, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ProductCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        product = Product.objects.create(title=title, description=description,
                                         price=price, category_id=category_id)
        for i in request.data.get('reviews', []):
            Review.objects.create(
                stars=i['stars'],
                text=i['text'],
                product=product
            )
        return Response(data=ProductSerializers(product).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detaile_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=404, data={'massage': 'Product not found'})
    if request.method == 'GET':
        data = ProductSerializers(product).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        product.save()
        return Response(data=ProductSerializers(product).data)



