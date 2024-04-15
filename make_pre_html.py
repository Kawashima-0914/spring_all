#都道府県ごとのhtmlファイルを作成する
#それぞれの都道府県の温泉地の情報(画像、名前etc)からhtmlファイルを作成する
#作成したhtmlファイルはtemplates/prefecturesに格納
import os
import csv
import bs4
import pykakasi
from make_list1 import List_make #温泉地の名前、場所、画像url取得

soup = bs4.BeautifulSoup('', 'html.parser')


List_spring = List_make()
List_spring.list_operate()
location_all = List_spring.location

#都道府県の配列を作る(温泉が格納されているcsvファイルにアクセスして所在地として取り出す)
pre_list = []
for location in location_all:
    if not location in pre_list:
            pre_list.append(location)


def make_pre_html(base):
    same_judge = []
    for pre in pre_list:
        os.chdir("C:\\Users\\Owner\\python_practice\\spring_all\\prefecture")
        with open(pre+".csv", "r", encoding="UTF-8") as f: #県ごとの情報(温泉の名前と画像url)
            datalist = f.readlines()
            #漢字、ひらがな、カタカナをローマ字に変換
            kakasi = pykakasi.kakasi()
            kakasi.setMode('J', 'a') #漢字→ローマ字
            kakasi.setMode('K', 'a') #カタカナ→ローマ字
            kakasi.setMode('H', 'a') #ひらがな→ローマ字
            conversion = kakasi.getConverter()
            pref_name = conversion.do(pre)
            pref_name = pref_name.replace('ken', '') #htmlの名前にはkenを含ませないので除去
            os.chdir("C:\\Users\\Owner\\python_practice\\springproject\\templates\\prefectures")
            with open(pref_name+'.html', 'w', encoding="UTF-8") as t: #県ごとのhtmlファイルに書き出していく
                t.write(base)   #baseとなる部分を書き出す

                h_tag = soup.new_tag('h2') #見出しの部分(~県)
                h_tag['class'] = 'icon'
                h_tag.string = pre 
                t.write(str(h_tag))  

                i = 1
                for data in datalist: #県ごとに格納されている温泉の名前と画像urlを扱う
                    data = data.replace("\n", "")
                    data = data.split(',')
                    if i % 2:
                        data_name = data[0].split('（') #温泉の読み方の部分と漢字の部分で分かる
                        spring_name = conversion.do(data_name[0]) #温泉の名前をローマ字に変換
                        #htmlのファイル名として使えない物を除去
                        spring_name = spring_name.replace("'", '')
                        spring_name = spring_name.replace(" ", '')
                        spring_name = spring_name.replace(".", '')

                        if len(data_name) == 2: #温泉の読み方の部分がある場合
                            spring_name2 = data_name[1] #温泉の読み方の部分を格納
                            spring_name2 = conversion.do(spring_name2) #ローマ字に変換
                            #不要な物は除去
                            spring_name2 = spring_name2.replace('）', '')
                            spring_name2 = spring_name2.replace("'", '')
                            spring_name2 = spring_name2.replace(" ", '')
                            spring_name2 = spring_name2.replace(".", '')
                        else:
                            spring_name2 = '1' #読み方がない場合は'1'を格納
                        
                        total_name = spring_name+spring_name2+pref_name #totalの名前として、漢字+読み方+県
                        if total_name in same_judge: #同じtotalがないかを調べる
                            spring_name2 = '2' #同じtotalがある場合、読み方の部分を2とする
                        same_judge.append(total_name) #totalを格納していく


                        form_tag = soup.new_tag('form') #画像から温泉の特徴に飛ぶためのform
                        form_tag['name'] = spring_name + '_' + spring_name2 + '_' + pref_name
                        form_tag['action'] = "{% url 'appname:springs' %}" #情報をpostする場所
                        form_tag['method'] = "post" 
                        form_tag.string = "\n{% csrf_token %}" #postする際のまじない

                        input_tag = soup.new_tag('input') #input_tagのvalueをview.pyで受け取る
                        input_tag['type'] = "hidden"
                        input_tag['name'] = "id2"
                        input_tag['value'] = spring_name + "_" + spring_name2 + "_" + pref_name #valueは温泉の名前(ローマ字)

                        div_tag = soup.new_tag('div') #divは画像や温泉名の実際の表示の際にcssで扱いやすくするため
                        div_tag['class'] = 'con'

                        p_tag = soup.new_tag('p') #温泉の名前をpタグとして格納
                        p_tag.string = data_name[0]

                        a_tag = soup.new_tag('a') #遷移先のurl
                        a_tag['href'] = './spring_each/'
                        a_tag['onclick'] = "document."+spring_name + "_" + spring_name2 + "_" + pref_name+".submit(); return false;" #画像をクリックした際の動作(javascript)

                        img_tag = soup.new_tag('img')  #画像のurlを格納していく
                        img_tag['class'] = 'spring_img'
                        img_tag['src'] = data[1]
                        a_tag.append(img_tag)

                        div_tag.append(a_tag) #divの中にaタグ→pタグの順に格納
                        div_tag.append(p_tag)

                        form_tag.append(input_tag) #formタグの中にinputタグ→div_tagの順にを格納
                        form_tag.append(div_tag) 

                        t.write(str(form_tag)) #以上のタグを書き出す
                    i += 1
                t.write("\n{% endblock content %}") #htmlの締めの部分を書き出す
    
base = """
{% extends 'base-prefecture.html' %}\n
{% block header %}\n
{% endblock header %}\n
{% block content %}\n
"""

make_pre_html(base)
