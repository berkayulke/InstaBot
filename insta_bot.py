from selenium import webdriver
from time import sleep
insta = "https://www.instagram.com/"


def scroll_to_end(driver, box):
    # scrool to the end
    hei, pre_hei = 1, 0
    while hei != pre_hei:
        pre_hei = hei
        sleep(0.5)
        hei = driver.execute_script('''
        arguments[0].scrollIntoView(false);
        return arguments[0].scrollHeight;
        ''', box)
        # if stuck try again for 0.1 seconds 30 times
        i = 0
        while i < 30 and hei == pre_hei:
            sleep(0.1)
            hei = driver.execute_script('''
            arguments[0].scrollIntoView(false);
            return arguments[0].scrollHeight;
            ''', box)
            i += 1


class InstaBot:
    def __init__(self, uname, pword):
        self.uname = uname
        self.pword = pword

        self.driver = webdriver.Chrome()
        self.driver.get(insta)
        sleep(3)

        # click login button
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[2]/p/a").click()
        sleep(3)

        # fill uname & pword
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(uname)
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(pword)
        # click login
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button").click()
        sleep(5)

        # click not now in notification alert box
        self.driver.find_element_by_xpath(
            "/html/body/div[4]/div/div/div[3]/button[2]").click()

    def go_profile(self, to_uname):
        self.driver.get(f"{insta}{to_uname}/")
        sleep(3)

    def get_following(self, uname):
        self.go_profile(uname)
        sleep(4)
        # click following
        self.driver.find_element_by_xpath(
            "//a[contains(@href,'/following')]").click()
        sleep(4)

        scroll_box = self.driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]/ul")
        scroll_to_end(self.driver, scroll_box)

        links = scroll_box.find_elements_by_tag_name("a")
        names = [link.text for link in links if link.text != ""]
        sleep(3)
        return names

    def get_followers(self, uname):
        self.go_profile(uname)
        sleep(4)
        self.driver.find_element_by_xpath(
            "//a[contains(@href,'/followers')]").click()
        sleep(4)

        scroll_box = self.driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]/ul")
        scroll_to_end(self.driver, scroll_box)

        links = scroll_box.find_elements_by_tag_name("a")
        names = [link.text for link in links if link.text != ""]
        sleep(3)
        return names

    def not_followers_from_following(self, uname):
        sleep(3)
        followings = self.get_following(uname)
        sleep(3)
        followers = self.get_followers(uname)
        bad_people = []
        for following in followings:
            if following not in followers:
                bad_people.append(following)
        bad_people.sort()
        return bad_people

    def close(self):
        self.driver.close()
        self.driver.quit()
    
print("In order to use the program, you need to login with an account that have acces to the target profiles")
uname = input("Enter Username:")
pword = input("Enter Password:")

target_list = []
inp = input("Please type the username of the target:")
print("If you want to target more than one user, you can type their usernames now.")
print("When you're done, type 'done':")

while inp != "done":
    target_list.append(inp)
    inp = input()
print("Please wait...")

bot = InstaBot(uname, pword)

for user in target_list:
    bad_people = bot.not_followers_from_following(user)
    print(f"Here are the bad people for {user}\n{bad_people}\nTotal: {len(bad_people)} people")
bot.close()
