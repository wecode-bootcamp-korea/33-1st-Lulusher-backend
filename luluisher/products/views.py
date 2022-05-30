from django.http import JsonResponse
from django.views import View

from products.models import Product, ProductOption

class ProductDetailView(View):
    def get(self, request, product_id): 
        try: 
            product = Product.objects.get(id=product_id)
            product_options = ProductOption.objects.get(id=product_options)
            total_price = str(int(product_options.options_price) + int(product.price))

            options = [{
                'option_colors': product_options.option_colors,
                'option_size'  : product_options.option_sizes,
                'option_price' : product_options.options_price
            }for product_options in ProductOption.filter(product_id=product_id)]

            result = {
                'id'                : product.id,
                'name'              : product.name,
                'price'             : total_price,
                'image_url'         : product.product_options_images,
                'options'           : options,
                'fit_materials_care': product.fit_materials_care,
                'is_new'            : product.is_new,
                'is_bestseller'     : product.is_bestseller,
                'summer_clothes'    : product.summer_clothes
            }
            return JsonResponse({'result' : result}, status=200)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_FOUND'}, status=400)
    
    