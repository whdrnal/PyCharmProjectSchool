from django.db import models


from markets.models import Market


class Product(models.Model):
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    is_deleted = models.BooleanField('삭제여부', default=False)
    delete_date = models.DateTimeField('삭제날짜', null=True, blank=True)
    market = models.ForeignKey(Market, on_delete=models.DO_NOTHING)
    name = models.CharField('상품명(내부용)', max_length=100)
    display_name = models.CharField('상품명(고객용)', max_length=100)
    price = models.PositiveIntegerField('권장판매가')
    sale_price = models.PositiveIntegerField('실제판매가')
    is_hidden = models.BooleanField('노출여부', default=False)
    is_sold_out = models.BooleanField('품절여부', default=False)
    category_id = models.PositiveIntegerField('카테고리번호(추후설계)', default=0)
    hit_count = models.PositiveIntegerField('조회수', default=0)
    review_count = models.PositiveIntegerField('리뷰수', default=0)
    review_point = models.PositiveIntegerField('리뷰평점', default=0)

    def __str__(self):
        return self.display_name


class ProductReal(models.Model):
    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option_1_type = models.CharField('옵션1 타입', max_length=10, default='SIZE')
    option_1_name = models.CharField('옵션1 이름(내부용)', max_length=50)
    option_1_display_name = models.CharField('옵션1 이름(고객용)', max_length=50)
    option_2_type = models.CharField('옵션2 타입', max_length=10, default='COLOR')
    option_2_name = models.CharField('옵션2 이름(내부용)', max_length=50)
    option_2_display_name = models.CharField('옵션2 이름(고객용)', max_length=50)
    option_3_type = models.CharField('옵션3 타입', max_length=10, default='', blank=True)
    option_3_name = models.CharField('옵션3 이름(내부용)', max_length=50, default='', blank=True)
    option_3_display_name = models.CharField('옵션3 이름(고객용)', max_length=50, default='', blank=True)
    is_sold_out = models.BooleanField('품절여부', default=False)
    is_hidden = models.BooleanField('노출여부', default=False)
    add_price = models.IntegerField('추가가격', default=0)
    stock_quantity = models.PositiveIntegerField('재고개수, 품절일때 유용함', default=0)
