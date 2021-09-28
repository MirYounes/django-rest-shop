from django.conf import settings
from coupons.models import Coupon
import redis


if settings.DEBUG:
    redis = redis.Redis(host='127.0.0.1', port='6379')
else :
    redis = redis.Redis(host='redis', port='6379')


class Cart:
    PREFIX = settings.CART_PREFIX
    EXPIRE = settings.CART_EXPIRE

    @classmethod
    def add_cart(cls, **kwargs):
        user_id = kwargs.get('user_id')
        product_id = kwargs.get('product_id')
        cart_name = f'{cls.PREFIX}_{user_id}_{product_id}'

        if redis.exists(cart_name):
            redis.hincrby(cart_name, 'quantity', kwargs['quantity'])

        else:
            [redis.hset(cart_name, field, value)
             for field, value in kwargs.items()]
            redis.expire(cart_name, cls.EXPIRE)

        return 'cart added/changed'

    @classmethod
    def get_cart(cls, user_id):
        cart = []
        for user_carts in redis.scan_iter(f'{cls.PREFIX}_{user_id}_*'):
            data = {key.decode('utf-8'): value.decode('utf-8')
                    for key, value in redis.hgetall(user_carts).items()}
            cart.append(data)
        
        return cart
    
    @classmethod
    def delete_product(cls, user_id, product_id):
        cart_name = f'{cls.PREFIX}_{user_id}_{product_id}'
        return redis.delete(cart_name)        
    
    @classmethod
    def delete_cart(cls, user_id):
        for user_carts in redis.scan_iter(f'{cls.PREFIX}_{user_id}_*'):
            redis.delete(user_carts)
        cls.delete_coupon_from_cart(user_id)

    @classmethod
    def add_coupon_to_cart(cls,**kwargs):
        user_id = kwargs.get('user_id')
        coupon_name = f'{cls.PREFIX}_coupon_{user_id}'
        redis.set(coupon_name,kwargs.get("code"))          

    @classmethod
    def get_coupon_from_cart(cls,user_id):
        code = redis.get(f'{cls.PREFIX}_coupon_{user_id}')
        if code == None :
            return None

        try :
            coupon = Coupon.objects.get(code=code.decode('utf-8'))
        except Coupon.DoesNotExist :
            return None
        
        return coupon

    @classmethod
    def delete_coupon_from_cart(cls,user_id):
         coupon_name = f'{cls.PREFIX}_coupon_{user_id}'
         redis.delete(coupon_name)
        