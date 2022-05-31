from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from products.models import Menu

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
