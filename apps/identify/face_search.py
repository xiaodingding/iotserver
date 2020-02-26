import sys
import io
import urllib.request
import http.cookiejar


class Face_search:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance:
            return cls.__instance
        else:
            # cls._instance = super(object, cls).__new__(cls, *args, **kwargs)
            cls.__instance = object.__new__(Face_search)
        return  cls.__instance

    def __init__(self):
        # from .captcha import CaptchaIdentify
        super(Face_search, self).__init__()
        # self.captcha = CaptchaIdentify()

    def start(self):
        print("--------single mode start---------")

    def captcha_url(self, url):
        print("开始测试验证码识别功能")
        result = ""
        # result = self.captcha.recgImgFromUrl(url)
        print("识别结果", result)
        return result

    def captcha_image(self, image):
        print("开始测试验证码识别功能")
        result = ""
        # result = self.captcha.recgImgFromImg(image)
        print("识别结果", result)
        return result

Face_Search = Face_search()
