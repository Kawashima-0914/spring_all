#他で使用するための定義
import csv

#温泉の名前が入っているファイルを読み込み、名前、url、画像のurl、所在地(県)を取得するためのクラス
class List_make:
    name = []
    url = []
    image = []
    location = []
    
    def list_operate(self):
        with open('all_spring.csv', encoding='UTF-8') as f:
            reader = csv.reader(f)   
            i = 0
            for line in reader: #iによってランキングの1つずつを取り込む
                if(i!= 0):        
                    keyword = line[0]
                    loc = line[1]
                    urlinf = line[3]
                    imginf = line[4]
                    #不要な文字を除去する
                    keyword = keyword.replace('\u3000', '')
                    keyword = keyword.replace(' ', '')
                    keyword = keyword.replace('/', ',') #ファイルの名前として使えない文字を除去
                    if keyword in self.name: #同じ漢字で読み方も同じ際、後に出てきた温泉を格納する(前に出てきた温泉は除去)
                        #print(keyword)
                        j = self.name.index(keyword)
                        self.name[j] = keyword
                        self.location[j] = loc
                        self.url[j] = urlinf
                        self.image[j] = imginf
                    else:
                        self.name.append(keyword)   
                        self.location.append(loc)
                        self.url.append(urlinf)
                        self.image.append(imginf)
                i += 1



#list = List_make()
#list.list_operate()
#print(len(list.name))