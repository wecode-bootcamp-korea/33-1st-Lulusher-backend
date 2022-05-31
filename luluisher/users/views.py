# Create your views here.

import json, re, bcrypt, jwt
from json import JSONDecodeError

from django.http            import JsonResponse
from django.core.exceptions import MultipleObjectsReturned
from django.views           import View
from django.conf            import settings

from .models         import User, Cart
from utils           import login_decorator
from products.models import Product

class SignUpView(View):
    def post(self, request): 
        try: 
            input_data     = json.loads(request.body)
            email          = input_data['email']
            EMAIL_REGEX    = r"^[a-zA-Z0-9_-]+@[a-z]+.[a-z]+$"
            PASSWORD_REGEX = r"^(?=.{8,16}$)(?=.*[a-z])(?=.*[0-9]).*$"
            password       = input_data['password']
          
            if User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "THE_USER_EMAIL_ALREADY_EXISTS"}, status=400)

            if not re.match(EMAIL_REGEX, email):
                return JsonResponse({"message" : "INVALID_EMAIL_--_NEEDS_@_AND_."}, status=400)
         
            if not re.match(PASSWORD_REGEX, password):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")

            User.objects.create(
                name            = input_data['name'],
                email           = email,
                password        = hashed_password,
                mobile_number   = input_data['mobile_number'],
                address         = input_data['address'],
                email_subscribe = input_data['email_subscribe']
            ) 
            return JsonResponse({"messsage" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "Key_Error"}, status=400)
    
class SignInView(View):
    def post(self,request):
        try:
            input_data = json.loads(request.body)

            email    = input_data['email']
            password = input_data['password']
            user     = User.objects.get(email = email)

            if bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8)')):
                token = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
                return JsonResponse({'message' : "success", 'token' : token}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'Invalid Email'}, status = 400)

# 담기
class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            input_data = json.loads(request.body)
            user_id    = request.user
            product_id = input_data['product_id']
            image_url  = input_data['image_url']
            quantity   = input_data['quantity']
        
            if not Product.objects.filter(id=product_id).exists(): 
                return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status=400)
            if quantity <= 0:
                return JsonResponse({'message' : 'QUANTITY_ERROR'}, status=400)
        
            cart = Cart.objects.get_or_create(
                product_id = product_id,
                image_url  = image_url,
                user_id    = user_id
        )

            cart.quantity += quantity
            cart.save()
            return JsonResponse({'message' : 'SUCCESS'}, stauts=201)

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

    result = [{
        'cart_id' : cart.id,
        'quantity': cart.quantity,
        'price'   : cart.product.price,
        'image'   : cart.product_options_images_set.get(is_thumbnail=True).image_url
    } for cart in carts]
    return JsonResponse({'result' : result}, status=200)

# 수정 
# @login_decorator
def patch(self, request):
    try:
        input_data = json.loads(request.body)
        cart_id    = request.GET.get('id')
        quantity   = input_data['quantity']

        if not Cart.objects.filter(id=cart_id).exists():
            return JsonResponse({'message' : 'INVALID_CART_ID'}, status=404)
        
        if quantity <= 0:
            return JsonResponse({'message' : 'QUANTITY_ERROR'}, status=400)
        
        cart = Cart.objects.get(id=cart_id)

        cart.quantity = input_data['qunatity']
        cart.save()
        return JsonResponse({'quantity' : cart.quantity}, status=200)

    except MultipleObjectsReturned:
        return JsonResponse({'message' : 'MULTIPLE_OBJECTS_RETURNED'}, status=400)
    except JSONDecodeError:
        return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
    except KeyError: 
        return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

# 장바구니 삭제 
# @login_decorator
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

