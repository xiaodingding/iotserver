from django.apps import AppConfig
# from identify.face_search import Face_Search

class IdentifyConfig(AppConfig):
    name = 'identify'
    # def ready(self):
    #     face  = Face_Search
    #     print("identify single test", id(Face_Search))
    #     captchaURL = r"https://www.zhihu.com/captcha.gif?type=login"
    #     face.captcha_url(captchaURL)
    #     print(face)
