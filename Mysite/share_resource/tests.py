from django.test import TestCase
import os
import time
# Create your tests here.


path = r"C:\Users\Administrator\Desktop\NIMOA_DE_sku汇总表现.html"
a = time.localtime(os.path.getctime(path))
otherStyleTime = time.strftime("%Y-%m-%d %H:%M", a)
print(otherStyleTime)
