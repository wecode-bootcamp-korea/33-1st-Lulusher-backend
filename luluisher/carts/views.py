import json, re, bcrypt, jwt
from json import JSONDecodeError

from django.http            import JsonResponse
from django.core.exceptions import MultipleObjectsReturned
from django.views           import View

from .models         import Cart
from utils           import login_decorator
from products.models import Product, ProductOption


# 담기
class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user_id    = request.user
            product_id = data['product_id']
            quantity   = data['quantity']
            color_id   = data['color_id']
            size_id    = data['size_id']
        
            if not Product.objects.filter(id=product_id).exists(): 
                return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status=400)
            if quantity < 0:
                return JsonResponse({'message' : 'QUANTITY_ERROR'}, status=400)
            
            product_option = ProductOption.objects.get(
                product_id = product_id,
                color_id   = color_id,
                size_id    = size_id
            )

            cart, created = Cart.objects.get_or_create(
                product_option_id = product_option.id,
                user           = user_id,
                defaults          = {'quantity' : quantity},
        )
            if not created:
                cart.quantity += quantity
                cart.save()
            return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_CART'}, status=400)
        # excpet JSONDecodeError:
        #     return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

# 조회
@login_decorator
def get(self, request):

    user = request.user
    if not Cart.objects.filter(user=user).exists():
        return JsonResponse({'message' : 'USER_CART_DOES_NOT_EXIST'}, status=400)

    carts = Cart.objects.filter(user=user)

    results = [{
        'cart_id' : cart.id,
        'quantity': cart.quantity,
        'price'   : cart.product.price,
        'image'   : cart.product_options_images_set.get(is_thumbnail=True).image_url
    } for cart in carts]
    return JsonResponse({'results' : results}, status=200)

# 수정 
@login_decorator
def patch(self, request):
    try:
        data = json.loads(request.body)
        cart_id    = request.GET.get('id')
        quantity   = data['quantity']

        if not Cart.objects.filter(id=cart_id).exists():
            return JsonResponse({'message' : 'INVALID_CART_ID'}, status=404)
        
        if quantity < 0:
            return JsonResponse({'message' : 'QUANTITY_ERROR'}, status=400)
        
        cart = Cart.objects.get(id=cart_id)

        cart.quantity = data['quantity']
        cart.save()
        return JsonResponse({'quantity' : cart.quantity}, status=200)

    except MultipleObjectsReturned:
        return JsonResponse({'message' : 'MULTIPLE_OBJECTS_RETURNED'}, status=400)
    except JSONDecodeError:
        return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
    except KeyError: 
        return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

# 장바구니 삭제 
@login_decorator
def delete(self,request):
    try:
        user = request.user
        cart_id = request.GET.get('id')

        if not Cart.objects.filter(id=cart_id, user=user).exists():
            return JsonResponse({'message' : 'INVALID_CART_ID'}, status=404)
        
        cart = Cart.objects.get(id=cart_id, user=user)

        cart.delete()
        return JsonResponse({'message' : 'DELETED'}, status=200)

    except MultipleObjectsReturned:
        return JsonResponse({'message' : 'MULTIPLE_OBJECTS_RETURNED'}, status=400)
    except ValueError:
        return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

