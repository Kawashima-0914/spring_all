#温泉地の情報入りファイルを読み取り、温泉地の詳しい情報にアクセスして情報を取得してそれぞれの温泉地の名前のテキストファイルに書き込む
#urlはゆこゆこを参照
#保存場所はspring_feature2
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from make_list1 import List_make
import os


list_all = List_make()
list_all.list_operate()

list_name = list_all.name #温泉の名前を格納する配列
list_inf = list_all.url #温泉の情報あるurlを格納


quality_kinds = [
    "単純温泉", "塩化物泉", "炭酸水素塩泉", "硫酸塩泉",
    "二酸化炭素泉", "含鉄泉", "硫黄泉", "酸性泉", "ラジウム泉"
    ]

def operate():
    driver = webdriver.Chrome()
    for name, url in zip(list_name, list_inf):
        os.chdir("C:\\Users\\Owner\\python_practice\\spring_all\\spring_feature2")
        with open(name+".txt", 'w', encoding='utf-8') as f:
            driver.get(url)
            time.sleep(3)
            title = driver.find_element(By.CLASS_NAME,  "onsenDetail_contents_info_lead").text + "\n" #温泉地の概要のタイトルを取得
            title_content = driver.find_element(By.CLASS_NAME, "onsenDetail_contents_info_txt").text + "\n" #温泉地の概要を取得
            #改行は消しておく(後に活用するため)
            if("\n" in title_content):
                title_content.replace("\n", '')
            #情報の区切りをつけるために改行
            title_content + "\n"
            figure = driver.find_element(By.CLASS_NAME, "feature_contents_txt").text  #温泉地の泉質関係の概要を取得
            if("\n" in figure):
                figure.replace("\n", '')
            figure = figure + "\n"
            figure_quality = driver.find_elements(By.CLASS_NAME, "feature_contents_dl_dd") #泉質の特量を表す表を取得
            if(len(figure_quality) == 0):
                all_inf = [title, title_content, figure]
            elif(len(figure_quality)==1):
                figure_quality1 = figure_quality[0].text + "\n" #泉質
                all_inf = [title, title_content, figure, figure_quality1]
            elif(len(figure_quality)==2):
                figure_quality1 = figure_quality[0].text + "\n" #泉質か泉質の特徴
                figure_quality2 = figure_quality[1].text + "\n" #効能か泉質
                quality_judge = figure_quality1.split("、")
                if(quality_judge[0].replace("\n", "") in quality_kinds): #quality1は泉質、quality2は効能
                    all_inf = [title, title_content, figure, figure_quality1, figure_quality2]
                else:#quality1は泉質の特徴、quality2は泉質
                    all_inf = [title, title_content, figure, figure_quality2, figure_quality1]
            else:
                figure_quality1 = figure_quality[1].text + "\n" #泉質
                figure_quality2 = figure_quality[0].text + "、" #温泉の泉質についての特徴 
                figure_quality3 = figure_quality[2].text + "\n" #温泉の効能
                #温泉の泉質についての特徴と温泉の効能はまとめる
                all_inf = [title, title_content, figure, figure_quality1, figure_quality2, figure_quality3]
            f.writelines(all_inf)
            f.close()

operate() #実行してファイルを破損しないため、温泉の情報のテキストファイルが欲しい場合は実行する
            





        
