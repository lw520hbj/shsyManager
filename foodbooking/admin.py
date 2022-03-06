from django.contrib import admin
from .models import FoodInfo,FoodBooker
from django.utils.safestring import mark_safe
# Register your models here.


class FoodInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_filter = ('food_title', 'food_date', 'food_status')
    list_display = ('food_title', 'food_description', 'food_location', 'food_num', 'food_price',
                    'Preview', 'food_status', 'food_date')
    list_editable = ('food_status', 'food_date', )
    def Preview(self, obj):
        return mark_safe('<img src="%s" height="64" width="64" />' % (obj.food_img.url))
    Preview.allow_tags = True
    Preview.short_description = "菜品图片"
    ordering = ('food_date', )


class FoodBookerAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_filter = ('food', )


admin.site.register(FoodInfo, FoodInfoAdmin)
admin.site.register(FoodBooker, FoodBookerAdmin)
admin.AdminSite.site_header = '上海石油管理后台'
admin.AdminSite.site_title = '上海石油管理后台'
