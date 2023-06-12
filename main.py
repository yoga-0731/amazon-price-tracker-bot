import os
import requests
from bs4 import BeautifulSoup
import smtplib

AMAZON_PRODUCT_URL = "https://www.amazon.in/AGARO-Utensils-Stainless-Resistant-Cookware/dp/B09XTYCLDJ/ref=sr_1_6?crid=1AYIA3HNZ6HL2&keywords=kitchen+utensils&qid=1686540620&sprefix=kitchen+utensil%2Caps%2C421&sr=8-6"
FROM_MAIL = os.environ.get('FROM_EMAIL')
TO_MAIL = os.environ.get('TO_MAIL')
PASSWORD = os.environ.get('PASSWORD')

HEADERS = {
    "User-Agent": os.environ.get('USER_AGENT'),
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url=AMAZON_PRODUCT_URL, headers=HEADERS)
amazon_data = response.text

soup = BeautifulSoup(amazon_data, 'html.parser')
# print(soup.prettify())
amazon_price = float(soup.select_one(".a-price-whole").getText().replace(',', ''))
product = soup.select_one("#productTitle").getText().strip()
desired_price = 1400.00

if amazon_price <= desired_price:
    content = f"Kitchen utensil price dropped to Rs.{amazon_price}."
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=FROM_MAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=FROM_MAIL,
            to_addrs=TO_MAIL,
            msg=f"Subject: Amazon Price Alert for Kitchen Utensil!!\n\n{content}\nProduct - {product}\n{AMAZON_PRODUCT_URL}"
        )
