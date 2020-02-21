import os
import sys
import requests

from io import BytesIO
import tensorflow as tf
from PIL import Image
from identify import captcha_utils as utils
from identify import orcmodel
import numpy as np
from django.conf import settings
from common.utils import get_logger

try:
    type (eval('model'))
except:
    model = orcmodel.LSTMOCR('infer')
    model.build_graph()

config = tf.ConfigProto(allow_soft_placement=True)
checkpoint_dir= settings.CHECKPOINT or os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkpoint")

logger = get_logger(__name__)

class CaptchaIdentify():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.zhihu.com",
        "Upgrade-Insecure-Requests": "1",}

    #/root/src/iotweb/apps/identify/templates
    #/root/src/iotweb/data/checkpoint

    def __init__(self):
        # if sys.path[0]: os.chdir(sys.path[0])  # 设置脚本所在目录为当前工作目录
        # 恢复权重
        logger.debug("checkpoint_dir:{}".format(checkpoint_dir))
        self.__sess = self.__restoreSess(checkpoint_dir)
        # 维护一个会话
        self.__session = requests.Session()
        self.__session.headers = self.headers #为了伪装，设置headers


    # 恢复权重
    def __restoreSess(self, checkpoint=checkpoint_dir):

        W = tf.Variable(60, dtype=tf.float32, name='image_height')
        b = tf.Variable(150, dtype=tf.float32, name='image_width')

        sess=tf.Session(config=config)
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=100)
        ckpt = tf.train.latest_checkpoint(checkpoint)

        if ckpt:
            #回复权限，这里连 global_step 也会被加载进来
            saver.restore(sess, ckpt)
            # print('restore from the checkpoint{0}'.format(ckpt))
            logger.debug('已加载checkpoint{0}'.format(ckpt))
        else:
            logger.debug('警告：未加载任何chechpoint')
            logger.debug('如果这不是你预期中的，请确保以下目录存在可用的checkpoint:\n{0}'.format(checkpoint_dir))
        return sess

    def recgImgFromImg(self, img):
        """
        可以在线测试验证码识别功能
        参数：
            img 一个 (60, 150) 的图片
        """
        im = np.array(img.convert("L")).astype(np.float32)/255.
        im = np.reshape(im, [60, 150, 1])
        inp=np.array([im])
        seq_len_input=np.array([np.array([64 for _ in inp], dtype=np.int64)])
        #seq_len_input = np.asarray(seq_len_input)
        seq_len_input = np.reshape(seq_len_input, [-1])
        imgs_input = np.asarray([im])
        feed = {model.inputs: imgs_input,model.seq_len: seq_len_input}
        dense_decoded_code = self.__sess.run(model.dense_decoded, feed)
        expression = ''
        for i in dense_decoded_code[0]:
            if i == -1:
                expression += ''
            else:
                expression += utils.decode_maps[i]
        return expression

    def recgImgFromUrl(self, img_url):
        img=Image.open(BytesIO(self.open(img_url).content))
        im = np.array(img.convert("L")).astype(np.float32)/255.
        im = np.reshape(im, [60, 150, 1])
        inp=np.array([im])
        seq_len_input=np.array([np.array([64 for _ in inp], dtype=np.int64)])
        #seq_len_input = np.asarray(seq_len_input)
        seq_len_input = np.reshape(seq_len_input, [-1])
        imgs_input = np.asarray([im])
        feed = {model.inputs: imgs_input,model.seq_len: seq_len_input}
        dense_decoded_code = self.__sess.run(model.dense_decoded, feed)
        expression = ''
        for i in dense_decoded_code[0]:
            if i == -1:
                expression += ''
            else:
                expression += utils.decode_maps[i]
        return expression

    def open(self, url, delay=0, timeout=10):
        """
        打开网页，返回Response对象
        参数：
            delay 整数 延迟多少秒打开，默认不延迟
            timeout 设置最大等待时间，超过该设定时间报超时错误，默认10秒
        """
        if delay:
            time.sleep(delay)
        return self.__session.get(url, timeout=timeout)


