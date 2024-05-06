import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

VIRTUAL_TWILIO_NUMBER = ""
VERIFIED_NUMBER = None
TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "c2530f672c574e74954f8809c8cb8939"
API_KEY = "6EW2DZG30LORJDS6"
NEWS_PARAMS = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}
PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_KEY,
}

response = requests.get(url=STOCK_ENDPOINT, params=PARAMETERS)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_price = float(yesterday_data["4. close"])
print(yesterday_price)



day_before_data = data_list[1]
day_before_price = float(day_before_data["4. close"])
print(day_before_price)

difference = yesterday_price - day_before_price
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


percentage = round((difference / yesterday_price)) * 100
print(percentage)

if abs(percentage) > 2:
    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMS)
    articles = news_response.json()["articles"]
    top_three = articles[:3]
    print(top_three)





formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage}%\nHeadling: {article['title']}."
                      f"\nBrief: {article['description']}" for article in top_three]

print(formatted_articles)

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from=VIRTUAL_TWILIO_NUMBER,
        to=VERIFIED_NUMBER,
    )





