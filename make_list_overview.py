#他スクリプトファイルで使用するための定義
import os


#温泉地の名前から温泉の概要などの情報を取得するためのクラス
class List_inf:
    spring_inf = []

    def __init__(self, name):
        self.name = name

    def inf_get(self):
        with open(self.name+'.txt', 'r', encoding="UTF-8") as f:
            self.spring_inf = f.readlines()


#list = List_inf("草塩温泉（くさしお）")
#list.inf_get()
#print(list.spring_inf)