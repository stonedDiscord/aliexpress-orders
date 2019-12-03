from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import csv
text_file = open("Output.txt", "w")
driver = webdriver.Chrome("chromedriver.exe") 
driver.get("https://login.aliexpress.com/?returnUrl=https%3A%2F%2Ftrade.aliexpress.com%2ForderList.htm")
sleep(4)
driver.switch_to.frame(0)
username = driver.find_element_by_id("fm-login-id")
username.send_keys("USERNAME")
sleep(2)
password = driver.find_element_by_id("fm-login-password")
password.send_keys("PASSWORD")
sleep(2)
submit = driver.find_element_by_class_name("fm-submit")
submit.click()

text_file.write("Order ID;Product;Store;Value;Tracking ID;Carrier;Order time;Status\n")

orders = [["Order ID","Product(s)","Store","Value","Tracking ID","Carrier","Order Time","Status"]]

ordersleft = True
while ordersleft==True:
    sleep(6)
    text_file.flush()
    order_elements = driver.find_elements_by_class_name("order-item-wraper")

    for x in order_elements:
        thisorder = [x.find_element_by_css_selector(".order-info .first-row .info-body").text,
        x.find_element_by_css_selector(".product-title .baobei-name").text,
        x.find_element_by_css_selector(".store-info .info-body").text,
        x.find_element_by_css_selector(".amount-num").text,"","",
        x.find_element_by_css_selector(".order-info .second-row .info-body").text,
        x.find_element_by_css_selector(".order-status .f-left").text]

        item = ";".join(str(z) for z in thisorder)

        print(item)
        text_file.write(item+"\n")

        #print(thisorder)
        orders.append(thisorder)

    
    nextbutton = driver.find_element_by_class_name("ui-pagination-next")
    print(nextbutton.get_attribute('class').split())

    if 'ui-pagination-disabled' in nextbutton.get_attribute('class').split():
        ordersleft = False
    else:
        nextbutton.click()
    
text_file.close()

text_file = open("Logistics.txt", "w")

for y in orders:
    if y[7] == "Awaiting delivery" or y[7] == "Finished":
        driver.get("https://trade.aliexpress.com/order_detail.htm?orderId="+y[0])
        sleep(4)
        driver.switch_to.frame(0)
        y[5] = driver.find_elements_by_class_name("logistics-name").text
        y[4] = driver.find_elements_by_class_name("logistics-num").text

        item = ";".join(str(z) for z in y)

        print(item)
        text_file.write(item)

text_file.close()