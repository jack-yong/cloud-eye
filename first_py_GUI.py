import wx
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import my_envirounment

ID_EVENT_REFRESH = 9999
class MyfirstFram(wx.Frame,):
    def __init__(self, superior):

        #程序中需要用到的基本变量
        self._ShengFen = '江苏'
        self._ShiQu = '南京'
        self._cityname = '南京'
        self._year = '2015'
        self._month = '1'
        self._day = '1'
        self._TheDayOf = '1'
        self._time = '20170512'
        self._menuopetion = -1
        self._data = {}
        self._Dataframe = {}
        self._forecas_upcity = []
        self._forecas_city = []
        self._forecas_date = []
        self._forecas_spd = []
        self._forecas_hum = []
        self._forecas_uv = []
        self._forecas_min = []
        self._forecas_max = []
        self._forecas_pop = []
        self._forecas_vis = []
        self._forecas_cond_n = []
        self._forecas_cond_d = []
        self._forecas_dir = []
        self._forecas_sc = []
        self._Dhistory_city = []
        self._Dhistory_updatetime = []
        self._Dhistory_temperature = []
        self._Dhistory_phenomena = []
        self._Dhistory_feelst = []
        self._Dhistory_humidity = []
        self._Dhistory_rain = []
        self._Dhistory_winddirect = []
        self._Dhistory_windpower = []
        self._Dhistory_windspeed = []
        self._Mhistory_upcity = []
        self._Mhistory_city = []
        self._Mhistory_year = []
        self._Mhistory_month = []
        self._Mhistory_tem_max = []
        self._Mhistory_pre = []
        self._Mhistory_tem_min = []
        self._Mhistory_tem_avg = []
        self._Yhistory_upcity = []
        self._Yhistory_city = []
        self._Yhistory_date = []
        self._Yhistory_sunny_percent = []
        self._Yhistory_rain_percent = []
        self._Yhistory_rain_full = []
        self._Yhistory_hum_avg = []
        self._Yhistory_tem_max = []
        self._Yhistory_tem_min = []
        self._Yhistory_tem_avg = []
        self._Yhistory_wdir_most = []
        self._Yhistory_wspd_avg = []

        #获取省份:市区 和 市区:县区字典
        list_f = list(my_envirounment.palceName())
        dict1 = list_f[0]
        dict2 = list_f[1]

        #菜单栏部分
        wx.Frame.__init__(self, parent=superior, title="观云眼", pos=
        (200, 100), size=(1000, 600))
        self.CreateStatusBar()
        menuBar = wx.MenuBar()
        filemenu = wx.Menu()
        filemenu1 = wx.Menu()
        filemenu2 = wx.Menu()
        filemenu3 = wx.Menu()
        filemenu_S = wx.Menu()
        filemenu_S1 = wx.Menu()
        filemenu_S2 = wx.Menu()
        menuBar.Append(filemenu, "&主菜单")
        menuBar.Append(filemenu1, "&基础查询")
        menuBar.Append(filemenu2, "&地域环比")
        menuBar.Append(filemenu3, "&时间同比")
        myhelp = filemenu.Append(0,"&帮助","获得该软件的帮助信息")
        self.Bind(wx.EVT_MENU, self.helps, myhelp)
        QUit = filemenu.Append(wx.ID_EXIT, "&退出", "")
        self.Bind(wx.EVT_MENU, self.OnQuit, QUit)
        file_save =  filemenu.Append(1,"&保存",'保存当前内容')
        self.Bind(wx.EVT_MENU, self.fileSave, file_save)
        #Analyzer =  filemenu.Append(7,&分析",'分析列表中的数据')
        #self.Bind(wx.EVT_MENU, self.Analyzers, Analyzer)
        menuforecas = filemenu1.Append(2, "&天气预报", "未来七天的天气")
        assert isinstance(menuforecas, object)
        self.Bind(wx.EVT_MENU, self.Befor_forecas, menuforecas)
        menuDhistory = filemenu1.Append(3, "&24小时天气", "过去24小时历史天气")
        self.Bind(wx.EVT_MENU, self.Befor_Dhistory, menuDhistory)
        menuMhistory = filemenu1.Append(4, "&年度月天气"
                                          "", "指定年份月度天气")
        self.Bind(wx.EVT_MENU, self.Befor_Mhistory, menuMhistory)
        menuM_Dhistory = filemenu1.Append(5, "&月度日天气", "指定某一年某个月的历史天气数据")
        self.Bind(wx.EVT_MENU, self.Befor_M_day_historyy, menuM_Dhistory)
        self.menuYhistory = filemenu1.Append(6, "&日天气", "历史某一天天气")
        self.Bind(wx.EVT_MENU, self.Befor_Yhistory, self.menuYhistory)
        self.filemenu_S_foreast = filemenu_S.Append(11,"&天气预报","对所选定的未来第几天的天气预报进行环比")
        self.Bind(wx.EVT_MENU,self.Befor_filemenu_S_Hanbi_foreast, self.filemenu_S_foreast)
        self.filemenu_S_ForYearOfmonth = filemenu_S.Append(12, "&年度月天气", "对所选定的某一年的某个月的历史天气进行环比")
        self.Bind(wx.EVT_MENU, self.Befor_filemenu_S_Hanbi_ForYearOfmonth, self.filemenu_S_ForYearOfmonth)
        self.filemenu_S_ForDay = filemenu_S.Append(13, "&日天气", "对所选定的历史某一天的历史天气进行环比")
        self.Bind(wx.EVT_MENU, self.Befor_filemenu_S_Hanbi_ForDay, self.filemenu_S_ForDay)
        self.filemenu_S1_foreast = filemenu_S1.Append(14,"&天气预报","对所选定的未来第几天的天气预报进行环比")
        self.Bind(wx.EVT_MENU, self.Befor_filemenu_S1_Hanbi_foreast, self.filemenu_S1_foreast)
        self.filemenu_S1_ForYearOfmonth = filemenu_S1.Append(15, "&年度月天气", "对所选定的某一年的某个月的历史天气进行环比")
        self.Bind(wx.EVT_MENU, self.Befor_filemenu_S1_Hanbi_ForYearOfmonth, self.filemenu_S1_ForYearOfmonth)
        self.filemenu_S1_ForDay = filemenu_S1.Append(16, "&日天气", "对所选定的历史某一天的历史天气进行环比")
        self.Bind(wx.EVT_MENU, self.Befor_filemenu_S1_Hanbi_ForDay, self.filemenu_S1_ForDay)
        self.filemenu_S2_foreast =  filemenu_S2.Append(17,"&天气预报","对所选定的未来第几天的天气预报进行环比")
        self.Bind(wx.EVT_MENU, self.Befor_filemenu_S2_Hanbi_foreast, self.filemenu_S2_foreast)
        self.filemenu_S2_ForYearOfmonth = filemenu_S2.Append(18, "&年度月天气", "对所选定的某一年的某个月的历史天气进行环比")
        self.Bind(wx.EVT_MENU, self.Befor_filemenu_S2_Hanbi_ForYearOfmonth, self.filemenu_S2_ForYearOfmonth)
        self.filemenu_S2_ForDay = filemenu_S2.Append(19, "&日天气", "对所选定的历史某一天的历史天气进行环比")
        self.Bind(wx.EVT_MENU, self.Befor_filemenu_S2_Hanbi_ForDay, self.filemenu_S2_ForDay)
        filemenu2.AppendMenu(8,"&县区环比",filemenu_S)
        filemenu2.AppendMenu(9, "&市区环比", filemenu_S1)
        filemenu2.AppendMenu(10, "&省份环比", filemenu_S2)
        self.yearOf5_tongbi = filemenu3.Append(20,"五年同比","对所选定城市2015年之前的五年选定月份进行同比")
        self.Bind(wx.EVT_MENU, self.Befor_Tongbi_YearOf5, self.yearOf5_tongbi)
        self.yearOf15_tongbi = filemenu3.Append(21,"十五年同比","对所选定城市2015年之前的十五年选定月份进行同比")
        self.Bind(wx.EVT_MENU, self.Befor_Tongbi_YearOf15, self.yearOf15_tongbi)
        self.yearOf30_tongbi = filemenu3.Append(22,"三十年同比","对所选定城市2015年之前的三十年选定月份进行同比")
        self.Bind(wx.EVT_MENU, self.Befor_Tongbi_YearOf30,  self.yearOf30_tongbi)
        self.yearOf50_tongbi = filemenu3.Append(23,"五十年同比","对所选定城市2015年之前的五十年选定月份进行同比")
        self.Bind(wx.EVT_MENU, self.Befor_Tongbi_YearOf50,  self.yearOf50_tongbi)
        self.SetMenuBar(menuBar)

        # 控件模块
        self.panel = wx.Panel(self)
        codeSizer = wx.BoxSizer(wx.HORIZONTAL)


        #下拉选框部分
        proviceLable = wx.StaticText(self.panel, -1, "省份:")
        self.__ProvinceComboBox = wx.ComboBox(self.panel, -1, value=list(dict1.keys())[0], choices=list(dict1.keys()),
                                      style=wx.CB_READONLY)

        #定义一级列表刷新时响应二级列表的刷新事件
        self.__SecityDict = dict1
        self.panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected1, self.__ProvinceComboBox,)

        cityLable = wx.StaticText(self.panel, -1, "市区:")
        self.__CityComboBox = wx.ComboBox(self.panel, -1, value=dict1[list(dict1.keys())[0]][0],
                                   choices=dict1[list(dict1.keys())[0]], style=wx.CB_READONLY)

        #定义二级列表的刷新事件
        self.__SecityDict1 = dict2
        self.panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected2, self.__CityComboBox,)

        value1 = dict1[list(dict1.keys())[0]][0]
        xianquLable = wx.StaticText(self.panel, -1, "县区:")
        self._XianquCombobox = wx.ComboBox(self.panel, -1, value=dict2[value1][0],
                                   choices=dict2[value1], style=wx.CB_READONLY)

        #定义三级列表的刷新事件
        self.panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected3, self._XianquCombobox,)

        nianfenlist = [str(i) for i in range(1961,2020)]
        yuefenlist = [str(i) for i in range(1,13)]
        rilist =  [str(i) for i in range(1,32)]
        Thedaylist = [str(i) for i in range(1,8)]
        nianfenLable = wx.StaticText(self.panel, -1, "年份:")
        self.nianfenComboBox = wx.ComboBox(self.panel, -1, value="2019",
                                     choices=nianfenlist, style=wx.CB_READONLY)

        # 定义四级列表的刷新事件
        self.panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected4, self.nianfenComboBox, )

        yuefenLable = wx.StaticText(self.panel, -1, "月份:")
        self.yuefenComboBox = wx.ComboBox(self.panel, -1, value="1",
                                     choices=yuefenlist, style=wx.CB_READONLY)

        # 定义五级列表的刷新事件
        self.panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected5, self.yuefenComboBox, )

        riLable = wx.StaticText(self.panel, -1, "日:")
        self.riComboBox = wx.ComboBox(self.panel, -1, value="1",
                                     choices=rilist, style=wx.CB_READONLY)

        # 定义六级列表的刷新事件
        self.panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected6, self.riComboBox, )

        ThedayLable = wx.StaticText(self.panel, -1, "同比预报第几天:")
        self.ThedayComboBox = wx.ComboBox(self.panel, -1, value="1",
                                     choices= Thedaylist, style=wx.CB_READONLY)

        # 定义七级列表的刷新事件
        self.panel.Bind(wx.EVT_COMBOBOX, self.__OnComboBoxSelected7, self.ThedayComboBox, )

        codeSizer.AddMany([
            (proviceLable, 0,  wx.LEFT), (self.__ProvinceComboBox, 0, wx.LEFT,5)
            , (cityLable, 0, wx.LEFT,10), (self.__CityComboBox, 0, wx.LEFT,5)
            ,(xianquLable, 0, wx.LEFT,10), (self._XianquCombobox, 0, wx.LEFT,5),
            (nianfenLable, 0, wx.LEFT,40), (self.nianfenComboBox, 0, wx.LEFT,5),
            (yuefenLable, 0, wx.LEFT,10), (self.yuefenComboBox, 0, wx.LEFT,5),
            (riLable, 0, wx.LEFT,10), (self.riComboBox, 0, wx.LEFT,5),
            (ThedayLable, 0, wx.LEFT, 40), (self.ThedayComboBox, 0, wx.LEFT, 5),
        ])

        #展示数据部分的sizer
        S_show_mian_data = wx.BoxSizer(wx.HORIZONTAL)

        #分析数据模块的sizer
        anaylse = wx.BoxSizer(wx.VERTICAL)

        # 天气预报静态文本框
        Tanqi_note_Lable = wx.StaticText(self.panel, -1, "天气预报数据区：")
        anaylse.Add(Tanqi_note_Lable, 0, wx.RIGHT)

        # 天气预报复选框模块sizer
        fuxuan1_option = wx.GridSizer(4, 2, 5, 5)
        self.cb1 = wx.CheckBox(self.panel, 24, '最高气温')
        self.cb2 = wx.CheckBox(self.panel, 25, '最低气温')
        self.cb3 = wx.CheckBox(self.panel, 26, '相对湿度')
        self.cb4 = wx.CheckBox(self.panel, 27, '降水概率')
        self.cb5 = wx.CheckBox(self.panel, 28, '能见度')
        self.cb6 = wx.CheckBox(self.panel, 29, '紫外线级别')
        self.cb7 = wx.CheckBox(self.panel, 30, '风速')
        fuxuan1_option.AddMany([
            (self.cb1, 0, wx.EXPAND), (self.cb2, 0, wx.EXPAND),
            (self.cb3, 0, wx.EXPAND), (self.cb4, 0, wx.EXPAND),
            (self.cb5, 0, wx.EXPAND), (self.cb6, 0, wx.EXPAND),
            (self.cb7, 0, wx.EXPAND),
        ])
        anaylse.Add(fuxuan1_option, 0, wx.RIGHT, )

        # 24小时历史天气预报静态文本框
        H_note_Lable = wx.StaticText(self.panel, -1, "24小时历史天气数据区：")
        anaylse.Add(H_note_Lable, 0, wx.RIGHT)

        # 24小时历史天气复选框模块sizer
        fuxuan2_option = wx.GridSizer(3, 2, 5, 5)
        self.cb8 = wx.CheckBox(self.panel, 30, '气温')
        self.cb9 = wx.CheckBox(self.panel, 30, '体感温度')
        self.cb10 = wx.CheckBox(self.panel, 30, '相对湿度')
        self.cb11 = wx.CheckBox(self.panel, 30, '降雨量')
        self.cb12 = wx.CheckBox(self.panel, 30, '风速')
        fuxuan2_option.AddMany([
            (self.cb8, 0, wx.EXPAND), (self.cb9, 0, wx.EXPAND),
            (self.cb10, 0, wx.EXPAND), (self.cb11, 0, wx.EXPAND),
            (self.cb12, 0, wx.EXPAND)
        ])
        anaylse.Add(fuxuan2_option, 0, wx.RIGHT, )

        # 年度月天气预报静态文本框
        Yof_maonth_note_Lable = wx.StaticText(self.panel, -1, "年度月天气历史数据区：")
        anaylse.Add(Yof_maonth_note_Lable, 0, wx.RIGHT)

        # 年度月天气复选框模块sizer
        fuxuan3_option = wx.GridSizer(2, 2, 5, 5)
        self.cb13 = wx.CheckBox(self.panel, 30, '最高气温')
        self.cb14 = wx.CheckBox(self.panel, 30, '最低气温')
        self.cb15 = wx.CheckBox(self.panel, 30, '平均气温')
        self.cb16 = wx.CheckBox(self.panel, 30, '降水量')
        fuxuan3_option.AddMany([
            (self.cb13, 0, wx.EXPAND), (self.cb14, 0, wx.EXPAND),
            (self.cb15, 0, wx.EXPAND), (self.cb16, 0, wx.EXPAND),
        ])
        anaylse.Add(fuxuan3_option, 0, wx.RIGHT, )

        # 日天气预报静态文本框
        Ri_note_Lable = wx.StaticText(self.panel, -1, "日天气历史数据区：")
        anaylse.Add(Ri_note_Lable, 0, wx.RIGHT)

        # 日天气复选框模块sizer
        fuxuan4_option = wx.GridSizer(4, 2, 5, 5)
        self.cb17 = wx.CheckBox(self.panel, 30, '晴好天气比率')
        self.cb18 = wx.CheckBox(self.panel, 30, '总降水量')
        self.cb19 = wx.CheckBox(self.panel, 30, '平均湿度')
        self.cb20 = wx.CheckBox(self.panel, 30, '日最高气温')
        self.cb21 = wx.CheckBox(self.panel, 30, '日最低气温')
        self.cb22 = wx.CheckBox(self.panel, 30, '日平均气温')
        self.cb23 = wx.CheckBox(self.panel, 30, '平均风速')
        fuxuan4_option.AddMany([
            (self.cb17, 0, wx.EXPAND), (self.cb18, 0, wx.EXPAND),
            (self.cb19, 0, wx.EXPAND), (self.cb20, 0, wx.EXPAND),
            (self.cb21, 0, wx.EXPAND), (self.cb22, 0, wx.EXPAND),
            (self.cb23, 0, wx.EXPAND),
        ])
        anaylse.Add(fuxuan4_option, 0, wx.RIGHT, )

        #图表类型
        tubiao_list = ["折线图","直方图","箱型图"]
        Tubiao_option = wx.BoxSizer(wx.HORIZONTAL)
        TubiaoLable = wx.StaticText(self.panel, -1, "图表类型")
        self.TubiaoComboBox = wx.ComboBox(self.panel, -1, value="折线图",
                                   choices=tubiao_list, style=wx.CB_READONLY)

        Tubiao_option.AddMany([
            (TubiaoLable, 0, wx.Top), (self.TubiaoComboBox, 0, wx.LEFT, 10),
        ])
        anaylse.Add(Tubiao_option, 0, wx.TOP, 10)


        #按钮
        Anniu_box5 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn1 = wx.Button(self.panel, label='重置', size=(56, 24))

        #重置按钮响应事件
        self.panel.Bind(wx.EVT_BUTTON, self.showpicture, self.btn1, )

        self.btn2 = wx.Button(self.panel, label='分析', size=(56, 24))

        #分析按钮响应事件
        self.panel.Bind(wx.EVT_BUTTON, self.OnInitButton2, self.btn2, )

        Anniu_box5.AddMany([
            (self.btn1,0,wx.ALL,5),(self.btn2,0,wx.ALL,5)
                            ])
        anaylse.Add(Anniu_box5, 0, wx.TOP, 20)

        S_show_mian_data.Add(anaylse,0,wx.ALL,5 )

        #静态文本框部分
        #labelText = wx.StaticText(panel, label="日期:")
        #codeSizer.Add(labelText, 0, wx.ALIGN_RIGHT)
        #codeText = wx.TextCtrl(panel, value='20181125', style=wx.TE_PROCESS_ENTER)
        #self.Bind(wx.EVT_TEXT_ENTER, self.OnTextSubmitted, codeText)
        #codeSizer.Add(codeText)
        self.list = wx.ListCtrl(self.panel, wx.NewId(), style=wx.LC_REPORT,)
        self.list.InsertColumn(0, "开始说明")
        self.list.SetColumnWidth(0, 500)
        self.list.InsertItem(0,"您可以从菜单开始使用,或者点击主菜单中的help获取帮助:)")
        Mysizers = wx.BoxSizer(wx.VERTICAL)
        Mysizers.Add(codeSizer,0,wx.ALL,5 )
        S_show_mian_data.Add(self.list, -1, wx.ALL | wx.EXPAND, 5)
        Mysizers.Add(S_show_mian_data,-1, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizerAndFit(Mysizers)
        self.Center()

    #一级下拉列表被选中时的响应函数
    def __OnComboBoxSelected1(self, event):
        currentProvinceIndex1 = self.__ProvinceComboBox.GetSelection()
        if wx.NOT_FOUND == currentProvinceIndex1 :return
        value1 = self.__ProvinceComboBox.GetItems()[currentProvinceIndex1]
        self._ShengFen = value1
        if self.__CityComboBox.IsEnabled() == False: return
        # 注意中文在List dict 等存储时候, utf-8 格式不一致问题
        cityList = self.__SecityDict[value1]
        self.__CityComboBox.SetItems(cityList)
        self.__CityComboBox.SetValue(cityList[0])
        self.__OnComboBoxSelected2(self)

    #二级下拉列表被选中时的响应函数
    def __OnComboBoxSelected2(self, event):
        currentShiquIndex = self.__CityComboBox.GetSelection()
        if wx.NOT_FOUND == currentShiquIndex: return
        value = self.__CityComboBox.GetItems()[currentShiquIndex]
        self._ShiQu = value
        if self._XianquCombobox.IsEnabled() == False: return
        # 注意中文在List dict 等存储时候, utf-8 格式不一致问题
        cityList = self.__SecityDict1[value]
        self._XianquCombobox.SetItems(cityList)
        self._XianquCombobox.SetValue(cityList[0])

    #三级下拉列表被选中时的响应函数
    def __OnComboBoxSelected3(self,event):
        currentXianquIndex= self._XianquCombobox.GetSelection()
        value = self._XianquCombobox.GetItems()[currentXianquIndex]
        self._cityname = value
        if self._menuopetion == 1:
            self.forecas(event)
        if self._menuopetion == 2:
            self.Dhistory(event)

    #四级下拉列表被选中时的响应函数
    def __OnComboBoxSelected4(self,event):
        currentnianfenIndex = self.nianfenComboBox.GetSelection()
        value = self.nianfenComboBox.GetItems()[currentnianfenIndex]
        self._year = value
        if  self._menuopetion == 3:
            self.Mhistory(event)

    #五级下拉列表被选中时的响应函数
    def __OnComboBoxSelected5(self,event):
        currentyuefenIndex = self.yuefenComboBox.GetSelection()
        value = self.yuefenComboBox.GetItems()[currentyuefenIndex]
        self._month = value
        if self._menuopetion == 4:
            self.M_day_history(event)
        if self._menuopetion == 7:
            self.filemenu_S_Hanbi_ForYearOfmonth(event)
        if self._menuopetion == 10:
            self.filemenu_S1_Hanbi_ForYearOfmonth(event)
        if self._menuopetion == 13:
            self.filemenu_S2_Hanbi_ForYearOfmonth(event)
        if self._menuopetion == 15 or self._menuopetion == 16 or self._menuopetion == 17 or self._menuopetion == 18:
            self.Tongbi_YearOf5o15o30o50(event)
    # 六级下拉列表被选中时的响应函数
    def __OnComboBoxSelected6(self, event):
        currentriIndex = self.riComboBox.GetSelection()
        value = self.riComboBox.GetItems()[currentriIndex]
        self._day = value
        if self._menuopetion == 5:
            self.Yhistory(event)
        if self._menuopetion == 8:
            self.filemenu_S_Hanbi_ForDay(event)
        if self._menuopetion == 11:
            self.filemenu_S1_Hanbi_ForDay(event)
        if self._menuopetion == 14:
            self.filemenu_S2_Hanbi_ForDay(event)

    def __OnComboBoxSelected7(self,event):
        currentTheOfDayIndex = self.ThedayComboBox.GetSelection()
        value = self.ThedayComboBox.GetItems()[currentTheOfDayIndex]
        self._TheDayOf = value
        if self._menuopetion == 6:
            self.filemenu_S_Hanbi_foreast(event)
        if self._menuopetion == 9:
            self.filemenu_S1_Hanbi_foreast(event)
        if self._menuopetion == 12:
            self.filemenu_S2_Hanbi_foreast(event)

    #静态文本框有输入且用户按下Eenter键时的响应函数
    def OnTextSubmitted(self,event):
        self._time = event.GetString()

    #绘制天气预报信息列表头
    def createHeader2forecas(self):
        self.list.InsertColumn(0,"城市")
        self.list.InsertColumn(1, "日期")
        self.list.InsertColumn(2, "最高气温")
        self.list.InsertColumn(3, "最低气温")
        self.list.InsertColumn(4, "相对湿度")
        self.list.InsertColumn(5, "降水概率")
        self.list.InsertColumn(6, "能见度")
        self.list.InsertColumn(7, "紫外线级别")
        self.list.InsertColumn(8, "白天天气现象")
        self.list.InsertColumn(9, "夜晚天气现象")
        self.list.InsertColumn(10, "风向")
        self.list.InsertColumn(11, "风力")
        self.list.InsertColumn(12, "风速")

    #绘制过去二十四小时历史信息列表头
    def createHeader2history(self):
        self.list.InsertColumn(0, "城市")
        self.list.InsertColumn(1, "更新时间")
        self.list.InsertColumn(2, '气温')
        self.list.InsertColumn(3, "天气现象")
        self.list.InsertColumn(4, "体感温度")
        self.list.InsertColumn(5, "相对湿度")
        self.list.InsertColumn(6, "降雨量")
        self.list.InsertColumn(7, "风向")
        self.list.InsertColumn(8, "风力")
        self.list.InsertColumn(9, "风速")

    #绘制年份月度天气历史信息列表头
    def createHeader2Mhistory(self):
        self.list.InsertColumn(0, "城市")
        self.list.InsertColumn(1, "年份")
        self.list.InsertColumn(2, '月份')
        self.list.InsertColumn(3, "最高气温")
        self.list.InsertColumn(4, "最低气温")
        self.list.InsertColumn(5, "平均气温")
        self.list.InsertColumn(6, "降水量")

    #绘制历史某一天的天气信息列表头
    def createHeader2Yistory(self):
        self.list.InsertColumn(0, "城市")
        self.list.InsertColumn(1, "日期")
        self.list.InsertColumn(2, '晴好天气比率')
        self.list.InsertColumn(3, "降水天气比率")
        self.list.InsertColumn(4, "总降水量")
        self.list.InsertColumn(5, "平均湿度")
        self.list.InsertColumn(6, "日最高气温")
        self.list.InsertColumn(7, "日最低气温")
        self.list.InsertColumn(8, "日平均气温")
        self.list.InsertColumn(9, "最常见风向")
        self.list.InsertColumn(10, "平均风速")

    #绘制分析天气预报信息的列表头
    def createHeader2Analyse(self):
        self.list.InsertColumn(0,'生活指数类型')
        self.list.InsertColumn(1, "生活指数简述")
        self.list.InsertColumn(2, "生活指数详情",)
        self.list.SetColumnWidth(2, 600)

    #绘制帮助信息的列表头
    def createHeader2help(self):
        self.list.InsertColumn(0,'菜单选项')
        self.list.SetColumnWidth(0, 100)
        self.list.InsertColumn(1, "选项说明")
        self.list.SetColumnWidth(1, 800)

    #绘制县区环比天气预报信息列表头
    def createHeader2XianQuforecas(self):
        if self._menuopetion == 6:
            self.list.InsertColumn(0, "市区")
        if self._menuopetion == 9 or self._menuopetion == 12:
            self.list.InsertColumn(0, "省份")
        self.list.InsertColumn(1,"城市")
        self.list.InsertColumn(2, "日期")
        self.list.InsertColumn(3, "最高气温")
        self.list.InsertColumn(4, "最低气温")
        self.list.InsertColumn(5, "相对湿度")
        self.list.InsertColumn(6, "降水概率")
        self.list.InsertColumn(7, "能见度")
        self.list.InsertColumn(8, "紫外线级别")
        self.list.InsertColumn(9, "白天天气现象")
        self.list.InsertColumn(10, "夜晚天气现象")
        self.list.InsertColumn(11, "风向")
        self.list.InsertColumn(12, "风力")
        self.list.InsertColumn(13, "风速")

    #绘制县区环比天气预报信息列表头
    def createHeader_filemenu_S_Hanbi_ForYearOfmonth(self):
        if self._menuopetion == 7:
            self.list.InsertColumn(0, "市区")
        if self._menuopetion == 10 or self._menuopetion == 13:
            self.list.InsertColumn(0, "省份")
        self.list.InsertColumn(1, "城市")
        self.list.InsertColumn(2, "年份")
        self.list.InsertColumn(3, '月份')
        self.list.InsertColumn(4, "最高气温")
        self.list.InsertColumn(5, "最低气温")
        self.list.InsertColumn(6, "平均气温")
        self.list.InsertColumn(7, "降水量")

    def createHeade_filemenu_S_Hanbi_ForDay(self):
        if self._menuopetion == 8:
            self.list.InsertColumn(0, "市区")
        if self._menuopetion == 11 or self._menuopetion == 14:
            self.list.InsertColumn(0, "省份")
        self.list.InsertColumn(1, "城市")
        self.list.InsertColumn(2, "日期")
        self.list.InsertColumn(3, '晴好天气比率')
        self.list.InsertColumn(4, "降水天气比率")
        self.list.InsertColumn(5, "总降水量")
        self.list.InsertColumn(6, "平均湿度")
        self.list.InsertColumn(7, "日最高气温")
        self.list.InsertColumn(8, "日最低气温")
        self.list.InsertColumn(9, "日平均气温")
        self.list.InsertColumn(10, "最常见风向")
        self.list.InsertColumn(11, "平均风速")

    #天气预报的一级响应函数
    def Befor_forecas(self,event):
        self._menuopetion = 1
        self.UnDothings()

    #绘制天气预报的列表信息
    def forecas(self,event):
        self._forecas_city = []
        self._forecas_date = []
        self._forecas_hum = []
        self._forecas_max = []
        self._forecas_min = []
        self._forecas_pop = []
        self._forecas_vis = []
        self._forecas_spd = []
        self._forecas_uv = []
        self._forecas_cond_n = []
        self._forecas_cond_d = []
        self._forecas_dir = []
        self._forecas_sc = []
        self.onlonding(self)
        self._data = my_envirounment.weather_forecast(str(self._cityname))
        forecastes = self._data['forecast']
        if forecastes:
            self.list.ClearAll()
            self.createHeader2forecas()
            pos = 0
            for row in forecastes:
                temp = row['tmp']
                temp_mi = temp['max']
                temp_ma = temp['min']
                cond = row['cond']
                cond_n = cond['cond_n']
                cond_d = cond['cond_d']
                wind = row['wind']
                dir = wind['dir']
                sc = wind['sc']
                spd = wind['spd']
                pos = self.list.InsertItem(pos + 1, self._cityname)
                self.list.SetItem(pos, 1, row['date'])
                self.list.SetItem(pos, 2, temp_mi)
                self.list.SetItem(pos, 3, temp_ma)
                self.list.SetItem(pos, 4, row['hum'])
                self.list.SetItem(pos, 5, row['pop'])
                self.list.SetItem(pos, 6, row['vis'])
                self.list.SetItem(pos, 7, row['uv'])
                self.list.SetItem(pos, 8, cond_n)
                self.list.SetItem(pos, 9, cond_d)
                self.list.SetItem(pos, 10, dir)
                self.list.SetItem(pos, 11, sc)
                self.list.SetItem(pos, 12, spd)
                self._forecas_city.append(self._cityname)
                self._forecas_date.append(row['date'])
                self._forecas_hum.append(int(row['hum']))
                self._forecas_max.append(int(temp_mi))
                self._forecas_min.append(int(temp_ma))
                self._forecas_pop.append(int(row['pop']))
                self._forecas_vis.append(int(row['vis']))
                self._forecas_spd.append(int(spd))
                self._forecas_uv.append(int(row['uv']))
                self._forecas_cond_n.append(cond_n)
                self._forecas_cond_d.append(cond_d)
                self._forecas_dir.append(dir)
                self._forecas_sc.append(sc)
                if pos % 2 == 0:
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

     # 过去二十四小时天气的一级响应函数
    def Befor_Dhistory(self, event):
        self._menuopetion = 2
        self.UnDothings()

    #绘制过去二十四小时天气的列表信息
    def Dhistory(self,event):
        self._Dhistory_city = []
        self._Dhistory_updatetime = []
        self._Dhistory_temperature = []
        self._Dhistory_phenomena = []
        self._Dhistory_feelst = []
        self._Dhistory_humidity = []
        self._Dhistory_rain = []
        self._Dhistory_winddirect = []
        self._Dhistory_windpower = []
        self._Dhistory_windspeed = []
        self.onlonding(self)
        self._data = my_envirounment.weather_history(str(self._cityname))
        forecastes = self._data ['history']
        if forecastes:
            self.list.ClearAll()
            self.createHeader2history()
            pos = 0
            for row in forecastes:
                self._Dhistory_city.append(self._cityname)
                self._Dhistory_updatetime.append(row['updatetime'])
                self._Dhistory_temperature.append(float(row['temperature']))
                self._Dhistory_feelst.append(float(row['feelst']))
                self._Dhistory_humidity.append(float(row['humidity']))
                self._Dhistory_rain.append(float(row['rain']))
                self._Dhistory_phenomena.append(row['phenomena'])
                self._Dhistory_winddirect.append(row['winddirect'])
                self._Dhistory_windpower.append(row['windpower'])

                if str(row['windspeed']) == '':
                    self._Yhistory_wspd_avg.append(-1)
                else:
                    self._Yhistory_wspd_avg.append(float(float(row['windspeed'])))
                #self._Dhistory_windspeed.append(float(row['windspeed']))

                pos = self.list.InsertItem(pos + 1, self._cityname)
                self.list.SetItem(pos, 1, row['updatetime'])
                self.list.SetItem(pos, 2, row['temperature'])
                self.list.SetItem(pos, 3, row['phenomena'])
                self.list.SetItem(pos, 4, row['feelst'])
                self.list.SetItem(pos, 5, row['humidity'])
                self.list.SetItem(pos, 6, row['rain'])
                self.list.SetItem(pos, 7, row['winddirect'])
                self.list.SetItem(pos, 8, row['windpower'])
                self.list.SetItem(pos, 9, row['windspeed'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

     # 绘制某一年的月度天气的一级响应函数
    def Befor_Mhistory(self, event):
        self._menuopetion = 3
        self.UnDothings()

    #绘制某一年的月度天气列表信息
    def Mhistory(self,event):
        self._Mhistory_city = []
        self._Mhistory_year = []
        self._Mhistory_month = []
        self._Mhistory_tem_max = []
        self._Mhistory_tem_min = []
        self._Mhistory_tem_avg = []
        self._Mhistory_pre = []
        self.onlonding(self)
        M_year = self._year
        if int(M_year) > 2015:
            wx.MessageBox('请选择2016年以前的年份','Message', wx.OK | wx.ICON_INFORMATION)
            return
        self._data = my_envirounment.weather_month_history(str(self._cityname),self._year)
        if 'info' not in self._data:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)
            return
        forecastes = self._data ['info']
        if forecastes:
            self.list.ClearAll()
            self.createHeader2Mhistory()
            pos = 0
            for row in forecastes:
                self._Mhistory_city.append(self._cityname)
                self._Mhistory_year.append(str(row['year']))
                self._Mhistory_month.append(int(row['month']))
                self._Mhistory_tem_max.append(float(row['tem_max']))
                self._Mhistory_tem_min.append(float(row['tem_min']))
                self._Mhistory_tem_avg.append(float(row['tem_avg']))
                self._Mhistory_pre.append(float(row['pre']))
                pos = self.list.InsertItem(pos + 1, self._cityname)
                self.list.SetItem(pos, 1, str(row['year']))
                self.list.SetItem(pos, 2, str(row['month']))
                self.list.SetItem(pos, 3, row['tem_max'])
                self.list.SetItem(pos, 4, row['tem_min'])
                self.list.SetItem(pos, 5, row['tem_avg'])
                self.list.SetItem(pos, 6, row['pre'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))


     # 绘制某一年的某个月的日历史天气的一级响应函数
    def Befor_M_day_historyy(self, event):
        self._menuopetion = 4
        self.UnDothings()

    #绘制某一年的某个月的日历史天气信息
    def M_day_history(self,event):
        self._Yhistory_city = []
        self._Yhistory_date = []
        self._Yhistory_sunny_percent = []
        self._Yhistory_rain_percent = []
        self._Yhistory_rain_full = []
        self._Yhistory_hum_avg = []
        self._Yhistory_tem_max = []
        self._Yhistory_tem_min = []
        self._Yhistory_tem_avg = []
        self._Yhistory_wdir_most = []
        self._Yhistory_wspd_avg = []
        self.onlonding(self)
        M_year = self._year
        if int(M_year) < 2016:
            wx.MessageBox('请选择2015年以后的年份','Message', wx.OK | wx.ICON_INFORMATION)
            return
        self._data = my_envirounment.month2day(str(self._cityname), int(self._month),int(self._year))
        M_day_Data = self._data
        if len(M_day_Data) == 0:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)
            return
        self.list.ClearAll()
        self.createHeader2Yistory()
        pos = 0
        for row in M_day_Data:
            pos = self.list.InsertItem(pos + 1, self._cityname)
            self.list.SetItem(pos, 1, row['date'])
            self.list.SetItem(pos, 2, str(row['sunny_percent']))
            self.list.SetItem(pos, 3, str(row['rain_percent']))
            self.list.SetItem(pos, 4, str(row['rain_full']))
            self.list.SetItem(pos, 5, str(row['hum_avg']))
            self.list.SetItem(pos, 6, row['tem_max'])
            self.list.SetItem(pos, 7, row['tem_min'])
            self.list.SetItem(pos, 8, row['tem_avg'])
            self.list.SetItem(pos, 9, row['wdir_most'])
            self.list.SetItem(pos, 10, str(row['wspd_avg']))

            self._Yhistory_city.append(self._cityname)
            self._Yhistory_date.append(row['date'])
            self._Yhistory_sunny_percent.append((float(row['sunny_percent'])))
            self._Yhistory_rain_percent.append((float(row['rain_percent'])))
            self._Yhistory_rain_full.append(int(float(row['rain_full'])))
            self._Yhistory_hum_avg.append(int(float(row['hum_avg'])))
            self._Yhistory_tem_max.append(int(float(row['tem_max'])))
            self._Yhistory_tem_min.append(int(float(row['tem_min'])))
            self._Yhistory_tem_avg.append(int(float(row['tem_avg'])))
            self._Yhistory_wdir_most.append( row['wdir_most'])
            if 'm/s' in str(row['wspd_avg']):
                M_wspd_avg = str(row['wspd_avg'])
                M_wspd_avg_A = M_wspd_avg.strip('m/s')
                self._Yhistory_wspd_avg.append(int(float(M_wspd_avg_A)))
            else:
                self._Yhistory_wspd_avg.append(int(float(row['wspd_avg'])))
            if pos % 2 == 0:
                # Set new look and feel for odd lines
                self.list.SetItemBackgroundColour(pos, (134, 225, 249))

     # 绘制某一天的天气信息的一级响应函数
    def Befor_Yhistory(self, event):
        self._menuopetion = 5
        self.UnDothings()

    #绘制某一天的天气信息
    def Yhistory(self,event):
        self._Yhistory_city = []
        self._Yhistory_date = []
        self._Yhistory_sunny_percent = []
        self._Yhistory_rain_percent = []
        self._Yhistory_rain_full = []
        self._Yhistory_hum_avg = []
        self._Yhistory_tem_max = []
        self._Yhistory_tem_min = []
        self._Yhistory_tem_avg = []
        self._Yhistory_wdir_most = []
        self._Yhistory_wspd_avg = []
        self.onlonding(self)
        M_year = self._year
        Yhistory_month = self._month
        Yhistory_day = self._day
        if int(M_year) < 2016:
            wx.MessageBox('请选择2015年以后的年份','Message', wx.OK | wx.ICON_INFORMATION)
            return
        if int(Yhistory_month) < 10: Yhistory_month = '0'+ Yhistory_month
        if int(Yhistory_day) < 10: Yhistory_day = '0'+ Yhistory_day
        Data = self._year + Yhistory_month + Yhistory_day
        self._data = my_envirounment.weather_date_history(str(self._cityname),int(Data))
        row = self._data
        if row:
            self.list.ClearAll()
            self.createHeader2Yistory()
            pos = 0
            pos = self.list.InsertItem(pos + 1, self._cityname)
            self.list.SetItem(pos, 1, row['date'])
            self.list.SetItem(pos, 2, str(row['sunny_percent']))
            self.list.SetItem(pos, 3, str(row['rain_percent']))
            self.list.SetItem(pos, 4, str(row['rain_full']))
            self.list.SetItem(pos, 5, str(row['hum_avg']))
            self.list.SetItem(pos, 6, row['tem_max'])
            self.list.SetItem(pos, 7, row['tem_min'])
            self.list.SetItem(pos, 8, row['tem_avg'])
            self.list.SetItem(pos, 9, row['wdir_most'])
            self.list.SetItem(pos, 10, str(row['wspd_avg']))

            self._Yhistory_city.append(self._cityname)
            self._Yhistory_date.append(row['date'])
            self._Yhistory_sunny_percent.append((float(row['sunny_percent'])))
            self._Yhistory_rain_percent.append((float(row['rain_percent'])))
            self._Yhistory_rain_full.append(int(float(row['rain_full'])))
            self._Yhistory_hum_avg.append(int(float(row['hum_avg'])))
            self._Yhistory_tem_max.append(int(float(row['tem_max'])))
            self._Yhistory_tem_min.append(int(float(row['tem_min'])))
            self._Yhistory_tem_avg.append(int(float(row['tem_avg'])))
            self._Yhistory_wdir_most.append(row['wdir_most'])
            if 'm/s' in str(row['wspd_avg']):
                M_wspd_avg = str(row['wspd_avg'])
                M_wspd_avg_A = M_wspd_avg.strip('m/s')
                self._Yhistory_wspd_avg.append(int(float(M_wspd_avg_A)))
            else:
                self._Yhistory_wspd_avg.append(int(float(row['wspd_avg'])))
            if pos % 2 == 0:
                # Set new look and feel for odd lines
                self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

     # 绘制县区环比的天气预报的一级响应函数
    def Befor_filemenu_S_Hanbi_foreast(self, event):
        self._menuopetion = 6
        self.UnDothings()

    #县区环比的天气预报按钮响应函数
    def filemenu_S_Hanbi_foreast(self,event):
        self._forecas_upcity = []
        self._forecas_city = []
        self._forecas_date = []
        self._forecas_hum = []
        self._forecas_max = []
        self._forecas_min = []
        self._forecas_pop = []
        self._forecas_vis = []
        self._forecas_spd = []
        self._forecas_uv = []
        self._forecas_cond_n = []
        self._forecas_cond_d = []
        self._forecas_dir = []
        self._forecas_sc = []
        self.onlonding(self)
        citArr = self.__SecityDict1[self._ShiQu]
        TheDayOf = self._TheDayOf
        self._data = my_envirounment.diyu_huanbi(1,citArr,int(TheDayOf),-1,-1,-1)
        foreast = self._data
        if foreast:
            self.list.ClearAll()
            self.createHeader2XianQuforecas()
            pos = 0
            adder = 0
            for row in foreast:
                temp = row['tmp']
                temp_mi = temp['max']
                temp_ma = temp['min']
                cond = row['cond']
                cond_n = cond['cond_n']
                cond_d = cond['cond_d']
                wind = row['wind']
                dir = wind['dir']
                sc = wind['sc']
                spd = wind['spd']
                #收集数据
                self._forecas_upcity.append(self._ShiQu)
                self._forecas_city.append(citArr[adder])
                self._forecas_date.append(row['date'])
                self._forecas_hum.append(int(row['hum']))
                self._forecas_max.append(int(temp_mi))
                self._forecas_min.append(int(temp_ma))
                self._forecas_pop.append(int(row['pop']))
                self._forecas_vis.append(int(row['vis']))
                self._forecas_spd.append(int(spd))
                self._forecas_uv.append(int(row['uv']))
                self._forecas_cond_n.append(cond_n)
                self._forecas_cond_d.append(cond_d)
                self._forecas_dir.append(dir)
                self._forecas_sc.append(sc)

                pos = self.list.InsertItem(pos + 1, self._ShiQu)
                self.list.SetItem(pos, 1, citArr[adder])
                self.list.SetItem(pos, 2, row['date'])
                self.list.SetItem(pos, 3, temp_mi)
                self.list.SetItem(pos, 4, temp_ma)
                self.list.SetItem(pos, 5, row['hum'])
                self.list.SetItem(pos, 6, row['pop'])
                self.list.SetItem(pos, 7, row['vis'])
                self.list.SetItem(pos, 8, row['uv'])
                self.list.SetItem(pos, 9, cond_n)
                self.list.SetItem(pos, 10, cond_d)
                self.list.SetItem(pos, 11, dir)
                self.list.SetItem(pos, 12, sc)
                self.list.SetItem(pos, 13, spd)
                adder = adder+1
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

     # 绘制县区环比的年度月天气的一级响应函数
    def Befor_filemenu_S_Hanbi_ForYearOfmonth(self, event):
        self._menuopetion = 7
        self.UnDothings()

    # 县区环比的年度月天气响应函数
    def filemenu_S_Hanbi_ForYearOfmonth(self,event):
        self._Mhistory_upcity = []
        self._Mhistory_city = []
        self._Mhistory_year = []
        self._Mhistory_month = []
        self._Mhistory_tem_max = []
        self._Mhistory_tem_min = []
        self._Mhistory_tem_avg = []
        self._Mhistory_pre = []
        self.onlonding(self)
        citArr = self.__SecityDict1[self._ShiQu]
        M_year = self._year
        Year_S_Hanbi = self._year
        month_S_Hanbi = self._month
        if int(M_year) > 2015:
            wx.MessageBox('请选择2016年以前的年份','Message', wx.OK | wx.ICON_INFORMATION)
            return
        self._data = my_envirounment.diyu_huanbi(2, citArr, -1,int(Year_S_Hanbi), int(month_S_Hanbi), -1)
        Hanbi_ForYearOfmonth =   self._data
        if Hanbi_ForYearOfmonth:
            self.list.ClearAll()
            self.createHeader_filemenu_S_Hanbi_ForYearOfmonth()
            pos = 0
            adder = 0
            for row in Hanbi_ForYearOfmonth:
                #收集数据
                self._Mhistory_upcity.append(self._ShiQu)
                self._Mhistory_city.append(citArr[adder])
                self._Mhistory_year.append(str(row['year']))
                self._Mhistory_month.append(int(row['month']))
                self._Mhistory_tem_max.append(float(row['tem_max']))
                self._Mhistory_tem_min.append(float(row['tem_min']))
                self._Mhistory_tem_avg.append(float(row['tem_avg']))
                self._Mhistory_pre.append(float(row['pre']))

                pos = self.list.InsertItem(pos + 1, self._ShiQu)
                self.list.SetItem(pos, 1, citArr[adder])
                self.list.SetItem(pos, 2, str(row['year']))
                self.list.SetItem(pos, 3, str(row['month']))
                self.list.SetItem(pos, 4, row['tem_max'])
                self.list.SetItem(pos, 5, row['tem_min'])
                self.list.SetItem(pos, 6, row['tem_avg'])
                self.list.SetItem(pos, 7, row['pre'])
                adder = adder + 1
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

     # 绘制县区环比的日天气的一级响应函数
    def Befor_filemenu_S_Hanbi_ForDay(self, event):
        self._menuopetion = 8
        self.UnDothings()

    # 县区环比的日天气的响应函数
    def filemenu_S_Hanbi_ForDay(self,event):
        self._Yhistory_upcity = []
        self._Yhistory_city = []
        self._Yhistory_date = []
        self._Yhistory_sunny_percent = []
        self._Yhistory_rain_percent = []
        self._Yhistory_rain_full = []
        self._Yhistory_hum_avg = []
        self._Yhistory_tem_max = []
        self._Yhistory_tem_min = []
        self._Yhistory_tem_avg = []
        self._Yhistory_wdir_most = []
        self._Yhistory_wspd_avg = []
        self.onlonding(self)
        citArr = self.__SecityDict1[self._ShiQu]
        M_year = self._year
        Yhistory_month = self._month
        Yhistory_day = self._day
        if int(M_year) < 2016:
            wx.MessageBox('请选择2015年以后的年份','Message', wx.OK | wx.ICON_INFORMATION)
            return
        if int(Yhistory_month) < 10: Yhistory_month = '0'+ Yhistory_month
        if int(Yhistory_day) < 10: Yhistory_day = '0'+ Yhistory_day
        Data = self._year + Yhistory_month + Yhistory_day
        self._data = my_envirounment.diyu_huanbi(3, citArr, -1,-1, -1, int(Data))
        Hanbi_ForDay = self._data
        if Hanbi_ForDay:
            self.list.ClearAll()
            self.createHeade_filemenu_S_Hanbi_ForDay()
            pos = 0
            adder = 0
            for row in Hanbi_ForDay:
                pos = self.list.InsertItem(pos + 1, self._ShiQu)
                self.list.SetItem(pos, 1, citArr[adder])
                self.list.SetItem(pos, 2, row['date'])
                self.list.SetItem(pos, 3, str(row['sunny_percent']))
                self.list.SetItem(pos, 4, str(row['rain_percent']))
                self.list.SetItem(pos, 5, str(row['rain_full']))
                self.list.SetItem(pos, 6, str(row['hum_avg']))
                self.list.SetItem(pos, 7, row['tem_max'])
                self.list.SetItem(pos, 8, row['tem_min'])
                self.list.SetItem(pos, 9, row['tem_avg'])
                self.list.SetItem(pos, 10, row['wdir_most'])
                self.list.SetItem(pos, 11, str(row['wspd_avg']))
                #收集数据
                self._Yhistory_upcity.append(self._ShiQu)
                self._Yhistory_city.append(citArr[adder])
                self._Yhistory_date.append(row['date'])
                self._Yhistory_sunny_percent.append((float(row['sunny_percent'])))
                self._Yhistory_rain_percent.append((float(row['rain_percent'])))
                self._Yhistory_rain_full.append(int(float(row['rain_full'])))
                self._Yhistory_hum_avg.append(int(float(row['hum_avg'])))
                self._Yhistory_tem_max.append(int(float(row['tem_max'])))
                self._Yhistory_tem_min.append(int(float(row['tem_min'])))
                self._Yhistory_tem_avg.append(int(float(row['tem_avg'])))
                self._Yhistory_wdir_most.append(row['wdir_most'])
                if 'm/s' in str(row['wspd_avg']):
                    M_wspd_avg = str(row['wspd_avg'])
                    M_wspd_avg_A = M_wspd_avg.strip('m/s')
                    self._Yhistory_wspd_avg.append(int(float(M_wspd_avg_A)))
                else:
                    self._Yhistory_wspd_avg.append(int(float(row['wspd_avg'])))
                adder = adder + 1
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

     # 绘制市区环比的天气预报的一级响应函数
    def Befor_filemenu_S1_Hanbi_foreast(self, event):
        self._menuopetion = 9
        self.UnDothings()

    # 市区环比的天气预报响应函数
    def filemenu_S1_Hanbi_foreast(self,event):
        self._forecas_upcity = []
        self._forecas_city = []
        self._forecas_date = []
        self._forecas_hum = []
        self._forecas_max = []
        self._forecas_min = []
        self._forecas_pop = []
        self._forecas_vis = []
        self._forecas_spd = []
        self._forecas_uv = []
        self._forecas_cond_n = []
        self._forecas_cond_d = []
        self._forecas_dir = []
        self._forecas_sc = []
        self.onlonding(self)
        ShiQuArr =  self.__SecityDict[self._ShengFen]
        citArr = []
        for city in ShiQuArr:
            citArr.append(self.__SecityDict1[city][0])
        TheDayOf = self._TheDayOf
        self._data = my_envirounment.diyu_huanbi(1,citArr,int(TheDayOf),-1,-1,-1)
        foreast = self._data
        if foreast:
            self.list.ClearAll()
            self.createHeader2XianQuforecas()
            pos = 0
            adder = 0
            for row in foreast:
                temp = row['tmp']
                temp_mi = temp['max']
                temp_ma = temp['min']
                cond = row['cond']
                cond_n = cond['cond_n']
                cond_d = cond['cond_d']
                wind = row['wind']
                dir = wind['dir']
                sc = wind['sc']
                spd = wind['spd']
                #收集数据
                self._forecas_upcity.append(self._ShengFen)
                self._forecas_city.append(citArr[adder])
                self._forecas_date.append(row['date'])
                self._forecas_hum.append(int(row['hum']))
                self._forecas_max.append(int(temp_mi))
                self._forecas_min.append(int(temp_ma))
                self._forecas_pop.append(int(row['pop']))
                self._forecas_vis.append(int(row['vis']))
                self._forecas_spd.append(int(spd))
                self._forecas_uv.append(int(row['uv']))
                self._forecas_cond_n.append(cond_n)
                self._forecas_cond_d.append(cond_d)
                self._forecas_dir.append(dir)
                self._forecas_sc.append(sc)

                pos = self.list.InsertItem(pos + 1, self._ShengFen)
                self.list.SetItem(pos, 1, citArr[adder])
                self.list.SetItem(pos, 2, row['date'])
                self.list.SetItem(pos, 3, temp_mi)
                self.list.SetItem(pos, 4, temp_ma)
                self.list.SetItem(pos, 5, row['hum'])
                self.list.SetItem(pos, 6, row['pop'])
                self.list.SetItem(pos, 7, row['vis'])
                self.list.SetItem(pos, 8, row['uv'])
                self.list.SetItem(pos, 9, cond_n)
                self.list.SetItem(pos, 10, cond_d)
                self.list.SetItem(pos, 11, dir)
                self.list.SetItem(pos, 12, sc)
                self.list.SetItem(pos, 13, spd)
                adder = adder+1
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

     # 绘制市区环比的年度月天气的一级响应函数
    def Befor_filemenu_S1_Hanbi_ForYearOfmonth(self, event):
        self._menuopetion = 10
        self.UnDothings()

    # 市区环比的年度月天气响应函数
    def filemenu_S1_Hanbi_ForYearOfmonth(self,event):
        self._Mhistory_upcity = []
        self._Mhistory_city = []
        self._Mhistory_year = []
        self._Mhistory_month = []
        self._Mhistory_tem_max = []
        self._Mhistory_tem_min = []
        self._Mhistory_tem_avg = []
        self._Mhistory_pre = []
        self.onlonding(self)
        ShiQuArr =  self.__SecityDict[self._ShengFen]
        citArr = []
        for city in ShiQuArr:
            citArr.append(self.__SecityDict1[city][0])
        M_year = self._year
        Year_S_Hanbi = self._year
        month_S_Hanbi = self._month
        if int(M_year) > 2015:
            wx.MessageBox('请选择2016年以前的年份','Message', wx.OK | wx.ICON_INFORMATION)
            return
        self._data = my_envirounment.diyu_huanbi(2, citArr, -1,int(Year_S_Hanbi), int(month_S_Hanbi), -1)
        Hanbi_ForYearOfmonth =   self._data
        if Hanbi_ForYearOfmonth:
            self.list.ClearAll()
            self.createHeader_filemenu_S_Hanbi_ForYearOfmonth()
            pos = 0
            adder = 0
            for row in Hanbi_ForYearOfmonth:
                #收集数据
                self._Mhistory_upcity.append(self._ShengFen)
                self._Mhistory_city.append(citArr[adder])
                self._Mhistory_year.append(str(row['year']))
                self._Mhistory_month.append(int(row['month']))
                self._Mhistory_tem_max.append(float(row['tem_max']))
                self._Mhistory_tem_min.append(float(row['tem_min']))
                self._Mhistory_tem_avg.append(float(row['tem_avg']))
                self._Mhistory_pre.append(float(row['pre']))

                pos = self.list.InsertItem(pos + 1, self._ShengFen)
                self.list.SetItem(pos, 1, citArr[adder])
                self.list.SetItem(pos, 2, str(row['year']))
                self.list.SetItem(pos, 3, str(row['month']))
                self.list.SetItem(pos, 4, row['tem_max'])
                self.list.SetItem(pos, 5, row['tem_min'])
                self.list.SetItem(pos, 6, row['tem_avg'])
                self.list.SetItem(pos, 7, row['pre'])
                adder = adder + 1
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

     # 绘制市区环比的日天气的一级响应函数
    def Befor_filemenu_S1_Hanbi_ForDay(self, event):
        self._menuopetion = 11
        self.UnDothings()

    # 市区环比的日天气的响应函数
    def filemenu_S1_Hanbi_ForDay(self, event):
        self._Yhistory_upcity = []
        self._Yhistory_city = []
        self._Yhistory_date = []
        self._Yhistory_sunny_percent = []
        self._Yhistory_rain_percent = []
        self._Yhistory_rain_full = []
        self._Yhistory_hum_avg = []
        self._Yhistory_tem_max = []
        self._Yhistory_tem_min = []
        self._Yhistory_tem_avg = []
        self._Yhistory_wdir_most = []
        self._Yhistory_wspd_avg = []
        self.onlonding(self)
        ShiQuArr =  self.__SecityDict[self._ShengFen]
        citArr = []
        for city in ShiQuArr:
            citArr.append(self.__SecityDict1[city][0])
        M_year = self._year
        Yhistory_month = self._month
        Yhistory_day = self._day
        if int(M_year) < 2016:
            wx.MessageBox('请选择2015年以后的年份','Message', wx.OK | wx.ICON_INFORMATION)
            return
        if int(Yhistory_month) < 10: Yhistory_month = '0'+ Yhistory_month
        if int(Yhistory_day) < 10: Yhistory_day = '0'+ Yhistory_day
        Date = self._year + Yhistory_month + Yhistory_day
        self._data = my_envirounment.diyu_huanbi(3, citArr, -1,-1, -1, int(Date))
        Hanbi_ForDay = self._data
        if Hanbi_ForDay:
            self.list.ClearAll()
            self.createHeade_filemenu_S_Hanbi_ForDay()
            pos = 0
            adder = 0
            for row in Hanbi_ForDay:
                pos = self.list.InsertItem(pos + 1, self._ShengFen)
                self.list.SetItem(pos, 1, citArr[adder])
                self.list.SetItem(pos, 2, row['date'])
                self.list.SetItem(pos, 3, str(row['sunny_percent']))
                self.list.SetItem(pos, 4, str(row['rain_percent']))
                self.list.SetItem(pos, 5, str(row['rain_full']))
                self.list.SetItem(pos, 6, str(row['hum_avg']))
                self.list.SetItem(pos, 7, row['tem_max'])
                self.list.SetItem(pos, 8, row['tem_min'])
                self.list.SetItem(pos, 9, row['tem_avg'])
                self.list.SetItem(pos, 10, row['wdir_most'])
                self.list.SetItem(pos, 11, str(row['wspd_avg']))
                #收集数据
                self._Yhistory_upcity.append(self._ShengFen)
                self._Yhistory_city.append(citArr[adder])
                self._Yhistory_date.append(row['date'])
                self._Yhistory_sunny_percent.append((float(row['sunny_percent'])))
                self._Yhistory_rain_percent.append((float(row['rain_percent'])))
                self._Yhistory_rain_full.append(int(float(row['rain_full'])))
                self._Yhistory_hum_avg.append(int(float(row['hum_avg'])))
                self._Yhistory_tem_max.append(int(float(row['tem_max'])))
                self._Yhistory_tem_min.append(int(float(row['tem_min'])))
                self._Yhistory_tem_avg.append(int(float(row['tem_avg'])))
                self._Yhistory_wdir_most.append(row['wdir_most'])
                if 'm/s' in str(row['wspd_avg']):
                    M_wspd_avg = str(row['wspd_avg'])
                    M_wspd_avg_A = M_wspd_avg.strip('m/s')
                    self._Yhistory_wspd_avg.append(int(float(M_wspd_avg_A)))
                else:
                    self._Yhistory_wspd_avg.append(int(float(row['wspd_avg'])))
                adder = adder + 1
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

     # 绘制全国所有省份环比的天气预报的一级响应函数
    def Befor_filemenu_S2_Hanbi_foreast(self, event):
        self._menuopetion = 12
        self.UnDothings()

    # 全国所有省份环比的天气预报响应函数
    def filemenu_S2_Hanbi_foreast(self, event):
        self._forecas_upcity = []
        self._forecas_city = []
        self._forecas_date = []
        self._forecas_hum = []
        self._forecas_max = []
        self._forecas_min = []
        self._forecas_pop = []
        self._forecas_vis = []
        self._forecas_spd = []
        self._forecas_uv = []
        self._forecas_cond_n = []
        self._forecas_cond_d = []
        self._forecas_dir = []
        self._forecas_sc = []

        self.onlonding(self)
        S2Cdict = my_envirounment.ShengandCity()
        ShengFenArr = []
        TheCityArr = []
        for ShengFen,city in S2Cdict.items():
            ShengFenArr.append(ShengFen)
            TheCityArr.append(city)
        TheDayOf = self._TheDayOf
        self._data = my_envirounment.diyu_huanbi(1,TheCityArr,int(TheDayOf),-1,-1,-1)
        foreast = self._data
        if foreast:
            self.list.ClearAll()
            self.createHeader2XianQuforecas()
            pos = 0
            adder = 0
            for row in foreast:
                temp = row['tmp']
                temp_mi = temp['max']
                temp_ma = temp['min']
                cond = row['cond']
                cond_n = cond['cond_n']
                cond_d = cond['cond_d']
                wind = row['wind']
                dir = wind['dir']
                sc = wind['sc']
                spd = wind['spd']
                # 收集数据
                self._forecas_upcity.append(ShengFenArr[adder])
                self._forecas_city.append(TheCityArr[adder])
                self._forecas_date.append(row['date'])
                self._forecas_hum.append(int(row['hum']))
                self._forecas_max.append(int(temp_mi))
                self._forecas_min.append(int(temp_ma))
                self._forecas_pop.append(int(row['pop']))
                self._forecas_vis.append(int(row['vis']))
                self._forecas_spd.append(int(spd))
                self._forecas_uv.append(int(row['uv']))
                self._forecas_cond_n.append(cond_n)
                self._forecas_cond_d.append(cond_d)
                self._forecas_dir.append(dir)
                self._forecas_sc.append(sc)

                pos = self.list.InsertItem(pos + 1, ShengFenArr[adder])
                self.list.SetItem(pos, 1, TheCityArr[adder])
                self.list.SetItem(pos, 2, row['date'])
                self.list.SetItem(pos, 3, temp_mi)
                self.list.SetItem(pos, 4, temp_ma)
                self.list.SetItem(pos, 5, row['hum'])
                self.list.SetItem(pos, 6, row['pop'])
                self.list.SetItem(pos, 7, row['vis'])
                self.list.SetItem(pos, 8, row['uv'])
                self.list.SetItem(pos, 9, cond_n)
                self.list.SetItem(pos, 10, cond_d)
                self.list.SetItem(pos, 11, dir)
                self.list.SetItem(pos, 12, sc)
                self.list.SetItem(pos, 13, spd)
                adder = adder + 1
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

    # 绘制全国所有省份环比的年度月天气的一级响应函数
    def Befor_filemenu_S2_Hanbi_ForYearOfmonth(self, event):
        self._menuopetion = 13
        self.UnDothings()

    # 全国所有省份环比的年度月天气响应函数
    def filemenu_S2_Hanbi_ForYearOfmonth(self,event):
        self._Mhistory_upcity = []
        self._Mhistory_city = []
        self._Mhistory_year = []
        self._Mhistory_month = []
        self._Mhistory_tem_max = []
        self._Mhistory_tem_min = []
        self._Mhistory_tem_avg = []
        self._Mhistory_pre = []
        self.onlonding(self)
        S2Cdict = my_envirounment.ShengandCity()
        ShengFenArr = []
        TheCityArr = []
        for ShengFen,city in S2Cdict.items():
            ShengFenArr.append(ShengFen)
            TheCityArr.append(city)
        Year_S1_Hanbi = self._year
        month_S1_Hanbi = self._month
        if int(Year_S1_Hanbi) > 2015:
            wx.MessageBox('请选择2016年以前的年份','Message', wx.OK | wx.ICON_INFORMATION)
            return
        self._data = my_envirounment.diyu_huanbi(2, TheCityArr, -1,int(Year_S1_Hanbi), int(month_S1_Hanbi), -1)
        Hanbi_ForYearOfmonth = self._data
        if Hanbi_ForYearOfmonth:
            self.list.ClearAll()
            self.createHeader_filemenu_S_Hanbi_ForYearOfmonth()
            pos = 0
            adder = 0
            for row in Hanbi_ForYearOfmonth:
                # 收集数据
                self._Mhistory_upcity.append(ShengFenArr[adder])
                self._Mhistory_city.append(TheCityArr[adder])
                self._Mhistory_year.append(str(row['year']))
                self._Mhistory_month.append(int(row['month']))
                self._Mhistory_tem_max.append(float(row['tem_max']))
                self._Mhistory_tem_min.append(float(row['tem_min']))
                self._Mhistory_tem_avg.append(float(row['tem_avg']))
                self._Mhistory_pre.append(float(row['pre']))

                pos = self.list.InsertItem(pos + 1,ShengFenArr[adder] )
                self.list.SetItem(pos, 1, TheCityArr[adder])
                self.list.SetItem(pos, 2, str(row['year']))
                self.list.SetItem(pos, 3, str(row['month']))
                self.list.SetItem(pos, 4, row['tem_max'])
                self.list.SetItem(pos, 5, row['tem_min'])
                self.list.SetItem(pos, 6, row['tem_avg'])
                self.list.SetItem(pos, 7, row['pre'])
                adder = adder + 1
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

     # 绘制全国所有省份环比的日天气的一级响应函数
    def Befor_filemenu_S2_Hanbi_ForDay(self, event):
        self._menuopetion = 14
        self.UnDothings()

    # 全国所有省份环比的日天气的响应函数
    def filemenu_S2_Hanbi_ForDay(self, event):
        self._Yhistory_upcity = []
        self._Yhistory_city = []
        self._Yhistory_date = []
        self._Yhistory_sunny_percent = []
        self._Yhistory_rain_percent = []
        self._Yhistory_rain_full = []
        self._Yhistory_hum_avg = []
        self._Yhistory_tem_max = []
        self._Yhistory_tem_min = []
        self._Yhistory_tem_avg = []
        self._Yhistory_wdir_most = []
        self._Yhistory_wspd_avg = []
        self.onlonding(self)
        S2Cdict = my_envirounment.ShengandCity()
        ShengFenArr = []
        TheCityArr = []
        for ShengFen,city in S2Cdict.items():
            ShengFenArr.append(ShengFen)
            TheCityArr.append(city)
        M_year = self._year
        Yhistory_month = self._month
        Yhistory_day = self._day
        if int(M_year) < 2016:
            wx.MessageBox('请选择2015年以后的年份','Message', wx.OK | wx.ICON_INFORMATION)
            return
        if int(Yhistory_month) < 10: Yhistory_month = '0'+ Yhistory_month
        if int(Yhistory_day) < 10: Yhistory_day = '0'+ Yhistory_day
        Date = self._year + Yhistory_month + Yhistory_day
        self._data = my_envirounment.diyu_huanbi(3, TheCityArr, -1, -1, -1, int(Date))
        Hanbi_ForDay = self._data
        if Hanbi_ForDay:
            self.list.ClearAll()
            self.createHeade_filemenu_S_Hanbi_ForDay()
            pos = 0
            adder = 0
            for row in Hanbi_ForDay:
                pos = self.list.InsertItem(pos + 1, ShengFenArr[adder])
                self.list.SetItem(pos, 1, TheCityArr[adder])
                self.list.SetItem(pos, 2, row['date'])
                self.list.SetItem(pos, 3, str(row['sunny_percent']))
                self.list.SetItem(pos, 4, str(row['rain_percent']))
                self.list.SetItem(pos, 5, str(row['rain_full']))
                self.list.SetItem(pos, 6, str(row['hum_avg']))
                self.list.SetItem(pos, 7, row['tem_max'])
                self.list.SetItem(pos, 8, row['tem_min'])
                self.list.SetItem(pos, 9, row['tem_avg'])
                self.list.SetItem(pos, 10, row['wdir_most'])
                self.list.SetItem(pos, 11, str(row['wspd_avg']))
                #收集数据
                self._Yhistory_upcity.append(ShengFenArr[adder])
                self._Yhistory_city.append(TheCityArr[adder])
                self._Yhistory_date.append(row['date'])
                self._Yhistory_sunny_percent.append((float(row['sunny_percent'])))
                self._Yhistory_rain_percent.append((float(row['rain_percent'])))
                self._Yhistory_rain_full.append(int(float(row['rain_full'])))
                self._Yhistory_hum_avg.append(int(float(row['hum_avg'])))
                self._Yhistory_tem_max.append(int(float(row['tem_max'])))
                self._Yhistory_tem_min.append(int(float(row['tem_min'])))
                self._Yhistory_tem_avg.append(int(float(row['tem_avg'])))
                self._Yhistory_wdir_most.append(row['wdir_most'])
                if 'm/s' in str(row['wspd_avg']):
                    M_wspd_avg = str(row['wspd_avg'])
                    M_wspd_avg_A = M_wspd_avg.strip('m/s')
                    self._Yhistory_wspd_avg.append(int(float(M_wspd_avg_A)))
                else:
                    self._Yhistory_wspd_avg.append(int(float(row['wspd_avg'])))
                adder = adder + 1
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)


     # 指定城市某个月份同比过去五年的天气数据的一级响应函数
    def Befor_Tongbi_YearOf5(self, event):
        self._menuopetion = 15
        self.UnDothings()

    # 指定城市某个月份同比过去五年的天气数据的响应函数
    def Tongbi_YearOf5o15o30o50(self,event):
        self._Mhistory_city = []
        self._Mhistory_year = []
        self._Mhistory_month = []
        self._Mhistory_tem_max = []
        self._Mhistory_tem_min = []
        self._Mhistory_tem_avg = []
        self._Mhistory_pre = []
        self.onlonding(self)
        Theyear = -1
        if self._menuopetion == 15:
            Theyear = 5
        elif self._menuopetion == 16:
            Theyear = 15
        elif self._menuopetion == 17:
            Theyear = 30
        elif self._menuopetion == 18:
            Theyear = 50
        M_month = self._month
        self._data = my_envirounment.city_tongbi(str(self._cityname), Theyear,int(M_month))
        Tongbi_YearOf5_Data =   self._data
        if Tongbi_YearOf5_Data:
            self.list.ClearAll()
            self.createHeader_filemenu_S_Hanbi_ForYearOfmonth()
            pos = 0
            adder = 0
            for row in Tongbi_YearOf5_Data:
                #收集数据
                self._Mhistory_city.append(self._cityname)
                self._Mhistory_year.append( str(row['year']))
                self._Mhistory_month.append(int(row['month']))
                self._Mhistory_tem_max.append(float(row['tem_max']))
                self._Mhistory_tem_min.append(float(row['tem_min']))
                self._Mhistory_tem_avg.append(float(row['tem_avg']))
                self._Mhistory_pre.append(float(row['pre']))

                pos = self.list.InsertItem(pos + 1, self._cityname)
                self.list.SetItem(pos, 1, str(row['year']))
                self.list.SetItem(pos, 2, str(row['month']))
                self.list.SetItem(pos, 3, row['tem_max'])
                self.list.SetItem(pos, 4, row['tem_min'])
                self.list.SetItem(pos, 5, row['tem_avg'])
                self.list.SetItem(pos, 6, row['pre'])
                adder = adder + 1
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
        else:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

     # 指定城市某个月份同比过去十五年的天气数据的一级响应函数
    def Befor_Tongbi_YearOf15(self, event):
        self._menuopetion = 16
        self.UnDothings()

     # 指定城市某个月份同比过去三十年的天气数据的一级响应函数
    def Befor_Tongbi_YearOf30(self, event):
        self._menuopetion = 17
        self.UnDothings()

     # 指定城市某个月份同比过去五十年的天气数据的一级响应函数
    def Befor_Tongbi_YearOf50(self, event):
        self._menuopetion = 18
        self.UnDothings()


    #集成禁止控件函数
    def UnDothings(self):
        if self._menuopetion == 1 or self._menuopetion == 2:
            self.__ProvinceComboBox.Enable(True)
            self.__CityComboBox.Enable(True)
            self._XianquCombobox.Enable(True)
            self.nianfenComboBox.Enable(False)
            self.yuefenComboBox.Enable(False)
            self.riComboBox.Enable(False)
            self.ThedayComboBox.Enable(False)
        if self._menuopetion == 3:
            self.__ProvinceComboBox.Enable(True)
            self.__CityComboBox.Enable(True)
            self._XianquCombobox.Enable(True)
            self.nianfenComboBox.Enable(True)
            self.yuefenComboBox.Enable(False)
            self.riComboBox.Enable(False)
            self.ThedayComboBox.Enable(False)
        if self._menuopetion == 4:
            self.__ProvinceComboBox.Enable(True)
            self.__CityComboBox.Enable(True)
            self._XianquCombobox.Enable(True)
            self.nianfenComboBox.Enable(True)
            self.yuefenComboBox.Enable(True)
            self.riComboBox.Enable(False)
            self.ThedayComboBox.Enable(False)
        if self._menuopetion == 5:
            self.__ProvinceComboBox.Enable(True)
            self.__CityComboBox.Enable(True)
            self._XianquCombobox.Enable(True)
            self.nianfenComboBox.Enable(True)
            self.yuefenComboBox.Enable(True)
            self.riComboBox.Enable(True)
            self.ThedayComboBox.Enable(False)
        if self._menuopetion == 6 or self._menuopetion == 9 or self._menuopetion == 12:
            if self._menuopetion == 6:
                self.__ProvinceComboBox.Enable(True)
                self.__CityComboBox.Enable(True)
                self._XianquCombobox.Enable(False)
            if self._menuopetion == 9:
                self.__ProvinceComboBox.Enable(True)
                self.__CityComboBox.Enable(False)
                self._XianquCombobox.Enable(False)
            if self._menuopetion == 12:
                self.__ProvinceComboBox.Enable(False)
                self.__CityComboBox.Enable(False)
                self._XianquCombobox.Enable(False)
            self.nianfenComboBox.Enable(False)
            self.yuefenComboBox.Enable(False)
            self.riComboBox.Enable(False)
            self.ThedayComboBox.Enable(True)
        if self._menuopetion == 7 or self._menuopetion == 10 or self._menuopetion == 13:
            if self._menuopetion == 7:
                self.__ProvinceComboBox.Enable(True)
                self.__CityComboBox.Enable(True)
                self._XianquCombobox.Enable(False)
            if self._menuopetion == 10:
                self.__ProvinceComboBox.Enable(True)
                self.__CityComboBox.Enable(False)
                self._XianquCombobox.Enable(False)
            if self._menuopetion == 13:
                self.__ProvinceComboBox.Enable(False)
                self.__CityComboBox.Enable(False)
                self._XianquCombobox.Enable(False)
            self.nianfenComboBox.Enable(True)
            self.yuefenComboBox.Enable(True)
            self.riComboBox.Enable(False)
            self.ThedayComboBox.Enable(False)
        if self._menuopetion == 8 or self._menuopetion == 11 or self._menuopetion == 14:
            if self._menuopetion == 8:
                self.__ProvinceComboBox.Enable(True)
                self.__CityComboBox.Enable(True)
                self._XianquCombobox.Enable(False)
            if self._menuopetion == 11:
                self.__ProvinceComboBox.Enable(True)
                self.__CityComboBox.Enable(False)
                self._XianquCombobox.Enable(False)
            if self._menuopetion == 14:
                self.__ProvinceComboBox.Enable(False)
                self.__CityComboBox.Enable(False)
                self._XianquCombobox.Enable(False)
            self.nianfenComboBox.Enable(True)
            self.yuefenComboBox.Enable(True)
            self.riComboBox.Enable(True)
            self.ThedayComboBox.Enable(False)
        if self._menuopetion == 15 or self._menuopetion == 16 or self._menuopetion == 17 or self._menuopetion == 18:
            self.__ProvinceComboBox.Enable(True)
            self.__CityComboBox.Enable(True)
            self._XianquCombobox.Enable(True)
            self.nianfenComboBox.Enable(False)
            self.yuefenComboBox.Enable(True)
            self.riComboBox.Enable(False)
            self.ThedayComboBox.Enable(False)
        self.UnDoFuXuanthings()

    # 复选框禁用逻辑
    def UnDoFuXuanthings(self):
        if  self._menuopetion == 1 or self._menuopetion == 6 or self._menuopetion == 9 or self._menuopetion == 12:
            # 天气预报
            self.cb1.Enable(True)
            self.cb2.Enable(True)
            self.cb3.Enable(True)
            self.cb4.Enable(True)
            self.cb5.Enable(True)
            self.cb6.Enable(True)
            self.cb7.Enable(True)

            # 24 小时历史天气
            self.cb8.Enable(False)
            self.cb9.Enable(False)
            self.cb10.Enable(False)
            self.cb11.Enable(False)
            self.cb12.Enable(False)

            # 年度月天气
            self.cb13.Enable(False)
            self.cb14.Enable(False)
            self.cb15.Enable(False)
            self.cb16.Enable(False)

            # 日天气
            self.cb17.Enable(False)
            self.cb18.Enable(False)
            self.cb19.Enable(False)
            self.cb20.Enable(False)
            self.cb21.Enable(False)
            self.cb22.Enable(False)
            self.cb23.Enable(False)
        elif self._menuopetion == 3 or self._menuopetion == 7 or self._menuopetion == 10 or self._menuopetion == 13 or self._menuopetion == 15 or self._menuopetion == 16 or self._menuopetion == 17 or self._menuopetion == 18:
            # 天气预报
            self.cb1.Enable(False)
            self.cb2.Enable(False)
            self.cb3.Enable(False)
            self.cb4.Enable(False)
            self.cb5.Enable(False)
            self.cb6.Enable(False)
            self.cb7.Enable(False)

            # 24 小时历史天气
            self.cb8.Enable(False)
            self.cb9.Enable(False)
            self.cb10.Enable(False)
            self.cb11.Enable(False)
            self.cb12.Enable(False)

            # 年度月天气
            self.cb13.Enable(True)
            self.cb14.Enable(True)
            self.cb15.Enable(True)
            self.cb16.Enable(True)

            # 日天气
            self.cb17.Enable(False)
            self.cb18.Enable(False)
            self.cb19.Enable(False)
            self.cb20.Enable(False)
            self.cb21.Enable(False)
            self.cb22.Enable(False)
            self.cb23.Enable(False)
        elif self._menuopetion == 4 or self._menuopetion == 5 or self._menuopetion == 8 or self._menuopetion == 11 or self._menuopetion == 14:
            # 天气预报
            self.cb1.Enable(False)
            self.cb2.Enable(False)
            self.cb3.Enable(False)
            self.cb4.Enable(False)
            self.cb5.Enable(False)
            self.cb6.Enable(False)
            self.cb7.Enable(False)

            # 24 小时历史天气
            self.cb8.Enable(False)
            self.cb9.Enable(False)
            self.cb10.Enable(False)
            self.cb11.Enable(False)
            self.cb12.Enable(False)

            # 年度月天气
            self.cb13.Enable(False)
            self.cb14.Enable(False)
            self.cb15.Enable(False)
            self.cb16.Enable(False)

            # 日天气
            self.cb17.Enable(True)
            self.cb18.Enable(True)
            self.cb19.Enable(True)
            self.cb20.Enable(True)
            self.cb21.Enable(True)
            self.cb22.Enable(True)
            self.cb23.Enable(True)
        else:
            # 天气预报
            self.cb1.Enable(False)
            self.cb2.Enable(False)
            self.cb3.Enable(False)
            self.cb4.Enable(False)
            self.cb5.Enable(False)
            self.cb6.Enable(False)
            self.cb7.Enable(False)

            # 24 小时历史天气
            self.cb8.Enable(True)
            self.cb9.Enable(True)
            self.cb10.Enable(True)
            self.cb11.Enable(True)
            self.cb12.Enable(True)

            # 年度月天气
            self.cb13.Enable(False)
            self.cb14.Enable(False)
            self.cb15.Enable(False)
            self.cb16.Enable(False)

            # 日天气
            self.cb17.Enable(False)
            self.cb18.Enable(False)
            self.cb19.Enable(False)
            self.cb20.Enable(False)
            self.cb21.Enable(False)
            self.cb22.Enable(False)
            self.cb23.Enable(False)
    #刷新的响应函数
    def fileSave(self,event):
        '''
        保存文件内容
        与菜单中的保存选项绑定
        '''
        self.dir_name = ''
        filesFilter = "TEXT file(*.txt)|*.txt|Excel 文件(*.xlsx)|*.xlsx"
        fd = wx.FileDialog(self, '把文件保存到何处', self.dir_name,
                '.txt', filesFilter , wx.FD_SAVE)
        if fd.ShowModal() == wx.ID_OK:
            self.file_name = fd.GetFilename()
            self.dir_name = fd.GetDirectory()
            M_name = self.file_name
            if M_name.split('.')[1] == 'txt':
                try:
                    with open(os.path.join(self.dir_name, self.file_name), 'w', encoding='utf-8') as f:
                        text = self._data
                        f.write(str(text))
                        save_msg = wx.MessageDialog(self, '文件已保存', '提示')
                except FileNotFoundError:
                        save_msg = wx.MessageDialog(self, '保存失败,无效的保存路径', '提示')
            if M_name.split('.')[1] == 'xlsx':
                try:
                    self.Data2Dataframe(self)
                    file_dir_name = self.dir_name + '\\'
                    file_dir_name = file_dir_name + self.file_name
                    Dataframe = self._Dataframe
                    quotesdf = pd.DataFrame(Dataframe)
                    quotesdf.to_excel(file_dir_name,index = False)
                    save_msg = wx.MessageDialog(self, '文件已保存', '提示')
                except FileNotFoundError:
                    save_msg = wx.MessageDialog(self, '保存失败,无效的保存路径', '提示')
        else:
            save_msg = wx.MessageDialog(self, '未选择保存路径', '错误')
        save_msg.ShowModal()
        save_msg.Destroy()

    #退出的响应函数
    def OnQuit(self,event):
        self.Close()
        self.Destroy()

    #帮助的响应函数
    def helps(self,event):
        self.list.ClearAll()
        self.createHeader2help()
        ANniu = ['天气预报','24小时天气','月度天气',
                 '日天气','刷新','分析','帮助','退出']
        text1 = '获得所选择的城市的未来七天的天气预报,一定要点击县区的下拉选框的内容才可以实现功能(以下按键同上)，否则内容为南京的天气预报'
        text2 = '和forcas一样要首先选定县区,其功能为可以获取到所选城市过去二十四小时的天气情况'
        text3 = '获得所选城市指定年份的每个月的天气情况,需要手动输入年份,并且要按Enter键(日天气同上),若字符串长度超过四,截取前四位字符,仅支持2015年以前的查询'
        text4 = '获得所选城市的指定某一天的历史天气情况'
        text5 = '刷新功能,对于本项目没什么实际意义,pass了'
        text6 = '点击按键之前必须要有分析的数据.即要点击前四个按键其中之一,实现数据分析的功能,其中天气预报还会给出生活指数'
        text7 = '获取帮助信息'
        text8 = '退出该程序'
        text = [text1,text2,text3,text4,text5,text6,text7,text8]
        pos = 0
        for i in range(8):
            pos = self.list.InsertItem(pos + 1, ANniu[i])
            self.list.SetItem(pos, 1, text[i])
            if pos % 2 == 0:
                # Set new look and feel for odd lines
                self.list.SetItemBackgroundColour(pos, (134, 225, 249))

    # 重置按钮的响应函数
    def OnInitButton1(self,event):
        pass

    # 分析按钮的响应函数
    def OnInitButton2(self,event):
        if self._menuopetion == 1 or self._menuopetion == 6 or self._menuopetion == 9 or self._menuopetion == 12:
            self.Analyzers1(event)
        elif self._menuopetion == 3 or self._menuopetion == 7 or self._menuopetion == 10 or self._menuopetion == 13 or self._menuopetion == 15 or self._menuopetion == 16 or self._menuopetion == 17 or self._menuopetion == 18:
            self.Analyzers2(event)
        elif self._menuopetion == 4 or self._menuopetion == 5 or self._menuopetion == 8 or self._menuopetion == 11 or self._menuopetion == 14:
            self.Analyzers3(event)
        else:
            self.Analyzers4(event)


    def Analyzers1(self,event):
        Datef = {}
        if self.cb1.GetValue():
            Datef['temp_max'] = self._forecas_max
        if self.cb2.GetValue():
            Datef['temp_mix'] = self._forecas_min
        if self.cb3.GetValue():
            Datef['hum'] = self._forecas_hum
        if self.cb4.GetValue():
            Datef['pop'] = self._forecas_pop
        if self.cb5.GetValue():
            Datef['vis'] = self._forecas_vis
        if self.cb6.GetValue():
            Datef['uv'] = self._forecas_uv
        if self.cb7.GetValue():
            Datef['spd'] = self._forecas_spd
        quotesdf = pd.DataFrame(Datef)
        if Datef:
            if self.TubiaoComboBox.GetSelection() == 0:
                quotesdf.plot()
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
            if self.TubiaoComboBox.GetSelection() == 1:
                quotesdf.plot(kind='bar')
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
            if self.TubiaoComboBox.GetSelection() == 2:
                quotesdf.boxplot()
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
        else:
            wx.MessageBox('请选择要进行分析的数据项','Message', wx.OK | wx.ICON_INFORMATION)

    def Analyzers2(self,event):
        Datef = {}
        if  self.cb13.GetValue():
            Datef['tem_max'] = self._Mhistory_tem_max
        if self.cb14.GetValue():
            Datef['tem_min'] = self._Mhistory_tem_min
        if self.cb15.GetValue():
            Datef['tem_avg'] = self._Mhistory_tem_avg
        if self.cb16.GetValue():
            Datef['pre'] = self._Mhistory_pre
        quotesdf = pd.DataFrame(Datef)

        if Datef:
            if self.TubiaoComboBox.GetSelection() == 0:
                quotesdf.plot()
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
            if self.TubiaoComboBox.GetSelection() == 1:
                quotesdf.plot(kind='bar')
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
            if self.TubiaoComboBox.GetSelection() == 2:
                quotesdf.boxplot()
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
        else:
            wx.MessageBox('请选择要进行分析的数据项', 'Message', wx.OK | wx.ICON_INFORMATION)

    def Analyzers3(self, event):
        Datef = {}
        if self.cb17.GetValue():
            Datef['sunny_percent'] =  self._Yhistory_sunny_percent
        if self.cb18.GetValue():
            Datef['rain_full'] = self._Yhistory_rain_full
        if self.cb19.GetValue():
            Datef['hum_avg'] = self._Yhistory_hum_avg
        if self.cb20.GetValue():
            Datef['tem_max'] = self._Yhistory_tem_max
        if self.cb21.GetValue():
            Datef['tem_min'] = self._Yhistory_tem_min
        if self.cb22.GetValue():
            Datef['tem_avg'] = self._Yhistory_tem_avg
        if self.cb23.GetValue():
            Datef['wspd_avg'] = self._Yhistory_wspd_avg

        if Datef:
            quotesdf = pd.DataFrame(Datef)
            if self.TubiaoComboBox.GetSelection() == 0:
                quotesdf.plot()
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
            if self.TubiaoComboBox.GetSelection() == 1:
                quotesdf.plot(kind='bar')
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
            if self.TubiaoComboBox.GetSelection() == 2:
                quotesdf.boxplot()
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
        else:
            wx.MessageBox('请选择要进行分析的数据项', 'Message', wx.OK | wx.ICON_INFORMATION)

    def Analyzers4(self, event):
        Datef = {}
        if self.cb8.GetValue():
             Datef['temperature'] = self._Dhistory_temperature
        if self.cb9.GetValue():
            Datef['feels'] = self._Dhistory_feelst
        if self.cb10.GetValue():
            Datef['humidity'] = self._Dhistory_humidity
        if self.cb11.GetValue():
            Datef['rain'] = self._Dhistory_rain
        if self.cb12.GetValue():
            Datef['windspeed'] = self._Dhistory_windspeed

        if Datef:
            quotesdf = pd.DataFrame(Datef)
            if self.TubiaoComboBox.GetSelection() == 0:
                quotesdf.plot()
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
            if self.TubiaoComboBox.GetSelection() == 1:
                quotesdf.plot(kind='bar')
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
            if self.TubiaoComboBox.GetSelection() == 2:
                quotesdf.boxplot()
                plt.savefig('./picture\\ImgSave.png')
                self.showpicture(event)
                plt.show()
        else:
            wx.MessageBox('请选择要进行分析的数据项', 'Message', wx.OK | wx.ICON_INFORMATION)

    def onlonding(self,event):
        self.list.ClearAll()
        self.list.InsertColumn(0, "加载中...")
        self.list.SetColumnWidth(0, 100)

    #将数据转换成Datafram的格式
    def Data2Dataframe(self,event):
        self._Dataframe = {}
        if self._menuopetion == 1 or self._menuopetion == 6 or self._menuopetion == 9 or self._menuopetion == 12:
                if self._menuopetion == 1:
                    self._Dataframe = {'城市': self._forecas_city ,'日期': self._forecas_date,'最高气温': self._forecas_max,
                                        '最低气温': self._forecas_min,'相对湿度': self._forecas_hum, '降水概率': self._forecas_pop,
                                       '能见度': self._forecas_vis,'白天天气现象':self._forecas_cond_d,'夜晚天气现象':self._forecas_cond_n,
                                       '风向':self._forecas_dir,'风力':self._forecas_sc,'紫外线级别': self._forecas_uv,
                                       '风速': self._forecas_spd}
                else:
                    if self._menuopetion == 6:
                        upcity = '市区'
                    else:
                        upcity = '省份'
                    self._Dataframe = {upcity:self._forecas_upcity,'城市': self._forecas_city ,'日期': self._forecas_date,'最高气温': self._forecas_max,
                                        '最低气温': self._forecas_min,'相对湿度': self._forecas_hum, '降水概率': self._forecas_pop,
                                       '能见度': self._forecas_vis,'白天天气现象':self._forecas_cond_d,'夜晚天气现象':self._forecas_cond_n,
                                       '风向':self._forecas_dir,'风力':self._forecas_sc,'紫外线级别': self._forecas_uv,
                                       '风速': self._forecas_spd}
        elif self._menuopetion == 3 or self._menuopetion == 7 or self._menuopetion == 10 or self._menuopetion == 13 or self._menuopetion == 15 or self._menuopetion == 16 or self._menuopetion == 17 or self._menuopetion == 18:
                if self._menuopetion == 3 or self._menuopetion == 15 or self._menuopetion == 16 or self._menuopetion == 17 or self._menuopetion == 18:
                    self._Dataframe = {'城市':self._Mhistory_city,'年份':self._Mhistory_year,
                                       '月份':self._Mhistory_month,'最高气温': self._Mhistory_tem_max,
                                        '最低气温': self._Mhistory_tem_min,'平均气温': self._Mhistory_tem_avg,
                                        '降水量': self._Mhistory_pre}
                elif self._menuopetion == 7:
                    self._Dataframe = {'市区':self._Mhistory_upcity,'城市': self._Mhistory_city,
                                       '年份': self._Mhistory_year,'月份': self._Mhistory_month,
                                       '最高气温': self._Mhistory_tem_max,'最低气温': self._Mhistory_tem_min,
                                       '平均气温': self._Mhistory_tem_avg,'降水量': self._Mhistory_pre}
                else:
                    self._Dataframe = {'省份': self._Mhistory_upcity, '城市': self._Mhistory_city,
                                       '年份': self._Mhistory_year, '月份': self._Mhistory_month,
                                       '最高气温': self._Mhistory_tem_max, '最低气温': self._Mhistory_tem_min,
                                       '平均气温': self._Mhistory_tem_avg, '降水量': self._Mhistory_pre}
        elif self._menuopetion == 4 or self._menuopetion == 5 or self._menuopetion == 8 or self._menuopetion == 11 or self._menuopetion == 14:
                if self._menuopetion == 4 or self._menuopetion == 5:
                    self._Dataframe = { '城市':self._Yhistory_city,'日期':self._Yhistory_date,
                                        '晴好天气比率':self._Yhistory_sunny_percent,'降水天气比率':self._Yhistory_rain_percent,
                                       '总降水量':self._Yhistory_rain_full,'平均湿度': self._Yhistory_hum_avg,
                                       '日最高气温':self._Yhistory_tem_max,'日最低气温':self._Yhistory_tem_min,
                                         '日平均气温':self._Yhistory_tem_avg,'最常见风向':self._Yhistory_wdir_most,
                                        '平均风速':self._Yhistory_wspd_avg}
                elif self._menuopetion == 8:
                    self._Dataframe = { '市区':self._Yhistory_upcity,
                                        '城市': self._Yhistory_city, '日期': self._Yhistory_date,
                                       '晴好天气比率': self._Yhistory_sunny_percent, '降水天气比率': self._Yhistory_rain_percent,
                                       '总降水量': self._Yhistory_rain_full, '平均湿度': self._Yhistory_hum_avg,
                                       '日最高气温': self._Yhistory_tem_max, '日最低气温': self._Yhistory_tem_min,
                                       '日平均气温': self._Yhistory_tem_avg, '最常见风向': self._Yhistory_wdir_most,
                                       '平均风速': self._Yhistory_wspd_avg}
                else:
                    self._Dataframe = {'省份': self._Yhistory_upcity,
                                       '城市': self._Yhistory_city, '日期': self._Yhistory_date,
                                       '晴好天气比率': self._Yhistory_sunny_percent, '降水天气比率': self._Yhistory_rain_percent,
                                       '总降水量': self._Yhistory_rain_full, '平均湿度': self._Yhistory_hum_avg,
                                       '日最高气温': self._Yhistory_tem_max, '日最低气温': self._Yhistory_tem_min,
                                       '日平均气温': self._Yhistory_tem_avg, '最常见风向': self._Yhistory_wdir_most,
                                       '平均风速': self._Yhistory_wspd_avg}
        else:
            self._Dataframe = {'城市': self._Dhistory_city, '更新时间': self._Dhistory_updatetime,
                               '气温': self._Dhistory_temperature, '天气现象': self._Dhistory_phenomena,
                               '体感温度': self._Dhistory_feelst, '相对湿度': self._Dhistory_humidity,
                               '降雨量': self._Dhistory_rain, '风向': self._Dhistory_winddirect,
                               '风力': self._Dhistory_windpower, '风速': self._Dhistory_windspeed}
    def showpicture(self,event):
        dialog = MyDialog()
        rec = dialog.ShowModal()



    #分析的响应函数
    def Analyzers(self,event):
        data = self._data
        if('suggestion' in data.keys()):
            forecastes = data['suggestion']
            self.list.ClearAll()
            self.createHeader2Analyse()
            pos = 0
            if(forecastes['trav']):
                trdata = forecastes['trav']
                pos = self.list.InsertItem(pos + 1, '旅游指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['uv']):
                trdata = forecastes['uv']
                pos = self.list.InsertItem(pos + 1, '紫外线指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['flu']):
                trdata = forecastes['flu']
                pos = self.list.InsertItem(pos + 1, '流感指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['comf']):
                trdata = forecastes['comf']
                pos = self.list.InsertItem(pos + 1, '舒适度指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['sport']):
                trdata = forecastes['sport']
                pos = self.list.InsertItem(pos + 1, '运动感指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['air']):
                trdata = forecastes['air']
                pos = self.list.InsertItem(pos + 1, '空气指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['cw']):
                trdata = forecastes['cw']
                pos = self.list.InsertItem(pos + 1, '洗车指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            if (forecastes['drs']):
                trdata = forecastes['drs']
                pos = self.list.InsertItem(pos + 1, '穿衣指数')
                self.list.SetItem(pos, 1, trdata['brf'])
                self.list.SetItem(pos, 2, trdata['txt'])
                if pos % 2 == 0:
                    # Set new look and feel for odd lines
                    self.list.SetItemBackgroundColour(pos, (134, 225, 249))
            Datef = {'spd':self._forecas_spd,'hum':self._forecas_hum,'uv':self._forecas_uv,
                    'temp_max':self._forecas_max,'temp_mix':self._forecas_min,'vis':self._forecas_vis,
                     'pop':self._forecas_pop}
            quotesdf = pd.DataFrame(Datef)
            quotesdf.index = self._forecas_date
            quotesdf.plot()
            plt.show()
        if('history' in data.keys()):
            Datef = {'temperature':self._Dhistory_temperature,'windspeed':self._Dhistory_windspeed,
                     'rain':self._Dhistory_rain,'humidity':self._Dhistory_humidity,
                     'feels':self._Dhistory_feelst}
            quotesdf = pd.DataFrame(Datef)
            quotesdf.index = self._Dhistory_updatetime
            quotesdf.plot()
            plt.show()
        if('info' in data.keys()):
            Datef = {'tem_max':self._Mhistory_tem_max,
                     'tem_min':self._Mhistory_tem_min,'tem_avg':self._Mhistory_tem_avg,
                     'pre':self._Mhistory_pre}
            quotesdf = pd.DataFrame(Datef)
            quotesdf.index = self._Mhistory_month
            quotesdf.plot()
            plt.show()
        if data.items() == 0:
            wx.MessageBox('Download failed.', 'Message', wx.OK | wx.ICON_INFORMATION)

class MyDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '显示图片', size=(570, 550))
        self.filename = './picture\\ImgSave.png'
        self.Bind(wx.EVT_SIZE, self.change)
        self.p = wx.Panel(self, -1)
        self.SetBackgroundColour('white')

    def start(self):
        self.p.DestroyChildren()
        # 抹掉原先显示的图片
        self.width, self.height = self.GetSize()
        self.image = Image.open(self.filename)
        self.x, self.y = self.image.size
        self.x = self.width / 2 - self.x / 2
        self.y = self.height / 2 - self.y / 2
        self.pic = wx.Image(self.filename, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # 通过计算获得图片的存放位置
        self.button = wx.BitmapButton(self.p, -1, self.pic, pos=(self.x, self.y))
        self.p.Fit()


    def change(self, size):
        #如果检测到框架大小的变化，及时改变图片的位置
        if self.filename != "":
            self.start()
        else:
            pass

if __name__ == '__main__':
    app = wx.App()
    frame = MyfirstFram(None)
    frame.Show(True)
    app.MainLoop()