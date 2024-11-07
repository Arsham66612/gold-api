from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GoldPrice(BaseModel):
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.price}/{self.created_at}'


# class CoinPrice(BaseModel):
# #     ...
# #     pass