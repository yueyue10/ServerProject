import cv2
import json
import base64
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models


class OcrSdk(object):
    def __init__(self):
        pass

    def read_text_cv(self, cv_img):
        img_base = self.cv_img_to_base64(cv_img)
        text_list = self.ocr_text(img_base)
        print("text_list", text_list)
        texts = []
        for text in text_list:
            texts.append(text.DetectedText)
        print("texts=======", texts)
        return texts

    def read_text_local(self, path="t6.png"):
        with open(path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            self.ocr_text(s)

    @staticmethod
    def cv_img_to_base64(image_np):
        image = cv2.imencode('.jpg', image_np)[1]
        image_code = str(base64.b64encode(image))[2:-1]
        return image_code

    @staticmethod
    def ocr_text(img_base):
        try:
            cred = credential.Credential("AKIDnQq0uYw4vVoqa3GDtIRKxKQFo56rNhml", "rcASVIp54mDNHuHF0UjjTxCbkdFaeRzI")
            http_profile = HttpProfile()
            http_profile.endpoint = "ocr.tencentcloudapi.com"
            client_profile = ClientProfile()
            client_profile.httpProfile = http_profile
            client = ocr_client.OcrClient(cred, "ap-beijing", client_profile)
            req = models.GeneralHandwritingOCRRequest()
            params = {
                "ImageBase64": img_base
            }
            req.from_json_string(json.dumps(params))
            resp = client.GeneralHandwritingOCR(req)
            print("read_text========", resp.to_json_string())
            return resp.TextDetections
        except TencentCloudSDKException as err:
            print("read_text=======", err)


if __name__ == '__main__':
    ocr = OcrSdk()
    ocr.read_text_local()
