from django.http import JsonResponse
from django.views import View

from products.models import Menu

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