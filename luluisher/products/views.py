from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from products.models import Menu, Product, OptionSize, OptionColor, ProductOption, ProductOptionImage, Activity

class productListView(View):
    def get(self, request):
        try:
            main_category  = request.GET.get('main_category', None)
            sub_category   = request.GET.get('sub_category', None)
            option_color   = request.GET.getlist('option_color', None)
            option_size    = request.GET.getlist('option_size', None)
            is_new         = request.GET.get('is_new', None)
            is_bestseller  = request.GET.get('is_bestseller', None)
            summer_clothes = request.GET.get('summer_clothes', None)
            
            q = Q()

            if main_category:
                q &= Q(sub_category__main_category__in=main_category)
                
            if sub_category:
                q &= Q(sub_category__in=sub_category)

            if option_color:
                q &= Q(productoption__color__in=option_color) 
                
            if option_size:
                q &= Q(productoption__size__in=option_size)

            if is_new:
                q &= Q(is_new__in=is_new)
                
            if is_bestseller:
                q &= Q(is_bestseller__in=is_bestseller)

            if summer_clothes:
                q &= Q(summer_clothes__in=summer_clothes)
                
            products = Product.objects.filter(q)

            if (sub_category or option_color or option_size or is_new or is_bestseller or summer_clothes) == None:
                products = Product.objects.all()
                
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
                }for product in products
            ]

            return JsonResponse({"content" : product_list}, status = 200)

        except Menu.DoesNotExist:
            return JsonResponse({"message" : "MENU_DOES_NOT_EXIST"}, status = 400)
