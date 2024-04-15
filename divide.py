#温泉地の県によって温泉地を分類するためのファイル
#prefectureファイルへ格納する

import csv 
import os
from make_list1 import List_make #温泉地の名前、場所、画像url取得

List_spring = List_make()
List_spring.list_operate()
name_all = List_spring.name
location_all = List_spring.location
image_all = List_spring.image

def divide():
        os.chdir("./prefecture")
        for name, location, image in zip(name_all, location_all, image_all):
                with open(location+".csv", "a", encoding="UTF-8") as t:#ファイルの保存先はその温泉の所在地(都道府県)
                    writer = csv.writer(t)
                    row = [name, image] #温泉の名前と画像のデータをファイルとして保存
                    writer.writerow(row)
        #print(len_data)

divide()