import requests
from datetime import datetime, timedelta
from twilio.rest import Client

from keys import Keys
new_key = Keys()

STOCK_NAME = "DELL"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_key = new_key.stock_api_key
news_api_key = new_key.news_api_key
# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price. Hint: You can perform list
# comprehensions on Python dictionaries. e.g. [new_price for (key, value) in dictionary.items()]


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key
    }

stock_response = requests.get(STOCK_ENDPOINT, stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()['Time Series (Daily)']
yesterday_date = (datetime.today().date() - timedelta(days=5)).strftime("%Y-%m-%d")
yesterday_stock = stock_data.get(yesterday_date, None)
yesterday_closing_price = float(yesterday_stock["4. close"])


# Get the day before yesterday's closing stock price
day_before_yesterday_date = (datetime.today().date() - timedelta(days=4)).strftime("%Y-%m-%d")
day_before_yesterday_stock = stock_data.get(day_before_yesterday_date, None)
day_before_yesterday_closing_price = float(day_before_yesterday_stock["4. close"])

print(f"Yesterday closing price: {yesterday_closing_price}")
print(f"Day before yesterday closing price: {day_before_yesterday_closing_price}")

# - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20,
# but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = (yesterday_closing_price - day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "☝ 🚀"
else:
    up_down = "👎 😨"

print(f"Difference between both prices: {difference}")

# Work out the percentage difference in price between closing price yesterday
# and closing price the day before yesterday.
diff_perc = round((difference / yesterday_closing_price) * 100, 2)

print(f"Percentage of difference between: {diff_perc}")
# If TODO4 percentage is greater than 5 then print("Get News").
if abs(diff_perc) > 3:
    news_params = {
        "qInTitle": STOCK_NAME,
        "apiKey": news_api_key
    }

    news_response = requests.get(NEWS_ENDPOINT, news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    # print(news_data)

    # Use Python slice operator to create a list that contains the first 3 articles.
    # Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = news_data[:3]
    # print(three_articles)
    # STEP 3: Use twilio.com/docs/sms/quickstart/python
    # To send a separate message with each article's title and description to your phone number.

    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles_list = [f"\n{STOCK_NAME}: {up_down}{diff_perc}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles_list)
    # Send each article as a separate message via Twilio.
    # sending SMS via Twilio
    client = Client(new_key.twilio_account_sid, new_key.twilio_auth_token)

    for article in formatted_articles_list:

        message = client.messages.create(
            body=article,
            from_=new_key.twilio_from,
            to=new_key.twilio_to
        )
