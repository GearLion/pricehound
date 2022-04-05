# Amazon Price Tracker
from requests import get
from bs4 import BeautifulSoup
from credentials import ORIGIN_EMAIL, PASSWORD, TEST_EMAIL
from smtplib import SMTP
from re import sub

amazon_headers = {
    "User-Agent": "en-US,en;q=0.9",
    "Accept-Language": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
}

website = get("https://www.amazon.com/dp/B07ZJKZXLG/?coliid=I38TZMK6AGDLA5&colid=2VUSCXGEIOO2M&ref_=lv_ov_lig_dp_it&th=1", headers=amazon_headers).text
soup = BeautifulSoup(website, "html.parser")

item_name = soup.find(name="h1", class_="a-size-large a-spacing-none").get_text().split(",")[0]
item_name = sub(' +', ' ', item_name)
price_text = soup.find(name="span", class_="a-offscreen").get_text()
price = float(price_text.split("$")[1])

if price < 400:
    with SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=ORIGIN_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=ORIGIN_EMAIL, to_addrs=TEST_EMAIL,
                            msg=f"Subject: Shop Now!\n\nAn item on your list is for sale:"
                                f"\n\n Your{item_name} is on sale for {price_text}.")

