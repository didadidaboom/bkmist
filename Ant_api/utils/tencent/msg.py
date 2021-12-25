from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20190711 import sms_client, models
from django.conf import settings

def send_message(phone,code,TemplateID="1201306" ):
    '''
    #4, 发送短信  购买服务器进行短信服务：阿里云/腾讯云
            #4.1 创建应用 SDK AppID 1400597521
            #4.2 申请签名 ID 419121 名称 裂脑壳
            #4.3 创建模板 ID 1201306 模板名称 minprogram
            #4.4 腾讯云API SecretId:   SecretKey:
            #4.5 调用相关接口发短信
    :return:
    '''
    CHINA = "+86"
    phone = "{}{}".format(CHINA, phone)
    try:
        cred = credential.Credential(settings.TENCENT_SECRET_ID, settings.TENCENT_SECRET_KEY)

        client = sms_client.SmsClient(cred, settings.TENCENT_CITY)

        req = models.SendSmsRequest()
        # 短信应用 ID: 在 [短信控制台] 添加应用后生成的实际 SDKAppID，例如1400006666
        req.SmsSdkAppid = settings.TENCENT_SDK_APPID
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名，可登录 [短信控制台] 查看签名信息
        req.Sign = settings.TENCENT_SIGN
        req.PhoneNumberSet = [phone, ]
        # 模板 ID: 必须填写已审核通过的模板 ID，可登录 [短信控制台] 查看模板 ID
        req.TemplateID = TemplateID
        # 模板参数: 若无模板参数，则设置为空
        req.TemplateParamSet = [code, ]

        # 通过 client 对象调用 SendSms 方法发起请求。注意请求方法名与请求对象是对应的
        resp = client.SendSms(req)

        # 输出 JSON 格式的字符串回包
        print(resp.to_json_string(indent=2))
        if(resp.SendStatusSet[0].code=="Ok"):
            return True
    except TencentCloudSDKException as err:
        pass