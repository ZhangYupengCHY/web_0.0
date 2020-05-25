from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, Http404, HttpResponse, render_to_response
from django_pandas.io import read_frame
import warnings
import os
from datetime import datetime
import pandas as pd
import numpy as np

# Create your views here.

warnings.filterwarnings(action='ignore')


# 文件分享中心,上传函数
def share(request):
    name = request.session.get("username", None)
    store_folder = r"C:\Users\Administrator\PycharmProjects\web_0.0\Mysite\share_resource\resources"
    files_list = os.listdir(store_folder)
    icon_folder = r'C:\Users\Administrator\PycharmProjects\web_0.0\Mysite\static\images\icons'
    own_icon_files_type = os.listdir(icon_folder)
    own_icon_files_type = [os.path.splitext(file_type_name)[0].lower() for file_type_name in own_icon_files_type]
    file_list_icon = [os.path.splitext(file)[-1].lower().strip('.')+'.png' if os.path.splitext(file)[-1].lower().strip('.') in own_icon_files_type else 'none.png' for
                      file in files_list]
    file_list_icon_path = [os.path.join(icon_folder,file_icon) for file_icon in file_list_icon]
    data = np.array([files_list,file_list_icon_path]).T
    file_info = pd.DataFrame(data,columns=['file_name','file_icon'])

    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("upload_file", None)  # 获取上传的文件，如果没有文件，则默认为None
        upload_msg = ''
        if not myFile:
            upload_msg = '{} 上传失败'.format(myFile.name)
            return render_to_response('share_resource.html', locals())
        destination = open(os.path.join(store_folder, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        upload_msg = '{} 上传成功'.format(myFile.name)
        # share()
        return render_to_response('share_resource.html', locals())
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
