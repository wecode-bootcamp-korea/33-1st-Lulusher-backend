import json
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View
from django.db.models import Q, Avg

from utils import login_decorator
from products.models import Menu, Product, Review

class MenuListView(View):
    def get(self, request):
        menus = Menu.objects.all() \
            .prefetch_related('maincategory_set', 'maincategory_set__subcategory_set') \
            .order_by('id')

        results = [{
            'id'           : menu.id,
            'name'         : menu.name,
            'main_categories': [{
                'id'          : main_category.id,
                'name'        : main_category.name,
                'sub_categories': [{
                    'id'  : sub_category.id,
                    'name': sub_category.name
                    } for sub_category in main_category.subcategory_set.all()]
                } for main_category in menu.maincategory_set.all()]
            } for menu in menus]

        return JsonResponse({'results' : results}, status = 200) 

class ProductListView(View):
    def get(self, request):
        offset         = int(request.GET.get('offset',0))
        limit          = int(request.GET.get('limit',9))
        sort           = request.GET.get('sort','id')
        menu           = request.GET.get('menu')
        main_category  = request.GET.get('main_category')
        sub_category   = request.GET.getlist('sub_category')
        color          = request.GET.getlist('color')
        size           = request.GET.getlist('size')
        is_new         = request.GET.get('is_new')
        is_bestseller  = request.GET.get('is_bestseller')
        summer_clothes = request.GET.get('summer_clothes')
        activity       = request.GET.getlist('activity')
        search         = request.GET.get('search')
        
        q = Q()
        
        if menu:
            q &= Q(sub_category__main_category__menu__name=menu)
            
        if main_category:
            q &= Q(sub_category__main_category__name=main_category)
            
        if sub_category:
            q &= Q(sub_category__name__in=sub_category)

        if color:
            q &= Q(productoption__color__name__in=color)
            
        if size:
            q &= Q(productoption__size__name__in=size)

        if is_new:
            q &= Q(is_new__name=is_new)
            
        if is_bestseller:
            q &= Q(is_bestseller__in=is_bestseller)

        if summer_clothes:
            q &= Q(summer_clothes__in=summer_clothes)

        if activity:
            q &= Q(activity__activity_name__in=activity)
            
        if search:
            q &= Q(name__icontains=search)

        sort_set = {
            "id"    : "id",
            "name"  : "name",
            "price" : "price",
            "-price": "-price"
        }
        
        products = Product.objects.filter(q).distinct().order_by(sort_set[sort])[offset:offset+limit]
            
        results = [{
            'product_id'         : product.id,
            'name'               : product.name,
            'original_price'     : int(product.price),
            'is_new'             : product.is_new,
            'is_bestsellers'     : product.is_bestseller,
            'summer_clothes_shop': product.summer_clothes,
            'activities'         : [activity.activity_name for activity in product.activity_set.all()],
            'product_options': [{
                'product_options_id'   : product_option.id, 
                'color'                : product_option.color.name,
                'size'                 : product_option.size.name,
                'stock'                : product_option.stock,
                'option_price'         : int(product_option.option_price)+int(product.price),
                'product_option_images': [image.image_url for image in product_option.productoptionimage_set.all()]
                } for product_option in product.productoption_set.all()]
            } for product in products
        ]

        return JsonResponse({"results" : results}, status = 200)

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id = product_id).exists():
            return JsonResponse({'Message' : 'PRODUCT_DOES_NOT_EXIST'}, status = 404)

        results = [{
            'menu'               : product.sub_category.main_category.menu.name,
            'main_category'      : product.sub_category.main_category.name,
            'sub_category'       : product.sub_category.name,
            'id'                 : product.id,
            'name'               : product.name,
            'original_price'     : product.price,
            'is_new'             : product.is_new,
            'is_bestsellers'     : product.is_bestseller,
            'summer_clothes_shop': product.summer_clothes,
            'activities'         : [activity.activity_name for activity in product.activity_set.all()],
            'product_options': [{
                'product_options_id'   : product_option.id, 
                'color'                : product_option.color.name,
                'size'                 : product_option.size.name,
                'stock'                : product_option.stock,
                'option_price'         : str(int(product_option.option_price)+int(product.price)),
                'product_option_images': [image.image_url for image in product_option.productoptionimage_set.all()]
                } for product_option in product.productoption_set.all()]
            }for product in Product.objects.filter(id = product_id)]

        return JsonResponse({"results" : results}, status = 200)

class ReviewView(View):
    @login_decorator
    def post(self, request, product_id):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = data['content']
            rating  = data['rating']

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
            return JsonResponse({'Message' : 'PRODUCT_DOES_NOT_EXIST'}, status = 404)

    def get(self, request, product_id):
        offset = int(request.GET.get('offset',0))
        limit  = int(request.GET.get('limit',3))
        review_list = [{
            "id"       : review.id,
            "username" : review.user.name,
            "content"  : review.content,
            "rating"   : review.rating,
            "create_at": review.created_at,
            } for review in Review.objects.filter(product_id = product_id)[offset:offset+limit]
        ]
        review_count = Review.objects.filter(product_id = product_id).count()
        rating_average = Review.objects.filter(product_id = product_id).aggregate(Avg('rating'))

        return JsonResponse({'data' : review_list,'review_count' : review_count,'rating_average' : rating_average}, status = 200)
        
    @login_decorator
    def delete(self, request, product_id, review_id):
        Review.objects.filter(id = review_id, user_id = request.user.id).delete()
        return JsonResponse({'Message' : 'NO_CONTENT'}, status = 200)
        
    @login_decorator
    def patch(self, request, product_id, review_id):
        if not Review.objects.filter(id = review_id, user_id = request.user.id).exists():
            return JsonResponse({'Message' : 'REVIEW_DOES_NOT_EXIST'}, status = 404)
        
        data   = json.loads(request.body)
        review = Review.objects.get(id = review_id, user_id = request.user.id)
        
        review.rating  = data['rating'] if data['rating'] else review.rating
        review.content = data['content'] if data['content'] else review.content
        review.save()
        
        return JsonResponse({'Message' : 'SUCCESS'}, status = 200)