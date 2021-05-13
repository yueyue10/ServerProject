import json
import base64
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models


def test(img_base):
    try:
        cred = credential.Credential("AKIDnQq0uYw4vVoqa3GDtIRKxKQFo56rNhml", "rcASVIp54mDNHuHF0UjjTxCbkdFaeRzI")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)
        req = models.GeneralHandwritingOCRRequest()
        params = {
            "ImageBase64": img_base
        }
        req.from_json_string(json.dumps(params))
        resp = client.GeneralHandwritingOCR(req)
        print(resp.to_json_string())
    except TencentCloudSDKException as err:
        print(err)


def read_text():
    with open("t6.png", 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        test(s)


if __name__ == '__main__':
    read_text()
