#1300弱の温泉地の名前、場所、地域、詳細のurlの情報、画像のurlを取得し、csvファイルに保存
#urlはゆこゆこ参照
#保存場所はall_spring.csv
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from japanmap import groups
from japanmap import pref_code
import time

HEADER = [ 'name', 'location', 'area', 'urlinf', 'imginf']

#urlを取得して解析

driver = webdriver.Chrome()

url_list = []

for number in range(44):
    url_list.append("https://www.yukoyuko.net/onsen/search?page={}".format(number))


with open('all_spring.csv', 'a', encoding='utf-8') as f:
    #csvファイルへの書き込み
    writer = csv.writer(f)
    writer.writerow(HEADER)
    group = ['北海道','東北','関東','中部','近畿','中国', '四国','九州'] #温泉の場所がどの地方か分けるための配列
    for url in url_list:
        driver.get(url)
        time.sleep(3)
        
        #ページを自動でスクロールする
        #スクロールする理由は、ページの読み込みを完了させるため
        #これをしないと、画像のurlがno-imageとして表示されこれが取り込まれる
        height = driver.execute_script("return document.body.scrollHeight") 
        for x in range(1, height):
            if 3*x >= height:
                break
            driver.execute_script("window.scrollTo(0, "+str(3*x)+");")

        search_box = driver.find_elements(By.CLASS_NAME,"c-result_card")

        for inf in search_box:
            loc_inf = inf.find_elements(By.CLASS_NAME,"touchover") #場所
            name_inf = inf.find_element(By.TAG_NAME,"h2") #名前

            url_inf = name_inf.find_element(By.TAG_NAME, "a").get_attribute("href") #詳細ページのurl

            img_inf = inf.find_element(By.TAG_NAME, "img").get_attribute("src") #画像のurl

            if loc_inf[0].text == "北海道": #北海道はエリア名も北海道
                loc_item = loc_inf[0]
            else:
                loc_item = loc_inf[1]
                
            num = pref_code(loc_item.text) #場所(県)によって番号を振り分ける
            rank_area = '地方'
            for item in group:
                if(num in groups[item]):
                    rank_area = item #場所によってどの地方か判別し代入

            row = [name_inf.text, loc_item.text,  rank_area, url_inf, img_inf]
             #ファイルへの書き込み
            writer.writerow(row)

