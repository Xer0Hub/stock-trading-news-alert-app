import requests
from urllib3 import request
from datetime import datetime, timedelta
from json_data import data

#--------------------STOCK INFO------------------------------#
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = "O857A9YD8EG7TGNC"
FUNCTION="TIME_SERIES_DAILY"
INTERVAL="1 day"

#--------------------DEFINITIONS------------------------------#
def percentage_increase_decrease(new_num, old_num):
    step_1 = new_num - old_num
    return step_1 / old_num * 100

def news_grabber(news_articles):
    top_3_articles = []
    for article in range(3):
        titles = news_articles[article]["title"]
        url_link = news_articles[article]["url"]
        top_3_articles.append([titles, url_link])
    return top_3_articles

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO RE-ENABLE TOMORROW
# response = requests.get(url=f"https://www.alphavantage.co/query?function={FUNCTION}&symbol={STOCK}&interval={INTERVAL}&apikey={API_KEY}")
# response.raise_for_status()
# stock_data = response.json()

stock_data = data
comparison_list = []

for date, daily_data in stock_data["Time Series (Daily)"].items():
    high = daily_data["2. high"]
    if len(comparison_list) > 3:
        comparison_list.clear()
    comparison_list += [high, date]

    if len(comparison_list) == 4:
        today = float(comparison_list[0])
        yesterday = float(comparison_list[2])
        news_date = comparison_list[3]
        perc_check = percentage_increase_decrease(today, yesterday)
        if perc_check >= 5:
            top_news = []

            print(f"{STOCK}: 🔺 {round(perc_check)}% from {comparison_list[3]} to {comparison_list[1]}")
            # THIS IS WHERE THE NEWS API IS CALLED
            # NEWS API KEY
            NEWS_API_KEY = "d1329132c3074c509f52d020b4bacc4f"
            # CHECK YESTERDAY'S NEWS
            today_info = datetime.now()
            yesterday_date = today_info.date() - timedelta(days=1)

            # API CALL TO NEWS FOR COMPANY
            response = requests.get(
                url=f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={news_date}&sortBy=publishedAt&apiKey={NEWS_API_KEY}")
            response.raise_for_status()
            news_data = response.json()
            articles = news_data["articles"]
            top_news += news_grabber(articles)
            print(top_news)
            print(len(top_news))

        elif perc_check <= -5:
            top_news = []

            print(f"{STOCK}: 🔻 {round(perc_check)}% from {comparison_list[3]} to {comparison_list[1]}")
            ## STEP 2: Use https://newsapi.org
            # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

            # THIS IS WHERE THE NEWS API IS CALLED
            # NEWS API KEY
            NEWS_API_KEY = "d1329132c3074c509f52d020b4bacc4f"
            #CHECK YESTERDAY'S NEWS
            today_info = datetime.now()
            yesterday_date = today_info.date() - timedelta(days=1)

            #API CALL TO NEWS FOR COMPANY
            response = requests.get(
                url=f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={news_date}&sortBy=publishedAt&apiKey={NEWS_API_KEY}")
            response.raise_for_status()
            news_data = response.json()
            articles = news_data["articles"]
            top_news += news_grabber(articles)
            print(top_news)
            print(len(top_news))




## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

