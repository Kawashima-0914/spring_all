#類似度を計算してcsvファイルとして保存する
#温泉の情報の改行を区切りに段落としている

import gensim
from sklearn.metrics.pairwise import cosine_similarity
import os
from make_list1 import List_make
import csv

#温泉の名前を保存
inf = List_make()
inf.list_operate()
list_name = inf.name 

HEADER = ['name', 'value']

#泉質の種類をリストに保存
#温泉の情報に泉質の種類が含まれる場合と含まれない場合があるので
quality_kinds = [
    "単純温泉", "塩化物泉", "炭酸水素塩泉", "硫酸塩泉",
    "二酸化炭素泉", "含鉄泉", "硫黄泉", "酸性泉", "ラジウム泉"
    ]


model_path = "C:\\Users\\Owner\\python_practice\\spring_all\\chive-1.2-mc5_gensim\\chive-1.2-mc5_gensim\\chive-1.2-mc5.kv"
model = gensim.models.KeyedVectors.load(model_path) #類似度を出す際の学習モデル



#温泉の特徴と泉質の説明の類似度を出す関数(1つずつ単語を比較していき、1つの単語に対して一番大きな類似度をその単語が持つ類似度として
#全ての単語の類似度を平均した結果を単語の類似度とする。)
def cosine_eval(datalist, datalist_center, i, j):   #比較する温泉の名前(name)、中心となる(軸)温泉の名前(name_center)と何段落目からの情報かを表すiを引数として持つ
    word_eval = 0 #1つずつの単語の類似の一次保管
    word_all_eval = 0 #全ての単語での類似度を平均した結果

    datalist_center = datalist_center[j].split('、') #"、"を基準に切り分け配列に格納
    if datalist_center[0] == "\n":
        return 0.0
    datalist_center.pop()#含まれる改行を取り除く
    datalist_center_len = 0 #類似度を足した回数をカウント(配列の大きさでは類似度を計算に入れない単語が出たとき意味合いが変わる)
    
    datalist = datalist[i].split('、')
    if datalist[0] == "\n":
        return 0.0
    datalist.pop()
    #単語1つずつ比較していく
    for word_center in datalist_center:
        word_eval = 0.0
        if "pH" in word_center: #pHによる類似度の計算
            try:
                pH_word_center = word_center.replace("pH", "") #"pH"は計算に不要
                pH_word_center = float(pH_word_center) #pHの値を不動少数に変換
                for word in datalist:
                    if "pH" in word:
                        pH_word = word.replace("pH", "")
                        pH_word = float(pH_word)
                        if pH_word_center == pH_word: #pHが同じ時は類似度1
                            word_all_eval += 1.0
                            datalist_center_len += 1
                            break
                        else:
                            pH_diff = abs(pH_word_center-pH_word) #pHの差の絶対値
                            if pH_diff < 2.0: #pHの差が2より小さい時は類似度が高いとする
                                word_all_eval += 0.8
                                datalist_center_len += 1
                                break
                            elif pH_diff < 4.0: #pHの差が4より小さい時は少し類似度あり
                                word_all_eval += 0.5
                                datalist_center_len += 1
                                break
                            else: #pHの差が4より大きいものは類似度なしとする
                                word_all_eval += 0.0
                                datalist_center_len += 1
                                break
            except:
                continue
        else:
            for word in datalist:
                try:
                    match = cosine_similarity([model[word_center]], [model[word]]) #それぞれの単語の類似度を計算、計算出来ない単語があるときはスルー
                    match = match[0][0] #出力が二次元配列であるため
                    if word_eval < match: #対象の単語でそれぞれの単語との類似度を計算して一番大きい類似度を保存していく
                        word_eval = match
                except:  
                    continue
            word_all_eval += word_eval #類似度の総和
            datalist_center_len += 1 #類似度が計算できたら比べた単語の数としてカウントしていく
    if datalist_center_len != 0:
        word_all_eval = word_all_eval / datalist_center_len #平均を出す
    else:
        return 0
    return word_all_eval


def spring_feature(name): #温泉の情報を返す関数
    os.chdir("C:\\Users\\Owner\\python_practice\\spring_all\\spring_feature_list")
    f = open(name+'_analy.txt', 'r', encoding='UTF-8')
    datalist = f.readlines()
    f.close()
    return datalist

#受け取った情報に温泉の泉質(単純温泉など)がふくまれるかを返す関数。含まれる場合は1、含まれない場合は0を返す
def quality_is(datalist, i): #nameは温泉、iは温泉の何段落目かの情報か
    quality = datalist[i].replace("\n","").split("、") #情報を扱える形に変形→改行を取り除いたものをリストに格納
    quality_len = len(quality)
    for j in range(quality_len):
        quality_item = quality[j-1]#リストの１つずつが温泉の種類に含まれるかを見る
        if quality_item in quality_kinds:
            return 1
    return 0

#温泉の種類から類似度を出す、類似度の計算の仕方は同じ泉質１つにつき0.5を加算するとする
def quality_similarity(datalist_center, datalist): #name_centerは温泉の比較の中心、nameは比較される温泉
    similar = 0 #類似度を格納
    quality_center = datalist_center[2].replace("\n", "").split("、") #改行を除き、"、"で区切りリストとして保存
    quality = datalist[2].replace("\n", "").split("、")
    for item in quality_center:
        if item in quality:
            similar = similar + 0.5
    return similar




class Similarity_value:

    result = {} #それぞれの温泉に対しての類似度を辞書として保存するためのもの(keyが名前でvalueが類似度)
    flag_center = 0 #比較の中心の温泉の情報に泉質の種類が含まれるか
    flag = 0 #比較される温泉の情報に泉質の種類が含まれるか
    quality_number_center = 0 #比較の中心の温泉において泉質の種類がどの段落にあるかを格納
    quality_number = 0 #比較される温泉において泉質の種類がどの段落にあるかを格納

    def __init__(self, data, center): #dataは温泉の名前全体(list)、centerは対象とする温泉(軸)
        self.data = data
        self.center = center

    def calculate(self):
        datalist_center = spring_feature(self.center)
        len_center = len(datalist_center)
        #１段落目の情報の類似度
        for name in self.data:
            datalist = spring_feature(name)
            len_datalist = len(datalist)
            self.result[name] = cosine_eval(datalist, datalist_center, 0, 0) #一段落目の説明の類似度を辞書に格納
            self.result[name] = self.result[name] + cosine_eval(datalist, datalist_center, 1, 1) #二段落目の説明の類似度を辞書に格納
            if len_center > 2: #泉質、効能が含まれる場合
                self.flag_center = quality_is(datalist_center, 2) #泉質が含まれる場合はflagが1になる
                if self.flag_center == 1: #泉質が含まれる場合
                    if len_datalist > 2:
                        self.flag = quality_is(datalist, 2)
                        if self.flag == 1: #比較する温泉も泉質がある場合
                            self.result[name] = self.result[name] + quality_similarity(datalist_center, datalist) #三段落目の泉質についての類似度計算
                            if len_datalist == 4 and len_center == 4: #効能がどちらの温泉においてもある場合
                                self.result[name] = self.result[name] + cosine_eval(datalist, datalist_center, 3, 3)
                        elif self.flag == 0:    #比較する温泉に泉質がない場合
                            if len_center == 4: #比較の中心となる温泉に効能が含まれる場合
                                self.result[name] = self.result[name] + cosine_eval(datalist, datalist_center, 2, 3)
                elif self.flag_center == 0:     #比較の中心となる温泉に泉質が含まれない場合
                    if len_datalist > 2:
                        self.flag = quality_is(datalist, 2)
                        if self.flag == 0:  #比較される温泉に泉質が含まれない場合
                            self.result[name] = self.result[name] + cosine_eval(datalist, datalist_center, 2, 2)
                        elif self.flag == 1: #比較される温泉に泉質が含まれる場合
                            if len_datalist == 4:   #比較される温泉に効能が含まれる場合
                                self.result[name] = self.result[name] + cosine_eval(datalist, datalist_center, 3, 2)


#それぞれの温泉のcsvファイルとして類似度を保存していく
#類似度が高い順に書き出す
for name in list_name[900:1000]:
    os.chdir("C:\\Users\\Owner\\python_practice\\spring_all\\cosine_value")
    with open(name+"_cosine.csv", "w", encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        value = Similarity_value(list_name, name) 
        value.calculate() #類似度を計算し辞書として格納
        result1 = value.result #類似度が入っているのはresult
        result2 = sorted(result1.items(), key=lambda x:x[1], reverse=True) #類似度の高い順に並び替える
        for item in result2: #kは温泉の名前、vは類似度
            k = item[0]
            v = item[1]
            row = [k,v]
            writer.writerow(row)
        f.flush()



