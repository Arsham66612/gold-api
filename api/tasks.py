import os
from django_q.tasks import async_task
import requests
from goldprice.models import GoldPrice
from django_q.models import Schedule
import redis
from django.conf import settings


def fetch_gold_price():
    api_key = os.environ.get('API_KEY')
    symbol = "XAU"
    curr = "USD"
    date = ""

    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"

    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        price = data['price']
        GoldPrice.objects.create(price=price)


# فراخوانی async_task برای اجرا در پس ‌زمینه
# def schedule_fetch_gold_price():
#     async_task('api.tasks.fetch_gold_price')


def create_schedule_task():
    # ایجاد وظیفه زمان‌بندی شده برای هر 1 دقیقه
    Schedule.objects.create(
        name='update_gold_price',
        func='api.tasks.fetch_gold_price',  # مسیری که تابع شما در آن قرار دارد
        schedule_type=Schedule.MINUTES,
        minutes=1,  # هر 1 دقیقه یکبار اجرا می‌شود
        repeats=-1  # -1 یعنی همیشه تکرار شود
    )


redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


def check_gold_price():
    # واکشی دو رکورد آخر
    last_two_prices = GoldPrice.objects.order_by('-created_at')[:2]

    # بررسی اینکه دو رکورد موجود باشد
    if len(last_two_prices) == 2:
        latest_price = last_two_prices[0].price  # آخرین قیمت
        second_last_price = last_two_prices[1].price  # یکی‌مانده‌به‌آخری قیمت
        pub_data = latest_price

        if latest_price != second_last_price:
            # پابلیش در کانال Redis
            redis_instance.publish('gold_price_channel', pub_data)
            return pub_data
        else:
            pass

    else:
        latest_price = last_two_prices[0].price
        pub_data = latest_price

        # پابلیش در کانال Redis
        redis_instance.publish('gold_price_channel', pub_data)
        return pub_data


# schedule publishing data
def schedule_publishing_data():
    Schedule.objects.create(
        name='publish_new_price',
        func='api.tasks.check_and_publish_gold_price',
        schedule_type=Schedule.MINUTES,
        minutes=1,
        repeats=-1
    )


pubsub = redis_instance.pubsub()
pubsub.subscribe('gold_price_channel')  # نام کانالی که می‌خواهید بررسی کنید

print("Listening for messages on 'gold_price_channel'...")

# گوش دادن به پیام‌های جدید
for message in pubsub.listen():
    if message['type'] == 'message':
        print("Received new gold price:", message['data'])
