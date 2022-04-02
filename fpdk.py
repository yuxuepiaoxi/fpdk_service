from ctypes import *
import json

'''
综服平台的一些接口
'''
#载入动态库
hhc_fpdk=cdll.LoadLibrary('./hhc_fpdk_x86.dll')
# 0 初始化函数
fpdk_init=hhc_fpdk.fpdk_init
fpdk_init.argtypes=[c_char_p]

# 9.1 根据税号获取地区编码
getDq_byCert=hhc_fpdk.getDq_byCert
getDq_byCert.argtypes=[c_char_p]
getDq_byCert.restype=c_char_p

#2.1 登录综服（插入设备）
get_login=hhc_fpdk.get_login
get_login.argtypes=[c_char_p,c_char_p,c_char_p]
get_login.restype=c_char_p

#检查字符串是否为json格式
def checkJson(str1):
    try:
        str1=json.loads(str1)

        if isinstance(str1,dict):
            return True
        else:
            return False
    except BaseException:
        return False

#对动态库返回结果的处理
def deal_result(str_ret):
    ret_code={}
    if checkJson(str_ret):
        ret_code['code']=0
        ret_code['value']=str_ret
    else:
        ret_code['code']=str_ret
        ret_code['msg']='异常错误'
    return ret_code
class Fpdk:
    def __init__(self,cert):
        self.dqbm=None
        self.token=None
        self.cert=cert

        #根据税号获取地区编码
        ret_getDq_byCert=getDq_byCert(cert.encode()).decode()
        self.dqbm=json.loads(ret_getDq_byCert).get('dqbm')
    #登录函数
    def login(self,password):
        ret_get_login=get_login(self.cert.encode(),self.dqbm.encode(),password.encode()).decode()
        ret_code=deal_result(ret_get_login)
        if ret_code['code']==0:
            self.token=json.loads(ret_code['value']).get('token')
    
    #勾选接入接口 deductInvoices
    def deductInvoices(self,taxNo,period,deductType,invoices):
        
        


if __name__=='__main__':
    fpdk_init(b'4.0.19')
    cert='91420106737921226H'
    password='88888888'
    fpdk=Fpdk(cert)
    fpdk.login(password)
    