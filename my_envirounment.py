import pandas as pd
import requests  as re
import json
import pinyin
import numpy as np

file_path = '.\\areaid.csv'
#将城市名称转换成环境云网站提供的城市代码
def city2code(cityname):
    csv_file = pd.read_csv(file_path)
    list_index = [i for i in csv_file.NAMEEN]
    csv_file.index = list_index
    csv_file1 = csv_file.drop(['NAMECN'], axis = 1)
    value = csv_file1.at[cityname, 'AREAID']
    if type(value) is np.int64:
        return value
    else:
        return value[0]

#使用pandas读取excel文件，返回省份对应市区，市区对应县区的两个字典
def palceName():
    csv_file = pd.read_csv(file_path)
    list_index = [i for i in csv_file.NAMEEN]
    csv_file.index = list_index
    csv_file1 = csv_file.drop(['NAMEEN'], axis = 1)
    list_P = csv_file1.PROVCN
    list_D = csv_file1.DISTRICTCN
    Shengfen_1 = set(i for i in list_P)
    Shengfen = list(Shengfen_1)
    list1_W = []
    for i in Shengfen:
        csv_file_c = csv_file.copy()
        csv_file_c.index = [i for i in csv_file_c.PROVEN]
        shenfen_py = pinyin.get(i, format="strip", delimiter="")
        if i == '陕西':
            shenfen_py = 'shan-xi'
        csv_file_c_s =  csv_file_c.loc[shenfen_py,'DISTRICTCN']
        set_F = set(csv_file_c_s)
        list_f = [i for i in set_F]
        list1_W.append(list_f)
    dict_1 = dict(zip(Shengfen,list1_W))
    Shiqu_1 =  set(i for i in list_D)
    Shiqu = list(i for i in Shiqu_1)
    list1_N = []
    for i in Shiqu:
        csv_file_c_f = csv_file.copy()
        csv_file_c_f.index = [i for i in csv_file.DISTRICTEN]
        shiqu_py = pinyin.get(i, format="strip", delimiter="")
        csv_file_c_s = csv_file_c_f.loc[shiqu_py, 'NAMECN']
        if type(csv_file_c_s) is str:
            str_list = [csv_file_c_s]
            list1_N.append(str_list)
        else:
            set_g = set(csv_file_c_s)
            list_q = [i for i in set_g]
            list1_N.append(list_q)
    dict_2 = dict(zip(Shiqu, list1_N))
    return dict_1,dict_2

#向环境云网站request选中城市的未来十五天的天气预报。
def weather_forecast(cityname):
    name_py = pinyin.get(cityname, format="strip", delimiter="")
    citycode_f = city2code(name_py)
    citycode = citycode_f
    url = 'http://service.envicloud.cn:8082/v2/weatherforecast/AMFJAY1JYWKXNTQYOTCXMJK2NZM0/%s'%citycode
    payload = ""
    headers = {
        'cache-control': "no-cache"
    }

    response = re.request("GET", url, data=payload, headers=headers)
    return json.loads(response.text)

#向环境云网站request选中城市的过去24小时的天气。
def weather_history(cityname):
    name_py = pinyin.get(cityname, format="strip", delimiter="")
    citycode = city2code(name_py)
    url = 'http://service.envicloud.cn:8082/v2/weatherhistory/AMFJAY1JYWKXNTQYOTCXMJK2NZM0/%s' % citycode
    payload = ""
    headers = {
        'cache-control': "no-cache"
    }

    response = re.request("GET", url, data=payload, headers=headers)
    return json.loads(response.text)


#向环境云网站request选中城市和年份的月度天气
def weather_month_history(city,year):
    name_py = pinyin.get(city, format="strip", delimiter="")
    citycode = city2code(name_py)
    url = 'http://service.envicloud.cn:8082/v2/monthlymete/AMFJAY1JYWKXNTQYOTCXMJK2NZM0/%s/%s' % (citycode,year)
    payload = ""
    headers = {
        'cache-control': "no-cache"
    }
    response = re.request("GET", url, data=payload, headers=headers)
    return json.loads(response.text)

#向环境云网站request指定城市和指定日期的天气情况
def weather_date_history(city,date):
    name_py = pinyin.get(city, format="strip", delimiter="")
    citycode = city2code(name_py)
    url = 'http://service.envicloud.cn:8082/v2/weatherhistory/AMFJAY1JYWKXNTQYOTCXMJK2NZM0/%s/%s' % (citycode,date)
    payload = ""
    headers = {
        'cache-control': "no-cache"
    }
    response = re.request("GET", url, data=payload, headers=headers)
    return json.loads(response.text)

def isyear(year): #判断该年份是否是闰年
    if  (year %4 == 0 and year %100 != 0) or year %400 == 0:
        return True
    else:
        return False

def month2day(city,month,year): #该函数可以获取指定月份每一天的天气数据
    r_value = []
    month_arr = [1,3,5,7,8,10,12]
    year_str = str(year)
    if month < 10:
        month_str = '0'+str(month)
    else:
        month_str = str(month)
    if(month == 2 and isyear(year)):
        dead_line = 30
    elif(month == 2 and isyear(year) == False):
        dead_line = 29
    elif month in  month_arr:
        dead_line = 32
    else:
        dead_line = 31
    for i in range(1,dead_line):
        if i < 10:
            data_str = '0' + str(i)
        else:
            data_str = str(i)
        time = int(year_str + month_str + data_str)
        mon2day_eve = weather_date_history(city, time)
        if mon2day_eve['rcode'] == 203:
            break
        elif mon2day_eve['rcode'] == 202 :
            break
        else:
            r_value.append(mon2day_eve)
    return r_value

def Base1_huanbi(city_array,S_choise):  #地域环比的公用接口函数1
    #对于地域环比中天气预报选项的处理
    R_cityArr_weatherForecast = []
    for city in city_array:
        forecast = weather_forecast(city)
        if "forecast" not in forecast:
            continue
        city_forecast = forecast["forecast"]
        if len(city_forecast) < S_choise:
            continue
        R_cityArr_weatherForecast.append(city_forecast[S_choise-1])
    return R_cityArr_weatherForecast

def Base2_huanbi(city_array,year,Y_choise):# 地域环比的公用接口函数2
    # 对于地域环比中历史年度数据的处理
    R_cityArr_weatherMonthHistory = []
    for city in city_array:
        month_history = weather_month_history(city,year)
        if "info" not in month_history:
            continue
        city_month_history = month_history["info"]
        R_cityArr_weatherMonthHistory.append(city_month_history[Y_choise-1])
    return R_cityArr_weatherMonthHistory

def Base3_huanbi(city_array,data): #地域环比的公用接口函数3
    R_cityArr_weather_date_history = []
    for city in city_array:
        date_history = weather_date_history(city,data)
        if date_history['rcode'] == 203:
            break
        elif date_history['rcode'] == 202 :
            break
        R_cityArr_weather_date_history.append(date_history)
    return R_cityArr_weather_date_history

#地域环比的入口函数
def diyu_huanbi(choise,city_array,S_choise,year,Y_choise,data):
    if choise  == 1:
       return Base1_huanbi(city_array,S_choise)
    elif choise  == 2:
        return  Base2_huanbi(city_array,year,Y_choise)
    else:
        return Base3_huanbi(city_array,data)

#时间同比的入口函数
def city_tongbi(cityname,years,month):
    city_tongbi_Arr = []
    M_years = years
    cout_year = 2015
    while(M_years > 0):
        history = weather_month_history(cityname,cout_year)
        if "info" not in history:
            cout_year -= 1
            M_years -= 1
            continue
        month_history = history["info"]
        city_tongbi_Arr.append(month_history[month-1])
        cout_year-=1
        M_years-=1
    return city_tongbi_Arr

#返回省和省会城市的字典
def ShengandCity():
    shengfenCitydict = {'北京':'北京','上海':'上海','天津':'天津','重庆':'重庆','黑龙江':'哈尔滨','吉林':'长春','辽宁':'沈阳','内蒙古':'呼和浩特','河北':'石家庄','山西':'太原','陕西':'西安','山东':'济南','新疆':'乌鲁木齐','西藏':'拉萨','青海':'西宁','甘肃':'兰州','宁夏':'银川','河南':'郑州','江苏':'南京','湖北':'武汉','浙江':'杭州','安徽':'合肥','福建':'福州','江西':'南昌','湖南':'长沙','贵州':'贵阳','四川':'成都','广东':'广州','云南':'昆明','广西':'南宁','海南':'海口','香港':'香港','澳门':'澳门','台湾':'台北'}
    return shengfenCitydict

#以下为测试代码
if __name__ == '__main__':
    # name = '北京'
    # Mlist = list(palceName())
    # Mdict0 = Mlist[0]
    # Mlist1 = Mdict0.values()
    # list1 = []
    # for i in Mlist1:
    #     list1 +=i
    # csv_file = pd.read_csv(file_path)
    # list_B = csv_file.loc[:,['DISTRICTEN']]
    # list2_before =set([i for i in list_B.DISTRICTEN])
    # list2 = [i for i in list2_before]
    # for i in range(len(list1)):
    #     shiqu_py = pinyin.get(list1[i], format="strip", delimiter="")
    #     if shiqu_py not in list2:
    #             print(list1[i],shiqu_py)
    # print(list2)
    # print(list1)
    #name_py = pinyin.get(name, format="strip", delimiter="")
    #help()
    # w = weather_date_history(name,20170722)
    # print(w)
    #w1 = json.loads(w) #将文本格式转化为字典格式
    # for i in w1:
    #      print(i)
    # print(w1['rdesc'])
    #palceName()
    # Y = palceName()
    # print(w)
    # 1961-2015年都有数据
    # 2015年八月份开始到现在有相关数据
    data = weather_history('南京')
    print(data)