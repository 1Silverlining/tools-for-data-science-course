import os
import pymongo
from pyecharts import Line, Bar

cur = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = cur['jane']
cur = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = cur['jane']
start_dict = {
            '美妆': ['口红', '粉底', '眉笔', '眼影', '遮暇'],
            '食品': ['辣条', '鸭脖', '薯片', '可乐', '瓜子'],
            '电子产品': ['手机', '耳机', '平板', '笔记本电脑', '音响'],
            '家电': ['冰箱', '空调', '洗衣机', '电视', '扫地机器人'],
            '包': ['行李箱', '双肩包', '挎包', '钱包', '电脑包']
        }
for type, categorys in start_dict.items():
    os.makedirs('./{}'.format(type))
    item_list = list()
    x_list = list()
    for category in categorys:
        # 根据品类获取数据
        type_data = [i for i in db['clean_data'].find({"product_category": category})]
        # 根据品类按照好评数进行排序
        type_data.sort(key=lambda x: x["GoodRate"]*x['CommentCount'])
        # 品类数据分类添加
        x_list_category = [
            "产品id:" + str(i.get('_id'))
            + "|" + "价格:" + i.get("product_price")
            + "|" + "店名:" + i.get("product_shop_name") if i.get("product_shop_name") else ''
            for i in type_data]
        item_list_category = [i["GoodRate"]*i['CommentCount'] for i in type_data]
        # 对品类下所有产品进行作图
        bar_category = Bar("{}领域-{}_品类优选分析".format(type, category))
        bar_category.add("{}_品类优选分析".format(category), x_list_category, item_list_category, interval=0, xaxis_rotate=-40)
        bar_category.render('./{}/{}_品类最佳优选.html'.format(type, category))
        data = (type_data[-1])
        if not type_data[-1].get("product_shop_name"):
            data['product_shop_name'] = ''
        # 领域数据添加
        item_list.append((data))
        x_list.append(category+'|'+"产品id:"+str(data.get('_id'))
                      +"|"+"价格:"+data.get("product_price")
                      + "|" + "店名:" + data.get("product_shop_name")
                      )
    item_list = [i["GoodRate"]*i['CommentCount'] for i in item_list]
    # 获取领域下最优选，画图
    bar = Bar("{}_领域各品类最佳优选".format(type))
    bar.add("最佳优选", x_list, item_list, interval=0, xaxis_rotate=-40)
    bar.render('./{}/{}_领域品类最佳优选.html'.format(type, type))

