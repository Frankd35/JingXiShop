import pandas as pd
import pymysql
import random

#读取数据
test_data = pd.read_csv(r'D:\JXproject\WebProject\read_csv\7.csv')   # <- 文件路径，每次需要修改
test_data.head()
#连接数据库
db = pymysql.connect(host="139.9.247.4", user="root", passwd="JXsc12345",db="jxdb",charset='utf8')
#定义操作函数
def insert_test_data():
    liData = []
    cateId = 7    # <- 分类id，每次需要修改
    startId = 532   # <- 前置id，每次需要修改
    num = 0
    cursor = db.cursor()
    # 利用shape的第一个元素来获取数据的数量
    for i in range(0,test_data.shape[0]):
        # 获取第每行数据
        line_data = test_data.iloc[i]
         #读取第每行中每列数据
        id = i+startId
        # 第[1]项为目录id，每次 ↓ 录入不同目录需要修改其值
        value = (str(id),str(cateId),str(line_data[3]),str(line_data[2]),str(line_data[5]),str(line_data[4]),str("地球高质量商品"),
                 str(1),str(4),str(random.randint(0,10000)))
        liData.append(value)
        num +=1
        print(value)
        if num == test_data.shape[0]:
            sql = "INSERT INTO goods_goods(id,category_id,name,price,number,img,text,status,shop_id,searching_num)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.executemany(sql, liData)  # 执行sql语句
            db.commit()
            num = 0  # 计数归零
            liData.clear()  # 清空list
    print("插入成功")
    cursor.close()
    db.close()

#执行函数
insert_test_data()