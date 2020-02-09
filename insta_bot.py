from selenium import webdriver
from time import sleep
import getpass
insta = "https://www.instagram.com/"


def scroll_to_end(driver, box, get_links=True):
    # scrool to the end
    links = set()
    hei, pre_hei = 1, 0
    while hei != pre_hei:
        if get_links:
            cur_links = box.find_elements_by_tag_name("a")
            for l in cur_links:
                if l.text != "":
                    links.add(l.text)
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
    return links


def get_user_infos():
    uname = input("Enter Username:")
    pword1, pword2 = "", " "
    while pword1 != pword2:
        pword1 = input("Enter password:")  # getpass.getpass("Enter Password:")
        # getpass.getpass("Confirm Password:")
        pword2 = input("Confirm Password:")
        if pword1 != pword2:
            print("Unmatching password")
    return uname, pword1


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
        sleep(3)
        # click following
        self.driver.find_element_by_xpath(
            "//a[contains(@href,'/following')]").click()
        sleep(3)

        scroll_box = self.driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]/ul")
        scroll_to_end(self.driver, scroll_box, False)

        links = scroll_box.find_elements_by_tag_name("a")
        names = [link.text for link in links if link.text != ""]
        sleep(3)
        return names

    def get_followers(self, uname):
        self.go_profile(uname)
        sleep(3)
        self.driver.find_element_by_xpath(
            "//a[contains(@href,'/followers')]").click()
        sleep(3)

        scroll_box = self.driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]/ul")
        scroll_to_end(self.driver, scroll_box, False)

        links = scroll_box.find_elements_by_tag_name("a")
        names = [link.text for link in links if link.text != ""]
        sleep(3)
        return names

    def get_last_fotos(self, uname):
        self.go_profile(uname)
        fotos = self.driver.find_elements_by_class_name("_9AhH0")
        return fotos

    def get_last_likes(self, uname, index):
        fotos = self.get_last_fotos(uname)
        fotos[index].click()
        sleep(3)
        # see all likes
        try:
            self.driver.find_element_by_xpath(
                "/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button").click()
        except:
            print("FAIL1")
            try:
                self.driver.find_element_by_xpath(
                    "/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div[2]/button").click()
            except:
                print("FAIL2")
        sleep(2)
        box = self.driver.find_element_by_xpath(
            "/html/body/div[5]/div/div[2]/div/div")
        likes = scroll_to_end(self.driver, box)
        return list(likes)

    def count_likes_for_followers(self, uname):
        total_photos = 0
        followers = self.get_followers(uname)
        counts = {follower: 0 for follower in followers}
        for i in range(5):
            try:
                likes = self.get_last_likes(uname, i)
                for like in likes:
                    if like in followers:
                        counts[like] += 1
                total_photos += 1
            except:
                break
        return counts, total_photos

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

    def print_likes_per_follower(self, uname):
        counts, total_photos = self.count_likes_for_followers(uname)
        followings = self.get_following(uname)

        sorted_counts = sorted((value, key) for (key, value) in counts.items())
        for like, uname in sorted_counts:
            if uname in followings:
                print(f"{like}/{total_photos} {uname}")

    def print_non_follow_backs(self, uname):
        bad_people = self.not_followers_from_following(uname)
        print(f"Here are the bad people for {uname}\n")
        for bad in bad_people:
            print(bad)
        print(f"\nTotal: {len(bad_people)} people")

    def close(self):
        self.driver.close()
        self.driver.quit()
        # self.driver.stop_client()


print("In order to use the program, you need to login with an account that have acces to the target profiles")
uname, pword = get_user_infos()
bot = InstaBot(uname, pword)

choise = 1
while choise != 0:
    print("What would you like to do?")
    print("0 - Exit")
    print("1 - See the people that doesn't follow target account but target follows them")
    print("2 - See how many photos did each followers like in last 5 photos")
    choise = int(input())
    if choise == 1:
        inp = input("Please type the username of the target:")
        print("Please wait...")
        bot.print_non_follow_backs(inp)
    elif choise == 2:
        inp = input("Please type the username of the target:")
        print("Please wait...")
        bot.print_likes_per_follower(inp)

print("Bye")
bot.close()

# birden fazla windowla aynı anda bikac listeyi birden alabilir miyim?
# en basiti 5 fotoğrafın hepsini aynı anda almak
