# -*- coding: utf-8 -*-
import oss2
import os
from oss2.credentials import EnvironmentVariableCredentialsProvider

# https://help.aliyun.com/zh/oss/developer-reference/preface?spm=a2c4g.11186623.0.0.44515168ytKEOl#concept-32026-zh
class OssManager:
    def __init__(self, bucket_name="mrch", is_internal=True):
        # 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
        # auth = oss2.Auth("LTAI5t9QG6d2HBuVfTRqJBMA", "xcnVBg18xSXAo4OfRKnnzs0Xx3oAOq")
        auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
        # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        # 填写Bucket名称。
        # 内网endpoint是oss-cn-shanghai-internal.aliyuncs.com，进行切换。
        end_point = "https://oss-cn-shanghai.aliyuncs.com"
        if is_internal:
            end_point = "oss-cn-shanghai-internal.aliyuncs.com"

        self.bucket = oss2.Bucket(auth, end_point, bucket_name)

    def put_object(self, file_name, put_object, prefix_name="task_info"):
        # result = bucket.put_object('exampleobject.txt', 'Hello OSS', headers=headers)
        result = self.bucket.put_object("{}/{}".format(prefix_name, file_name), put_object)

        # HTTP返回码。
        print('http status: {0}'.format(result.status))
        # 请求ID。请求ID是本次请求的唯一标识，强烈建议在程序日志中添加此参数。
        print('request_id: {0}'.format(result.request_id))
        # ETag是put_object方法返回值特有的属性，用于标识一个Object的内容。
        print('ETag: {0}'.format(result.etag))
        # HTTP响应头部。
        print('date: {0}'.format(result.headers['date']))

        return result.status

    def put_file(self, local_file_path, file_name="", prefix_name="user_picture"):
        # 填写Object完整路径和本地文件的完整路径。Object完整路径中不能包含Bucket名称。
        # 如果未指定本地路径，则默认从示例程序所属项目对应本地路径中上传文件。
        if not file_name:
            (file, put_filename) = os.path.split(local_file_path)
        else:
            put_filename = file_name
        result = self.bucket.put_object_from_file("{}/{}".format(prefix_name, put_filename), local_file_path)
        print("put file {} to {} succ".format(put_filename, prefix_name))

        # HTTP返回码。
        print('http status: {0}'.format(result.status))
        # 请求ID。请求ID是本次请求的唯一标识，强烈建议在程序日志中添加此参数。
        print('request_id: {0}'.format(result.request_id))
        # ETag是put_object方法返回值特有的属性，用于标识一个Object的内容。
        print('ETag: {0}'.format(result.etag))
        # HTTP响应头部。
        print('date: {0}'.format(result.headers['date']))
        return result

    def get_file(self, local_file_path, file_name, prefix_name):
        # -*- coding: utf-8 -*-
        self.bucket.get_object_to_file("{}/{}".format(prefix_name, file_name), local_file_path)

    def get_file_url(self, object_name, valid_time=3600):
        # 填写Object完整路径，例如exampledir/exampleobject.txt。Object完整路径中不能包含Bucket名称。

        # 生成下载文件的签名URL，有效时间为3600秒。
        # 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用。
        url = self.bucket.sign_url('GET', object_name, valid_time, slash_safe=True)
        print('签名URL的地址为：', url)
        return url

def download_file_from_url(url, local_file_path):
    # -*- coding: utf-8 -*-
    import oss2
    import requests

    # 填写步骤1生成的签名URL。
    # 通过签名URL下载文件，以requests为例说明。
    resp = requests.get(url)

    # 填写下载到本地文件的完整路径。
    with open(local_file_path, "wb") as code:
        code.write(resp.content)
    return

if __name__=='__main__':

    import json
    # oss_manager = OssManager(bucket_name="mrch")
    # oss_manager.put_file("/Users/shirley/Desktop/psycho/psychic-potato/AutoGenOne/picture/test_guofeng.png",
    #                      "test_guofeng.png",
    #                      "picturea")
    # # 获得文件分享url
    # url = oss_manager.get_file_url('pic_waitlist/00000101901710.898072467417163.png')

    # 上传字符串
    # file_name = "0_17220005234391468/novel_dict"
    # put_object = "role_name_dict_v1:" + json.dumps({"他": ["刘洋"], "唐梦婷": [], "赵明": [], "美女幸存者": ["美术生", "女孩"], "女孩子": []}, ensure_ascii=False)
    # oss_manager.put_object(file_name, put_object, prefix_name="task_info")
    # put_object = "roleGen_cost:0.0015748000000000001"
    # oss_manager.put_object(file_name, put_object, prefix_name="task_info")
    # 【上传/下载模型】
    # 模型文件在 bucket_name="qnaipic"
    oss_manager = OssManager(bucket_name="qnaipic")
    # 从本地上传文件到oss
    # https://openmodeldb.info/models/2x-sudo-RealESRGAN
    # oss_manager.put_file("D:\\ComfyUI\\models\\upscale_models\\RealESRGAN_x4plus.pth",
    #                      "RealESRGAN_x4plus.pth",
    #                      "models")
    # oss_manager.put_file("D:\ComfyUI\models\loras.zip",
    #                      "loras.zip",
    #                      "models")
    # oss_manager.put_file("D:\QingNingFiles\psychic-potato\models\sfts\sdxlNijiSeven_sdxlNijiSeven.safetensors",
    #                      "sdxlNijiSeven_sdxlNijiSeven.safetensors",
    #                      "models")

    # 下载comfyui必备插件、模型
    # ComfyUI_PATH = "D:\\ComfyUI\\"  # 请修改为本地comfyui目录
    # oss_manager.get_file(f"{ComfyUI_PATH}/custom_nodes.tar.gz", "custom_nodes.tar.gz", "models")
    # oss_manager.get_file(f"{ComfyUI_PATH}/models/checkpoints/animagineXLV31_v31.safetensors", "animagineXLV31_v31.safetensors", "models")
    # oss_manager.get_file(f"{ComfyUI_PATH}/models/checkpoints/kohakuXLBeta_beta7.safetensors", "kohakuXLBeta_beta7.safetensors", "models")
    # oss_manager.get_file(f"{ComfyUI_PATH}/models/checkpoints/sdxlNijiSeven_sdxlNijiSeven.safetensors", "sdxlNijiSeven_sdxlNijiSeven.safetensors", "models")
    # oss_manager.get_file(f"{ComfyUI_PATH}/models/loras.zip", "loras.zip", "models")
    # oss_manager.get_file(f"{ComfyUI_PATH}/models/sams.zip", "sams.zip", "models")
    # oss_manager.get_file(f"{ComfyUI_PATH}/models/ultralytics.zip", "ultralytics.zip", "models")
    # oss_manager.get_file(f"{ComfyUI_PATH}/models/upscale_models/2x-sudo-RealESRGAN.pth", "2x-sudo-RealESRGAN.pth", "models")