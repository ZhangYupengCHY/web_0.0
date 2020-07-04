from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, Http404, HttpResponse, render_to_response
from django_pandas.io import read_frame
import warnings
import os
from datetime import datetime
import pandas as pd
import numpy as np
import pickle
import redis
# Create your views here.
import pymysql
import zipfile

warnings.filterwarnings(action='ignore')


class Redis_Store(object):
    """
    将list数据写入到redis中,实现存储和取用
    """

    def __init__(self, redis_host='127.0.0.1', redis_port=6379, redis_db=2,
                 redis_psw='chy910624'):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_psw = redis_psw
        self.redis_pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, password=self.redis_psw,
                                               db=self.redis_db, decode_responses=True)
        self.red = redis.StrictRedis(connection_pool=self.redis_pool)

    def redis_upload_list(self, list_data: list, list_key: 'str'):
        """
        将list数据上传到redis
        :param list_data:list型的数据
        :param list_key:存储的键名称
        :param save_datetime:保存时间20200218
        :return:
        """
        if list_data is None:
            return
        if not isinstance(list_data, list):
            return
        # 判断键名称是否存在
        if self.red.exists(list_key):
            self.red.delete(list_key)
        self.red.lpush(list_key, *list_data)

    def keys(self):
        return self.red.keys()

    def expire(self,key,time):
        return self.red.expire(key,time)

    # 将取出存储在redis中list
    def redis_download_list(self, list_key):
        """
        :return:key对应的list
        """
        if not self.red.exists(list_key):
            return
        list_from_redis = self.red.lrange(list_key, 0, -1)
        return list_from_redis


# 连接数据库得到站点列表
def db_download_station_names(db='team_station', table='only_station_info', ip='wuhan.yibai-it.com', port=33061,
                              user_name='marmot', password=''):
    """
    加载广告组接手的站点以及对应的平均数据
    :return: 站点平均cpc和acos
    """
    conn = pymysql.connect(
        host=ip,
        user=user_name,
        password=password,
        database=db,
        port=port,
        charset='UTF8')
    # 创建游标
    cursor = conn.cursor()
    # 写sql
    sql = """SELECT station FROM {} """.format(table)
    # 执行sql语句
    cursor.execute(sql)
    stations_info = cursor.fetchall()
    stations_name = [station[0].strip(' ') for station in stations_info]
    conn.commit()
    cursor.close()
    conn.close()
    return stations_name


# 连接数据库得到销售上传表的信息
def db_download_upload_file_log(db='team_station', table='saler_upload_files_log', ip='wuhan.yibai-it.com', port=33061,
                              user_name='marmot', password=''):

    conn = pymysql.connect(
        host=ip,
        user=user_name,
        password=password,
        database=db,
        port=port,
        charset='UTF8')
    # 创建游标
    cursor = conn.cursor()
    # 写sql
    sql = """SELECT * FROM {} """.format(table)
    # 执行sql语句
    cursor.execute(sql)
    stations_info = cursor.fetchall()
    stations_name = [list(station) for station in stations_info]
    conn.commit()
    cursor.close()
    conn.close()
    return stations_name


# 将station_info加载到服务器中
def db_upload_upload_file_log(upload_info:list, db='team_station', table='saler_upload_files_log', ip='wuhan.yibai-it.com',
                           port=33061,
                           user_name='marmot', password=''):
    conn = pymysql.connect(
        host=ip,
        user=user_name,
        password=password,
        database=db,
        port=port,
        charset='UTF8')
    # 创建游标
    cursor = conn.cursor()
    # 站号
    # 将数据变成可进行读入数据库的dict格式
    upload_info = [tuple(upload_info)]
    # 写sql
    insert_sql = """insert into {} (id,username,station_name,upload_datetime) \
                    values (%s,%s,%s,%s)""".format(table)
    # 执行sql语句
    try:
        cursor.execute(insert_sql, upload_info)
        conn.commit()
        print('上传成功...')
        print("===================================================")
    except Exception as e:
        conn.rollback()
        print('上传失败...')
        print("===================================================")
        print(e)
    cursor.close()
    conn.close()



# 上传压缩文件
def upload_files(request):
    """
    销售上传站点5表压缩文件到广告服务器中
        1.核对上传五表的压缩包名(核查上传站点是否正确)
            A:获得全站点列表
                上传压缩文件时,先去redis中查找站点列名(all_station_name_time 类型为list)
                若redis中存在all_station_name_time键,则加载redis数据,若redis中没有all_station_name_time键,说明已经过期,则需要重新将
                站点列表从mysql加载到redis中.
            B:判断表名是否存在
                然后判断销售上传的站点是否在列表中,若不存在,则应该给出错误提示。
        2.解压后核对5表的文件名:
            1.  广告报表(cp):           国家开头并包含bulksheet的xlsx(注意:英国是以gb开头)
            2.  搜索词报告(st):         包含Search的xlsx
            3.  商业报告(br):           包含business
            4.  active_listing报表(ac): 包含active
            5.  订单报告(ao):           全数字
    :param request:
    :return:
    """
    def db_download_table(table, db='team_station', ip='wuhan.yibai-it.com', port=33061,
                          user_name='marmot', password=''):
        """
        下载数据库表
        :return:
        """
        conn = pymysql.connect(
            host=ip,
            user=user_name,
            password=password,
            database=db,

            port=port,
            charset='UTF8')
        # 创建游标
        cursor = conn.cursor()

        # 写sql
        sql = """SELECT * FROM {} """.format(table)
        # 执行sql语句
        cursor.execute(sql)
        table_data = cursor.fetchall()
        # 获得列名
        cols = cursor.description
        table_col = []
        for i in cols:
            table_col.append(i[0])
        table_data = pd.DataFrame([list(row) for row in table_data], columns=table_col)
        conn.commit()
        cursor.close()
        conn.close()
        return table_data

    sales_upload_log = db_download_table('sales_upload_files_log')
    print(sales_upload_log)


    name = request.session.get("username", None)
    store_folder = r"D:\sales_upload_zipped"
    return_html = render_to_response('share_resource.html', locals())
    all_station_redis_key = 'all_station_name'
    error_msg = ''
    return_html.set_cookie("postToken",value='allow')
    print(request.COOKIES["postToken"])
    files_list = os.listdir(store_folder)
    if request.method == "POST":  # 请求方法为POST时，进行处理
        if request.COOKIES["postToken"] != 'allow':
            print('不存在合法Token,该表单为重复提交!')
            return HttpResponse("you can't post it again.")
        myFile = request.FILES.get("upload_zip", None)  # 获取上传的文件，如果没有文件，则默认为None
        if myFile is None:
            return render_to_response('share_resource.html', locals())
        myFile_name = myFile.name
        # 1.判断是否为压缩文件
        upload_zipped_file_type = os.path.splitext(myFile.name)[1]
        zipped_file_sign = '.zip'
        if upload_zipped_file_type.lower() != zipped_file_sign:
            error_msg = '{}不是.zip文件,请上传.zip压缩文件.'.format(myFile_name)
            print(error_msg)
            return render_to_response('share_resource.html', locals())
        # 2.判断站点是否正确
        # 2.1加载站点列表
        conn_redis = Redis_Store()
        redis_keys = conn_redis.keys()
        if all_station_redis_key not in redis_keys:
            station_names = db_download_station_names()  # 从mysql数据库中加载station_name
            conn_redis.redis_upload_list(station_names, all_station_redis_key)
            conn_redis.expire(all_station_redis_key, 3600)
        else:
            station_names = conn_redis.redis_download_list(all_station_redis_key)  # 从redis中加载station_name
        station_names = (station.lower() for station in station_names)
        # 2.2 判断上传的压缩文件文件名是否正确
        upload_zipped_file_name = os.path.splitext(myFile.name)[0]
        upload_zipped_file_name = upload_zipped_file_name.strip(' ()（）12').lower()
        if upload_zipped_file_name not in station_names:
            error_msg = '{}不存在,请核对后上传.'.format(upload_zipped_file_name)
            return render_to_response('share_resource.html', locals())
        # 2.3判断压缩文件内容
        five_file_sign = {'cp': 'bulksheet', 'ac': 'active', 'st': 'search', 'ao': 'all', 'br': "business"}
        z = zipfile.ZipFile(myFile, "r")
        file_list = z.namelist()
        file_list = [file.split('/')[1] for file in file_list]
        print(file_list)
        lost_list = []
        for file_type, file_sign in five_file_sign.items():
            is_exist = False
            if file_type != 'ao':
                for file in file_list:
                    if file_sign.lower() in file.lower():
                        is_exist = True
                        break
                if not is_exist:
                    lost_list.append(file_type)
            else:
                # ao表识别方式:allorders 或是存数字
                order_is_exists = False
                for file in file_list:
                    if 'order' in file:
                        order_is_exists = True
                        break
                    if os.path.splitext(file)[0].isdigit():
                        order_is_exists = True
                        break
                if not order_is_exists:
                    lost_list.append('ao')
        if lost_list:
            error_msg = '缺失{}表,请核查后再次上传'.format(lost_list)
            return render_to_response('share_resource.html', locals())
        # 2.4核对是否上传正确的站点
        site = upload_zipped_file_name[-2:].lower()
        camp_file_site = [file for file in file_list if five_file_sign['cp'] in file.lower()][0][:2]
        # 广告报表的前两个数字
        if site != camp_file_site:
            error_msg = '上传的站点{},而文件内容站点数据为{},请核查后再次上传'.format(site, camp_file_site)
            return render_to_response('share_resource.html', locals())
        # 2.5回传压缩文件
        destination = open(os.path.join(store_folder, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        print(myFile)
        print(type(myFile))
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        # 2.6显示已经上传的文件列表
        files_list = os.listdir(store_folder)

        #2.7 将信息上传到数据库中
#         username = request.get_signed_cookie('username', salt='marmot')
        upload_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response = render_to_response('share_resource.html', locals())
        response.set_cookie("postToken",value='disable')
        return response
    return return_html


# 文件分享中心,上传函数
def share(request):
    # name = request.session.get("username", None)
    # store_folder = r"C:\Users\Administrator\PycharmProjects\web_0.0\Mysite\share_resource\resources"
    # files_list = os.listdir(store_folder)
    # icon_folder = r'C:\Users\Administrator\PycharmProjects\web_0.0\Mysite\static\images\icons'
    # own_icon_files_type = os.listdir(icon_folder)
    # own_icon_files_type = [os.path.splitext(file_type_name)[0].lower() for file_type_name in own_icon_files_type]
    # file_list_icon = [os.path.splitext(file)[-1].lower().strip('.')+'.png' if os.path.splitext(file)[-1].lower().strip('.') in own_icon_files_type else 'none.png' for
    #                   file in files_list]
    # file_list_icon_path = [os.path.join(icon_folder,file_icon) for file_icon in file_list_icon]
    # data = np.array([files_list,file_list_icon_path]).T
    # file_info = pd.DataFrame(data,columns=['file_name','file_icon'])
    name = request.session.get("username", None)
    store_folder = r"C:\Users\Administrator\PycharmProjects\web_0.0\Mysite\share_resource\resources"
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("upload_zip", None)  # 获取上传的文件，如果没有文件，则默认为None
        print(myFile)
        for file in myFile:
            if not myFile:
                upload_msg = '{} 上传失败'.format(file.name)
                return render_to_response('share_resource.html', locals())
            # 文件内容
            destination = open(os.path.join(store_folder, file.name), 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in file.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
    files_list = os.listdir(store_folder)

    return render_to_response('share_resource.html', locals())


# 下载文件
def download(request, file_name):
    store_folder = r"C:\Users\Administrator\PycharmProjects\web_0.0\Mysite\share_resource\resources"
    file_path = os.path.join(store_folder, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f)
        response['Content-Type'] = 'application/octet-stream'
        from django.utils.http import urlquote
        response['Content-Disposition'] = 'attachment;filename={0}'.format(urlquote(file_name))
        return response
    else:
        return Http404


