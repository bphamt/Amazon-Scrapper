from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib, ssl

# SMTP Login
my_email = "-----redacted-----"
password = "-----redacted-----"
PORT = 587

CHROME_DRIVER_PATH = r"C:\Users\bpham\Documents\chromedriver"

# PRICE TO ALERT WHEN PRODUCT GOES BELOW THIS
MY_PRICE = 32
# AMAZON URL LINK
URL_SCRAPE = "https://www.amazon.com/gp/product/B072P11H8L?pf_rd_r=C5K6WNK06FH2GWNGDES8&pf_rd_p=5ae2c7f8-e0c6-4f35-9071-dc3240e894a8&pd_rd_r=5420a85a-b122-4473-919c-4a4aca94a5ec&pd_rd_w=xH16V&pd_rd_wg=EINuO&ref_=pd_gw_unk"

# Run headless
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options, executable_path=CHROME_DRIVER_PATH)

# Grab web data
driver.get(URL_SCRAPE)

# Grab element by tag xPATH
price = float((driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]')).text.split("$")[1])
title = (driver.find_element_by_xpath('//*[@id="productTitle"]')).text

if price < MY_PRICE:
    SUBJECT = "Low Price Alert!"
    MESSAGE = f"Low Price Alert!\nOnly ${price} to buy {title}\n\nLink: {URL_SCRAPE}"

    try:
        context = ssl.create_default_context()
        connection = smtplib.SMTP("smtp.gmail.com", port=PORT)
        connection.starttls(context=context)
        connection.login(user=my_email, password=password)
    except:
        print("Can't connect to server")
    else:
        connection.sendmail(
            from_addr=my_email,
            to_addrs="-----redacted-----",
            msg='Subject: {}\n\n{}'.format(SUBJECT, MESSAGE)
        )
    finally:
        connection.close()

driver.quit()
