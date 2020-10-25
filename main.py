# -*- coding: utf-8 -*-

"""
爬取百度迁徙数据，分为3个类型：城市，省份，全国

问题描述：
使用python爬取百度迁徙平台：http://qianxi.baidu.com/ 中人口流动数据，根据所需类型取消注释相应代码即可。
爬取内容将会以 Excel文件形式 保存在代码根目录中的“move_in"、"move_out"文件夹

使用须知：
【路径】：使用前请修改绝对路径
【日期】：请在【migration_all_date】函数中修改日期（注意，左区间包含，右区间不包含）
【城市区间】：由于爬取的时候没有设置异步操作，所以一次性爬取城市过多的情况下会导致时间超时（time_out)，
因此建议分区间爬取，可以复制多个源程序文件，同时开启多次不同区间的爬取

source: https://github.com/Chenmo1212/baidu_qx

"""

import requests
import json
import time
import os
import xlwt
import shutil
# 如果有红色下划线，不需要管
from ChineseAdminiDivisionsDict import CitiesCode, ProvinceCode


# 定义生成不同时期，不同城市，不同迁徙方向
def migration_all_date(area_name, class_name, no, direction, fp):
    """
    定义生成不同时期，不同城市，不同迁徙方向
    :param area_name: 区域名字
    :param class_name: 类别——city，province，country
    :param no: 编号——城市为-1，省份为省份id，全国为0
    :param direction: 迁入还是迁出——in：迁入，out：迁出
    :param fp: 保存的绝对路径
    """
    if no == -1:
        no = CitiesCode[str(area_name)]

    # 创建一个workbook
    workbook = xlwt.Workbook(encoding='utf-8')  # 创建一个workbook 设置编码
    worksheet = workbook.add_sheet('Sheet', cell_overwrite_ok=True)  # 创建一个worksheet

    # 写入行头各城市代码及其城市名
    if direction == 'in':
        name_of_dire = '迁入来源地'
        fp += '/move_in/'
        print("开始爬取迁入数据")
    if direction == 'out':
        name_of_dire = '迁出目的地'
        fp += './move_out/'
        print("开始爬取迁出数据")

    cities_order = {}  # 存放城市序号的空字典

    worksheet.write(0, 0, label='城市代码')  # 写入行头
    worksheet.write(0, 1, label=str(name_of_dire))  # 写入行头
    times = 1
    for key, value in CitiesCode.items():
        worksheet.write(times, 0, label=str(value))  # 写入城市代码
        worksheet.write(times, 1, label=str(key))  # 写入城市名
        cities_order[str(key)] = times  # 写入城市序号字典
        times += 1

    # 设定日期
    date_list = []  # 日期列表
    counter_data = 2  # 日期计数器
    for date1 in range(20200101, 20200104):  # 一月份[)类型
        date_list.append(date1)
    # for date2 in range(20200201, 20200215):  # 二月份[)类型
    #     date_list.append(date2)
    # for date3 in range(20200301, 20200315):  # 三月份[)类型
    #     date_list.append(date3)save('test.xls')

    for date in date_list:  # 遍历所有日期
        date_name = date
        time.sleep(0.5)
        url = f'http://huiyan.baidu.com/migration/cityrank.jsonp?dt={class_name}&id={no}&type=move_{direction}&date={date}'
        print(url)
        response = requests.get(url, timeout=2)  # 发出请求并json化处理
        time.sleep(1)
        r = response.text[4:-1]  # 去头去尾
        data_dict = json.loads(r)  # 字典化
        if data_dict['errmsg'] == 'SUCCESS':
            data_list = data_dict['data']['list']
            time.sleep(0.5)
            # 写入
            worksheet.write(0, counter_data, label=date_name)  # 写入表头————日期
            for a in range(len(CitiesCode)):
                worksheet.write(a + 1, counter_data, label=0)  # 先把当前日期下该列所有城市值置0
            # 获取数据
            for i in range(len(data_list)):
                city_name = data_list[i]['city_name']  # 城市名
                value = data_list[i]['value']  # 当日迁徙量所占百分比值
                # 写入
                worksheet.write(cities_order[str(city_name)], counter_data, label=value)  # 查找城市序号字典，在对应的行里写入相应的值
            counter_data += 1  # 日期计数器自加一
    workbook_name = area_name + "-" + name_of_dire + ".xls"
    workbook.save(workbook_name)  # 保存
    shutil.move(workbook_name, os.path.join(fp, workbook_name))


def create_mig_type(fp):
    """
    创建迁移类型文件夹
    :param fp: 绝对路径
    """
    mig_type_list = ['move_in', 'move_out']
    for mig_type in mig_type_list:
        if not os.path.exists(fp + mig_type):
            os.makedirs(fp + mig_type)


# 分为迁入迁出两种情况
def circu_exe_direction(area_name, class_name, no, fp):
    """
    定义生成不同时期，不同城市，不同迁徙方向
    :param area_name: 区域名字
    :param class_name: 类别——city，province，country
    :param no: 编号——城市为-1，省份为省份id，全国为0
    :param fp: 爬取文件保存的绝对路径
    """
    mig_type_list = ['in', 'out']
    for mig_type in mig_type_list:
        migration_all_date(area_name, class_name, no, mig_type, fp)
    print(str(area_name) + '---', '完成')


# 获取目标文件夹的所有子文件
def file_name(file_dir, mig_type):
    """
    获取目标文件夹的所有子文件
    :param file_dir: 目标文件夹路径(绝对路径)
    :param mig_type: 返回类型，1：文件夹；2：文件
    :return: 所有子文件
    """
    # 绝对路径
    folders_list = []
    files_list = []
    for file in os.listdir(file_dir):
        file_path = os.path.join(file_dir, file)
        if os.path.isdir(file_path):  # 是不是文件夹
            folders_list.append(file)
        else:
            files_list.append(file)
    if mig_type == 1:
        return folders_list
    else:
        return files_list


# 设置需要爬取的区域（因为一次性爬369个城市容易出现Time-out错误，所以采用分批区域爬取。
def set_city_area(min_num, max_num, fp):
    """
    设置需要爬取的区域（因为一次性爬369个城市容易出现Time-out错误，所以采用分批区域爬取。
    :param min_num: 最小值
    :param max_num: 最大值
    :param fp: 爬取文件保存的绝对路径
    """
    num = 0

    # 把本地已经爬取的文件名转成列表，再利用set去重，最后利用str转成字符串，在利用in关键词判断当前爬取的城市是否已经爬取了
    local_data = str(set(file_name('./move_in', 2)))

    for city_name in CitiesCode.keys():
        # print(city_name in str(local_data))
        num += 1
        if num <= min_num:
            continue
        elif min_num < num <= max_num:
            # 判断当前城市是否已经爬取，如果本地存在，则跳过
            if city_name in local_data:
                print(city_name, "已完成", num)
                continue
            else:
                print(city_name, "现在开始")
                # 爬取开始
                circu_exe_direction(city_name, 'city', -1, fp)
        if num >= max_num:
            exit()


# 爬取省级数据
def get_province_data(city_name, fp):
    """
    爬取省级数据
    :param city_name: 省级名字
    :param city_name: 省级名字
    :param fp: 爬取文件保存的绝对路径
    """
    # 获取省份对应id
    # print(ProvinceCode[city_name])
    province_id = ProvinceCode[city_name]
    circu_exe_direction(city_name, 'province', province_id, fp)


if __name__ == "__main__":

    # 设置爬取文件保存的绝对路径
    fp = "F:/工作/大创项目/000 新冠疫情信息系统/004 数据/00 百度迁徙/03 csdn1/源代码/"
    # 创建保存文件夹
    create_mig_type(fp)

    """##########################  Type one: 市级数据  ##########################"""
    # 爬取市级数据
    # 市级名字列表
    # print(list(CitiesCode.keys()))

    # 注意，一次性爬取全部城市可能会爬取超时，建议分批爬取
    set_city_area(0, 1, fp)

    """##########################  Type Two: 省级数据  ##########################"""
    # 爬取省级数据
    get_province_data("湖北省", fp)

    """##########################  Type Three: 全国数据  ##########################"""
    # 爬取省级数据
    circu_exe_direction('全国', 'country', 0, fp)
    print('全部完成')
