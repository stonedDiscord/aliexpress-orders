from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep

#open orders file
text_file = open("Output.txt", "w", encoding="utf-8")

#use chrome for this
driver = webdriver.Chrome("chromedriver.exe") 

#login and go to the order list
driver.get("https://login.aliexpress.com/?returnUrl=https%3A%2F%2Ftrade.aliexpress.com%2ForderList.htm")
sleep(4)
driver.switch_to.frame(0)

username = driver.find_element_by_id("fm-login-id")
# put your username/email here
username.send_keys("USERNAME")

sleep(2)

password = driver.find_element_by_id("fm-login-password")
# password
password.send_keys("PASSWORD")

sleep(2)
submit = driver.find_element_by_class_name("fm-submit")
# go
submit.click()

# put a pretty header on my csv file
text_file.write("Order ID;Product;Store;Value;Tracking ID;Carrier;Order time;Status\n")
orders = [["Order ID","Product(s)","Store","Value","Tracking ID","Carrier","Order Time","Status"]]

ordersleft = True
page=1
while ordersleft==True and page<=50:
    sleep(6)
    # wait for everything to load
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
        if thisorder not in orders:
            print(item)
            text_file.write(item+"\n")

            orders.append(thisorder)
    
    nextbutton = driver.find_element_by_class_name("ui-pagination-next")

    # if the next page button is disabled, we have reached the end
    if 'ui-pagination-disabled' in nextbutton.get_attribute('class').split():
        ordersleft = False
    else:
        nextbutton.click()
        page+=1
    
text_file.close()
# open a new file for the complete list
# because i want to keep a backup
text_file = open("Logistics.txt", "w", encoding="utf-8")

for y in orders:
    # only get orders that have been sent out, otherwise it will fail
    if y[7] == "Awaiting delivery": # or y[7] == "Finished":
        sleep(4)
        text_file.flush()
        driver.get("https://trade.aliexpress.com/order_detail.htm?orderId="+y[0])
        sleep(4)
        y[5] = driver.find_element_by_css_selector(".logistics-name").text
        y[4] = driver.find_element_by_css_selector(".logistics-num").text

        item = ";".join(str(z) for z in y)

        print(item)
        text_file.write(item+"\n")

text_file.close()