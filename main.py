import requests
from datetime import datetime, timedelta
from twilio.rest import Client

#THIS IS DUMMY DATA FOR DEBUG PURPOSES, ALSO HELPS PREVENT EXHAUSTIVE API CALLS DURING TESTING
from json_data import data


#--------------------STOCK INFO------------------------------#
STOCK = " 'TSLA' FOR EXAMPLE"
COMPANY_NAME = "Tesla Inc FOR EXAMPLE"
API_KEY = "YOUR API KEY"
FUNCTION="TIME_SERIES_DAILY"
INTERVAL="15min"

#TWILIO
ACCOUNT_SID = "YOUR TWILIO ACCOUNT SID"
ACCOUNT_AUTH = "YOUR ACCOUNT AUTH"
TWILIO_PHONE = "+YOUR TWILIO PHONE"
TARGET_USER_PHONE = "THE PHONE YOU WANT TO SEND THE INFO TO"

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

#GRABS NEWS FROM ALPHAVANTAGE THEN FINDS 5% FLUCTUATIONS UP OR DOWN

response = requests.get(url=f"https://www.alphavantage.co/query?function={FUNCTION}&symbol={STOCK}&interval={INTERVAL}&apikey={API_KEY}")
response.raise_for_status()
stock_data = response.json()

comparison_list = []
stock_data_dic = {}

#GRABBING 20 DATA POINTS ONLY OR THE COMPARISON STRETCHES TOO FAR IN THE PAST
for i, (data, stock) in enumerate(stock_data['Time Series (Daily)'].items()):
    if i >=20:
        break
    stock_data_dic[data] = stock

for date, daily_data in stock_data_dic.items():
    high = daily_data["4. close"]
    if len(comparison_list) > 3:
        comparison_list.clear()
    comparison_list += [high, date]

    if len(comparison_list) == 4:
        today = float(comparison_list[0])
        yesterday = float(comparison_list[2])
        news_date = comparison_list[3]
        perc_check = percentage_increase_decrease(today, yesterday)

        # USES https://www.twilio.com TO SEND TEXTS TO THE USER, CHANGES THE MESSAGE BASED ON UP OR DOWN % STOCK

        if perc_check >= 5:
            top_news = []
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

            perc_news_trigger = f"{STOCK}: UP {round(perc_check)}% from {comparison_list[3]} to {comparison_list[1]}"

            #TODO you can enable this section if you'd like, but be warned it fails sometimes depending on article length and special characters.
            # formatted_news = "\n\n".join([f"{title}\n{url}" for title, url in top_news])
            # try:
            #     sms_news = formatted_news.encode('utf-8')
            #     print(sms_news)
            #     formatted_msg = f"{perc_news_trigger}\n\nNews Highlights:\n\n{sms_news}"
            # except UnicodeError:
            #     print("Unacceptable characters in new message.")

            #CREATES A CLIENT THEN SENDS A MESSAGE TO THE TARGET, TARGET MUST BE VERIFIED TO YOUR TWILLIO ACCOUNT.
            client = Client(ACCOUNT_SID, ACCOUNT_AUTH)

            message = client.messages.create(body=perc_news_trigger,

                                             from_=TWILIO_PHONE,

                                             to=TARGET_USER_PHONE,

                                             )

            # ALLOWS YOU TO SEE THE STATUS OF TEXTS SENT FOR ERRORS.
            print(message.status)
            print(message.body)
            print(message.sid)

        elif perc_check <= -5:
            top_news = []
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

            perc_news_trigger = f"{STOCK}: DOWN {round(perc_check)}% from {comparison_list[3]} to {comparison_list[1]}"

            # TODO you can enable this section if you'd like, but be warned it fails sometimes depending on article length and special characters.
            # formatted_news = "\n\n".join([f"{title}\n{url}" for title, url in top_news])
            # try:
            #     sms_news = formatted_news.encode('utf-8')
            #     print(sms_news)
            #     formatted_msg = f"{perc_news_trigger}\n\nNews Highlights:\n\n{sms_news}"
            # except UnicodeError:
            #     print("Unacceptable characters in new message.")

            #CREATES A CLIENT THEN SENDS A MESSAGE TO THE TARGET, TARGET MUST BE VERIFIED TO YOUR TWILLIO ACCOUNT.
            client = Client(ACCOUNT_SID, ACCOUNT_AUTH)

            message = client.messages.create(body=perc_news_trigger,

                                             from_=TWILIO_PHONE,

                                             to=TARGET_USER_PHONE,

                                             )

            # ALLOWS YOU TO SEE THE STATUS OF TEXTS SENT FOR ERRORS.
            print(message.status)
            print(message.body)
            print(message.sid)

