from selenium import webdriver
from time import sleep
import getpass
wp = "https://web.whatsapp.com/"

driver = webdriver.Chrome()
driver.get(wp)
sleep(3)
input("Please read the QR code and type something\n")
name = input("Type the person to auto answer\n")
#adi arat
sleep(3)
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/input").send_keys(name)
sleep(5)
#sohbete gir
driver.find_elements_by_class_name("X7YrQ")[0].click()
#son mesaji al
sleep(5)
last_message = driver.find_elements_by_class_name("message-in")[-1] 
print(f"last_message = {last_message.text}")
while True:
    sleep(3)
    cur_message = driver.find_elements_by_class_name("message-in")[-1]
    if cur_message != last_message:
        print(f"New message: {cur_message.text}")
        last_message = cur_message
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]").send_keys("Attığınız mesajlar Berkay'ın HİÇ umrunda değil. Birey gibi ses kaydı atınız.")
        sleep(0.2)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button").click()