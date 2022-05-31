import json
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from utils import login_decorator
from users.models import User
from products.models import Menu, Product, OptionSize, OptionColor, ProductOption, ProductOptionImage, Activity, Review

class productListView(View):
    def get(self, request):
        try: 
            offset         = int(request.GET.get('offset', 0))
            limit          = int(request.GET.get('limit', 9))
            menu           = request.GET.get('menu', None)
            main_category  = request.GET.get('main_category', None)
            sub_category   = request.GET.get('sub_category', None)
            option_color   = request.GET.getlist('option_color', None)
            option_size    = request.GET.getlist('option_size', None)
            is_new         = request.GET.get('is_new', None)
            is_bestseller  = request.GET.get('is_bestseller', None)
            summer_clothes = request.GET.get('summer_clothes', None)
            activity       = request.GET.get('activity', None)
            
            q = Q()
            
            if menu:
                q &= Q(sub_category__main_category__menu__name=menu)
                
            if main_category:
                q &= Q(sub_category__main_category__name=main_category)
                
            if sub_category:
                q &= Q(sub_category__name=sub_category)

            if option_color:
                q &= Q(productoption__color__name__in=option_color) 
                
            if option_size:
                q &= Q(productoption__size__name__in=option_size)

            if is_new:
                q &= Q(is_new__name=is_new)
                
            if is_bestseller:
                q &= Q(is_bestseller__name=is_bestseller)

            if summer_clothes:
                q &= Q(summer_clothes__name=summer_clothes)

            if activity:
                q &= Q(activity__activity_name=activity)
                
            products = Product.objects.filter(q)[offset:limit]

            if (menu or main_category or sub_category or option_color or option_size or is_new or is_bestseller or summer_clothes or activity) == None:
                products = Product.objects.all()[offset:limit]
                
            product_list = [{
                'product_id'         : product.id,
                'name'               : product.name,
                'original_price'     : product.price,
                'is_new'             : product.is_new,
                'is_bestsellers'     : product.is_bestseller,
                'summer_clothes_shop': product.summer_clothes,
                'activities'         : [i.activity_name for i in Activity.objects.filter(products__id=product.id)],
                'product_options': [{
                    'product_options_id'   : product_options.id,
                    'color'                : OptionColor.objects.get(id = product_options.color_id).name,
                    'size'                 : OptionSize.objects.get(id = product_options.size_id).name,
                    'stock'                : product_options.stock,
                    'option_price'         : str(int(product_options.option_price)+int(product.price)),
                    'product_option_images': [i.image_url for i in ProductOptionImage.objects.filter(product_option_id=product_options.id)]
                    } for product_options in ProductOption.objects.filter(product_id=product.id)]
                } for product in products
            ]

            return JsonResponse({"content" : product_list}, status = 200)

        except Menu.DoesNotExist:
            return JsonResponse({"message" : "MENU_DOES_NOT_EXIST"}, status = 400)

class MenuListView(View) :
    def get(self, request) :
        category_list = [{
            'id'           : menu.id,
            'name'         : menu.name,
            'main_category': [{
                'id'          : main_category.id,
                'name'        : main_category.name,
                'sub_category': [{
                    'id'  : sub_category.id,
                    'name': sub_category.name
                    } for sub_category in main_category.subcategory_set.all()]
                } for main_category in menu.maincategory_set.all()]
            } for menu in Menu.objects.all().order_by('id')]
        
        return JsonResponse({'category_list':category_list}, status = 200)
    
class ReviewView(View):
    @login_decorator
    def post(self, request, product_id):
        try:
            data = json.loads(request.body)
            user = request.user

            content = data.get('content')
            rating  = data.get('rating')
            product = data.get('product_id')

            product = Product.objects.get(id = product_id)
            
            Review.objects.create(
                content = content,
                user    = user,
                rating  = rating,
                product = product,
            )

            return JsonResponse({'Message' : 'SUCCESS'}, status = 200)

        except KeyError: 
            return JsonResponse({'Message' : 'KEY_ERROR'}, status = 400)

        except Product.DoesNotExist:
            return JsonResponse({'Message' : 'PRODUCT_DOES_NOT_EXIST'}, status = 400)

    def get(self, request, product_id):
        try:
            review_list = [{
                "id"       : review.id,
                "username" : User.objects.get(id = review.user_id).name,
                "content"  : review.content,
                "rating"   : review.rating,
                "create_at": review.created_at,
                } for review in Review.objects.filter(product_id = product_id)
            ]
            return JsonResponse({'data' : review_list}, status = 200)
        
        except KeyError: 
            return JsonResponse({'Message' : 'KEY_ERROR'}, status = 400)

        except Product.DoesNotExist:
            return JsonResponse({'Message' : 'PRODUCT_DOES_NOT_EXIST'}, status = 400)
        
    @login_decorator
    def delete(self, request, product_id, review_id):
        if not Product.objects.filter(id = product_id).exists():
            return JsonResponse({'Message' : 'PRODUCT_DOES_NOT_EXIST'}, status = 404)
        
        if not Review.objects.filter(id = review_id).exists():
            return JsonResponse({'Message' : 'REVIEW_DOES_NOT_EXIST'}, status = 404)
        
        review = Review.objects.get(id = review_id)
        
        if review.user != request.user:
            return JsonResponse({'Message' : 'Invalid_User'}, status = 401)

        review.delete()
        
        return JsonResponse({'Message' : 'SUCCESS'}, status = 200)
        
    @login_decorator
    def patch(self, request, product_id, review_id):
        if not Product.objects.filter(id = product_id).exists():
            return JsonResponse({'Message' : 'PRODUCT_DOES_NOT_EXIST'}, status = 404)
        
        if not Review.objects.filter(id = review_id).exists():
            return JsonResponse({'Message' : 'REVIEW_DOES_NOT_EXIST'}, status = 404)
        
        review = Review.objects.get(id = review_id)
            
        if review.user != request.user:
            return JsonResponse({'Message' : 'Invalid_User'}, status = 401)
        
        data = json.loads(request.body)
        
        review.rating  = data['rating']
        review.content = data['content']
        review.save()
        
        return JsonResponse({'Message' : 'SUCCESS'}, status = 200)
