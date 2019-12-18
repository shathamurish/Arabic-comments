from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv


class FacebookBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        bot.get('https://www.facebook.com/')
        time.sleep(3)
        email = bot.find_element_by_id('email')
        password = bot.find_element_by_id('pass')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def to_csv(self, link_of_posts):
        bot = self.bot
        for post in link_of_posts:
            bot.get(post)
            time.sleep(3)
            list_of_comments = []
            for i in range(2): # عدد صفحات الكومنتات
                content = bot.find_element_by_tag_name('p')
                comments = bot.find_elements_by_tag_name('div')
                for comment in comments:
                    if 'Save' in comment.text or 'Go to Home' in comment.text or 'Overlord' in comment.text or 'replies' in comment.text or 'reply' in comment.text or 'Public' in comment.text or 'Like' in comment.text or 'React' in comment.text or 'Comment' in comment.text or 'comment' in comment.text or 'Share' in comment.text:
                        pass
                    else :
                        list_of_comments.append(comment.text)
                try:
                    submit_button = bot.find_element_by_xpath("//*[contains(text(), 'View more comments')]")
                    submit_button.click()
                    time.sleep(3)
                except:
                    pass
            try:
                with open('facebook.csv', 'a') as csvFile:
                    writer = csv.writer(csvFile)
                    my_comments = set(list_of_comments)
                    row = [content.text, str(my_comments)]
                    writer.writerow(row)
                csvFile.close()
            except:
                pass
            

    def get_posts(self, hashtag):
        bot = self.bot
        list_of_pages = []
        bot.get("https://www.facebook.com/search/pages/?q={}&epa=SEARCH_BOX".format(hashtag))
        time.sleep(3)
        for i in range(2): # عدد الصفحات اثناء البحث
            pages = bot.find_elements_by_class_name('_32mo')
            for elem in pages:
                if elem not in list_of_pages:
                    list_of_pages.append(elem.get_attribute('href'))
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(3)
        link_of_posts = []
        for page in list_of_pages:
            page = page.replace("www", "mobile")
            bot.get(page)
            time.sleep(3)
            for i in range(2): # عدد صفحات البوستات
                posts = bot.find_elements_by_xpath("//*[contains(text(), 'Comments')]")
                for post in posts:
                    try:
                        post_link = post.get_attribute('href')
                        post_link = post_link.split('&')[:2]
                        post_link = '&'.join(post_link)
                        if post_link not in link_of_posts:
                            link_of_posts.append(post_link)
                            print(post_link)
                    except AttributeError:
                        pass
                try:
                    submit_button = bot.find_element_by_xpath("//*[contains(text(), 'Show more')]")
                    submit_button.click()
                    time.sleep(3)
                except:
                    pass
        self.to_csv(link_of_posts)


bb = FacebookBot('@gmail.com', '@@@@@@')
bb.login()
bb.get_posts('##########') 
