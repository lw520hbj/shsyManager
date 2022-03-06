from django.db import models

# Create your models here.


class FoodInfo(models.Model):
    id = models.BigAutoField(auto_created=True, null=False, primary_key=True)
    food_title = models.CharField(max_length=20, null=False, verbose_name="菜品名称")
    food_description = models.TextField(max_length=200, null=False, verbose_name="菜品描述")
    food_location = models.CharField(max_length=30, null=False, verbose_name="食堂地址")
    food_num = models.IntegerField(null=False, verbose_name="菜品数量（份）")
    food_price = models.IntegerField(null=False, default=10, verbose_name="菜品价格（/份）")
    food_img = models.ImageField(max_length=1000, null=False, upload_to="food_images", verbose_name="菜品图片")
    food_status = models.BooleanField(default=True, null=False, verbose_name="菜品是否上架")
    food_date = models.DateField(auto_now=False, auto_now_add=False, null=False, verbose_name="菜品上架日期")

    def __str__(self):
        return self.food_title + "-" + self.food_location + "-" + str(self.food_date)

    class Meta:
        verbose_name = "菜品信息"
        verbose_name_plural = "菜品信息"


class FoodBooker(models.Model):
    food = models.ForeignKey(FoodInfo, related_name="菜品预定者", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name + "-" + self.food.food_title + "-" + str(self.food.food_date)

    class Meta:
        verbose_name = "菜品预定者"
        verbose_name_plural = "菜品预定者"
