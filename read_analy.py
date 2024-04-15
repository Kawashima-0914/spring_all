#温泉の情報のテキストファイルを取得し形態素分析を行い、その結果をテキストファイルに保存。
#保存場所はspring_feature_list

import MeCab
import os
from make_list1 import List_make

#温泉の名前を保存
inf = List_make()
inf.list_operate()
list_name = inf.name


exclude_word_list = [
    "分", "時間", "秒", "自動車道", "ＩＣ", "年", "％", "m", "種類", 
    "種", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "曜日",
    "１", "２", "３", "４", "５", "６", "７", "８", "９","０"
    ] #意味がなさそうな言葉で、ファイルでは対応できないもの


target_parts = [ #意味がありそうな単語の品詞
    "名詞"
]

with open('splitfile.txt', 'r', encoding='UTF-8') as f:
    stop_words = f.read().splitlines() #一般的に不要な単語を格納

#形態素解析にはNEologdを使用
tagger = MeCab.Tagger(' -d "C:\\MeCab\\dic\\ipadic" -u "C:\\MeCab\\dic\\NEologd.dic"')
def extraction(text): #テキストを形態素解析して意味がある単語だけ取り出す関数
    flag = 0 #ワードをリストに格納して良い時は0
    flag_pH = 0
    result_word = [] #意味がありそうな単語を格納するリスト
    word_bank = '' #pHの値を取り込むため
    for line in tagger.parse(text).splitlines():
        if line is None or line == '' or line == 'EOS'or len(line.split()) < 2:
            continue
        for target in target_parts:
            if target in line.split()[1]:
                word = line.split()[0]
                if(word == 'pH' or word=='PH'): #pHの値だけは例外で取り込む
                    flag_pH = 1
                    break
                elif(flag_pH==1 or flag_pH==2):
                    if("." in word):#pH=9.0などの時、9.が数字として判定されないので、"."で判別してある場合はflag_pHに2をたてる
                        word_bank = word
                        flag_pH = 2
                        break
                    elif(flag_pH==2):#flag_pHが2の場合wordにはpHとpHの値を足した物を入れる
                        word = 'pH'+word_bank+word
                        flag_pH = 0
                        result_word.append(word)
                        break
                    elif(word.isnumeric()):#ここのifの分岐までくれば、pHの値が整数であることを示す
                        word = 'pH'+ word
                        flag_pH = 0
                        result_word.append(word)
                        break
                elif not word in stop_words: #不要な語として登録したものに該当しない場合
                    for ex_word in exclude_word_list: #不要語とし登録していないもので、不要なものを除去するため
                        if ex_word in word:
                            flag = 1
                    if flag == 0:
                        result_word.append(word)
                    flag = 0
    return result_word
                        
def write_file(list, file): #配列の要素をファイルに書き込むための関数
    for d in list:
        file.write(d+"、")
    file.write("\n")


#温泉の情報を解析してテキストファイルに格納
for name in list_name:
    #カレントディレクトリを移動する
    os.chdir("C:\\Users\\Owner\\python_practice\\spring_all\\spring_feature2")
    f = open(name+'.txt', 'r', encoding='UTF-8')#温泉の情報が書いてあるファイルを読み込む
    datalist = f.readlines() #全ての情報をリストに代入
    list_len = len(datalist) #情報がいくつあるかを格納
    content_title = datalist[0] #温泉の説明の見出し
    content = datalist[1] #温泉の説明
    quality_content = datalist[2] #温泉の泉質の説明
    if(list_len >= 4):
        quality = datalist[3] #温泉の泉質の名称か効能
        if("など" in quality):
            quality = quality.replace("など", "")
        if(list_len == 5):
            efficacy = datalist[4] #温泉の効能
            if("など" in efficacy):
                efficacy = efficacy.replace("など", "")
    f.close()
    
    content = content_title + content #温泉の説明の見出しと説明を合体
    
    result_feature = extraction(content) #温泉の説明の単語抽出した物のリスト
    result_qualisty = extraction(quality_content) #温泉の泉質の単語抽出した物のリスト

    #カレントディレクトリを移動する
    #ファイルへの書き込み
    os.chdir("C:\\Users\\Owner\\python_practice\\spring_all\\spring_feature_list")
    f = open(name+'_analy.txt', 'w', encoding='UTF-8')
    write_file(result_feature, f)
    write_file(result_qualisty, f)
    if(list_len >= 4):
        f.write(quality)
        if(list_len == 5):
            f.write(efficacy)
    f.close()











                    