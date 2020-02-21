import sys
import io
import urllib.request
import http.cookiejar

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

#登录时需要POST的数据
data = {'username':'1',
        'password':'1',
        'captcha':
        'goto:http':'//ssfw.xmu.edu.cn/cmstar/loginSuccess.portal',
        'gotoOnFail:http':'//ssfw.xmu.edu.cn/cmstar/loginFailure.portal'}
post_data = urllib.parse.urlencode(data).encode('utf-8')

#设置请求头
headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

#登录时表单提交到的地址（用开发者工具可以看到）
login_url = ' http://ssfw.xmu.edu.cn/cmstar/userPasswordValidate.portal

#构造登录请求
req = urllib.request.Request(login_url, headers = headers, data = post_data)

#构造cookie
cookie = http.cookiejar.CookieJar()

#由cookie构造opener
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

#发送登录请求，此后这个opener就携带了cookie，以证明自己登录过
resp = opener.open(req)
