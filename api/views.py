from django.shortcuts import render
from goldprice.models import GoldPrice
import requests


# def make_gapi_request():
#     api_key = "goldapi-1qtfsm2izc8jx-io"
#     symbol = "XAU"
#     curr = "USD"
#     date = ""
#
#     url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"
#
#     headers = {
#         "x-access-token": api_key,
#         "Content-Type": "application/json"
#     }
#
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#
#         result = response.text
#         print(result)
#     except requests.exceptions.RequestException as e:
#         print("Error:", str(e))
#
#
# make_gapi_request()


def make_gapi_request(request, symbol="XAU", curr="USD", date=""):
    api_key = "goldapi-1qtfsm2izc8jx-io"

    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"

    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        gold_price = data.get("price")

        if gold_price:
            GoldPrice.objects.create(price=gold_price)
            return render(request, 'goldprice/index.html')
