#それぞれの温泉地のhtmlファイルを作成する
#画像、概要、泉質、効能を含む
#作成したhtmlファイルはtemplates/spring_eachに格納

import os
import csv
import bs4
import pykakasi
from make_list1 import List_make #温泉地の名前、場所、画像url取得
from make_list_overview import List_inf #温泉地の名前から温泉の概要などの情報を取得するためのクラス

soup = bs4.BeautifulSoup('', 'html.parser')

quality_kinds = [
    "単純温泉", "塩化物泉", "炭酸水素塩泉", "硫酸塩泉",
    "二酸化炭素泉", "含鉄泉", "硫黄泉", "酸性泉", "ラジウム泉"
    ]

#泉質が含まれるかどうかを判定する関数
#含まれる場合は1、そうでない場合は0
def quality_is(datalist):
    quality = datalist[3].split("、")
    quality_len = len(quality)
    for j in range(quality_len):
        quality_item = quality[j-1]
        if quality_item in quality_kinds:
            return 1
    return 0


def get_spring_inf(get_name): #温泉の名前から、その温泉の名前、画像url、所在地(県)の情報を返す関数
    get_inf = []
    for name, image, location in zip(spring_name, image_link, spring_location):
        if name == get_name:
            get_inf.append(name)
            get_inf.append(image)
            get_inf.append(location)
            return get_inf
        

#温泉地の名前と画像の配列を作る
os.chdir("C:\\Users\\Owner\\python_practice\\spring_all") 
spring_name = []
image_link = []
List_spring = List_make()
List_spring.list_operate()
#全ての温泉の名前、画像url、所在地(県)を取得
spring_name = List_spring.name
image_link = List_spring.image
spring_location = List_spring.location


#名前と画像の確認
#print(spring_name)
#print(image_link)

def make_spring_html(base):
    same_judge = []
    for (spring, image, location) in zip(spring_name, image_link, spring_location): 
        #漢字、ひらがな、カタカナをローマ字に変換
        kakasi = pykakasi.kakasi()
        kakasi.setMode('J', 'a') #漢字→ローマ字
        kakasi.setMode('K', 'a') #カタカナ→ローマ字
        kakasi.setMode('H', 'a') #ひらがな→ローマ字
        conversion = kakasi.getConverter()
        name_data = spring.split('（') #温泉の名前で漢字の部分と、読み方の部分で分ける

        spring_name_con = conversion.do(name_data[0]) #温泉の漢字の部分をローマ字に変換して格納
        #htmlファイルとして使えない物を除去
        spring_name_con = spring_name_con.replace("'", '')
        spring_name_con = spring_name_con.replace(" ", '')
        spring_name_con = spring_name_con.replace(".", '')

        if len(name_data) == 2: #温泉の名前で、漢字の部分と読み方の部分があるとき
            spring_name_con2 = name_data[1] #温泉名の読み方の部分を取得
            spring_name_con2 = conversion.do(spring_name_con2)  
            #不要な物を除去
            spring_name_con2 = spring_name_con2.replace('）', '')
            spring_name_con2 = spring_name_con2.replace("'", '')
            spring_name_con2 = spring_name_con2.replace(" ", '')
            spring_name_con2 = spring_name_con2.replace(".", '')
        else:
            spring_name_con2 = '1' #温泉の名前で、読み方の部分がないときは代わりに1を格納

        loc_name_con = conversion.do(location)
        loc_name_con = loc_name_con.replace('ken', '') #htmlの名前にはkenを含ませないので除去

        total_name = spring_name_con + spring_name_con2 + loc_name_con #totalの名前として、漢字+読み方+県
        if total_name in same_judge: #同じtotalがないかを調べる
            spring_name_con2 = '2' #同じtotalがある場合、読み方の部分を2とする
        same_judge.append(total_name) #totalを格納していく
        os.chdir("C:\\Users\\Owner\\python_practice\\springproject\\templates\\spring_each")
        #それぞれの温泉のhtmlファイルを開き、htmlを作成していく
        with open(spring_name_con+"_"+spring_name_con2+"_"+loc_name_con+'.html', 'w', encoding="UTF-8") as f:
            f.write(base) #baseの書き出し
            h2_tag = soup.new_tag('h2') #見出しの作成
            h2_tag['class'] = 'icon'
            h2_tag.string = spring 
            f.write(str(h2_tag))

            h3_tag = soup.new_tag('h3') #見出し(所在地)の作成
            h3_tag['class'] = 'icon'
            h3_tag.string = " 所在地：" + location
            f.write(str(h3_tag))

            #温泉地の概要など情報を取得
            os.chdir("C:\\Users\\Owner\\python_practice\\spring_all\\spring_feature2")
            inf_list = List_inf(spring)
            inf_list.inf_get()
            datalist = inf_list.spring_inf
            len_datalist = len(datalist)
            
            #divタグを作成
            #div_tagは画像と泉質、効能の表
            #div_tag1は概要などの説明
            div_tag = soup.new_tag('div')
            div_tag['class'] = 'con'
            div_tag1 = soup.new_tag('div')
            div_tag1['class'] ='con1'

            if len_datalist > 3: #泉質、効能が含まれる場合
                table_tag = soup.new_tag('table') 
                tr_tag = soup.new_tag('tr')
                quality_flag = 0
                quality_flag = quality_is(datalist) #泉質があるかどうかを判定
                if quality_flag == 1: #泉質がある場合
                    th_tag = soup.new_tag('th')
                    th_tag.string = "泉質"
                    td_tag = soup.new_tag('td')
                    td_tag.string = datalist[3]
                    tr_tag.append(th_tag)
                    tr_tag.append(td_tag)
                    table_tag.append(tr_tag)
                    if len_datalist == 5: #泉質もあり、効能もある場合
                        th1_tag = soup.new_tag('th')
                        th1_tag.string = '効能'
                        td1_tag = soup.new_tag('td')
                        td1_tag.string = datalist[4]
                        tr1_tag = soup.new_tag('tr')
                        tr1_tag.append(th1_tag)
                        tr1_tag.append(td1_tag)
                        table_tag.append(tr1_tag)
                else: #効能のみある場合
                    th_tag = soup.new_tag('th')
                    th_tag.string = "効能"
                    td_tag = soup.new_tag('td')
                    td_tag.string = datalist[3]
                    tr_tag.append(th_tag)
                    tr_tag.append(td_tag)
                    table_tag.append(tr_tag)
                
            #表示するhtmlの温泉のimgを作成
            img_tag = soup.new_tag('img')
            img_tag['class'] = 'spring_img'
            img_tag['src'] = image

            #温泉の概要などの説明を作成
            p_tag = soup.new_tag('p')
            p_tag['class'] = 'feature'
            p_tag.string = datalist[1] + datalist[2]


            div_tag.append(img_tag)
            if len_datalist > 3:
                div_tag.append(table_tag)
            div_tag1.append(p_tag)
            f.write(str(div_tag))
            f.write(str(div_tag1))

             #似ている温泉を表示するためのコード

            h2_tag = soup.new_tag('h2') #見出しを作成
            h2_tag['class'] = 'icon'
            h2_tag.string = '似ている温泉' 
            f.write(str(h2_tag))

            #該当の温泉のそれぞれの温泉に対する類似度を取得
            os.chdir("C:\\Users\\Owner\\python_practice\\spring_all\\cosine_all")
            with open(spring+'_cosine.csv', 'r', encoding="UTF-8") as t:
                reader = csv.reader(t)
                i=0
                j=0
                similar_same = []
                for data in reader:
                    if i!=2 and i%2==0 and i!=0:
                        float_ope = "{:.3f}".format(float(data[1])) #類似度を小数点3桁で切る
                        get_inf = get_spring_inf(data[0]) #温泉の名前から、名前、画像url、所在地を取得


                        similar_pref = conversion.do(get_inf[2]) #所在地
                        similar_pref = similar_pref.replace('ken', '')

                        similar_name_origin = data[0].split('（') #名前を漢字と読み方の部分に分割
                        #以下totalの部分まで、上部と同じ
                        similar_name = conversion.do(similar_name_origin[0])
                        similar_name = similar_name.replace("'", '')
                        similar_name = similar_name.replace(" ", '')
                        similar_name = similar_name.replace(".", '')

                        if len(similar_name_origin) == 2:
                            similar_name2 = similar_name_origin[1]
                            similar_name2 = conversion.do(similar_name2)
                            similar_name2 = similar_name2.replace('）', '')
                            similar_name2 = similar_name2.replace("'", '')
                            similar_name2 = similar_name2.replace(" ", '')
                            similar_name2 = similar_name2.replace(".", '')
                        else:
                            similar_name2 = '1'

                        total_similar_name = similar_name + similar_name2 + similar_pref 
                        if total_similar_name in similar_same:
                            similar_name2 = '2'
                        similar_same.append(total_similar_name)


                        form_tag = soup.new_tag('form') #formタグで、似ている温泉をクリックしたときに遷移させる
                        form_tag['name'] = similar_name+"_"+similar_name2+"_"+similar_pref  #情報を送る際に他の温泉と区別するため
                        form_tag['action'] = "{% url 'appname:springs' %}" #受け取る場所を定義
                        form_tag['method'] = "post" #postさせるため
                        form_tag.string = "\n{% csrf_token %}"

                        input_tag = soup.new_tag('input') #inputタグ作成。valueがviewsで受け取る値に該当する
                        input_tag['type'] = "hidden" #実際のページには見えないように
                        input_tag['name'] = "id2" #id2の名前で値を取得
                        input_tag['value'] = similar_name+"_"+similar_name2+"_"+similar_pref

                        div_tag2 = soup.new_tag('div') #divタグ作成
                        div_tag2['class'] = 'con2'

                        p_tag.string = get_inf[0]  #温泉の名前
                        br_tag = soup.new_tag('br')
                        br_tag.string = '類似度:' + float_ope #類似度
                        p_tag.append(br_tag) #温泉の名前と類似度をpタグで改行させて表示する
                        
                        a_tag = soup.new_tag('a') #画像からリンクさせるため
                        a_tag['href'] = '../spring_each/'
                        a_tag['onclick'] = "document."+similar_name+"_"+similar_name2+"_"+similar_pref+".submit(); return false;"

                        img_tag['src'] = get_inf[1]

                        a_tag.append(img_tag)

                        div_tag2.append(a_tag)
                        div_tag2.append(p_tag)

                        form_tag.append(input_tag)
                        form_tag.append(div_tag2)

                        f.write(str(form_tag))
                        j += 1
                    i += 1
                    if j==4: #似ている温泉を4つ表示したら終了
                        break

            f.write("\n{% endblock content %}")
    


        
        
        
base = """
{% extends 'base-spring-each.html' %}\n
{% block header %}\n
{% endblock header %}\n
{% block content %}\n
"""

make_spring_html(base)