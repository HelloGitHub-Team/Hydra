# -*- coding=utf-8 -*-
"""
@FileName: operation_juejin.py
@Author: JunDay
@Date: 2019/7/6
@Doc describing: 掘金网相关操作
"""

import requests

class JueJin(object):
    """ 掘金网相关操作类 """

    def __init__(self, phone, pwd):
        self.phone_number = phone
        self.password = pwd
        self.user_info = self.login()

    def login(self):
        """ 登录方法 """
        url = "https://juejin.im/auth/type/phoneNumber"
        params = {
            "phoneNumber" : self.phone_number,
            "password" : self.password
        }

        res = requests.post(url, json=params)
        if res.status_code == 200:
            return res.json()
        return {}

    @property
    def token(self):
        """ 获取登录后 token 的方法 """
        token = self.user_info.get('token')
        return token

    @property
    def client_id(self):
        """ 获取用户 clientId 的方法 """
        client_id = self.user_info.get('clientId')
        return client_id

    @property
    def user_id(self):
        """ 获取用户 userId 的方法 """
        user_id = self.user_info.get('userId')
        return user_id

    def search_tags(self, key='', amount=100):
        """
        根据关键字搜索标签的方法
        Args:
            key: 需要进行搜索的关键字，默认为空字符串，则搜索全部标签
            amount: 需要显示的最大数量
        Returns:
            搜索出来的全部结果字典
        """
        url = f"https://gold-tag-ms.juejin.im/v1/tag/type/new/search/{key}/page/1/pageSize/{amount}"
        headers = {
            "X-Juejin-Src": "web",
            "X-Juejin-Token": self.token,
            "X-Juejin-Uid": self.user_id
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        return {}

    def categories(self):
        """ 获取分类列表方法 """
        url = "https://gold-tag-ms.juejin.im/v1/categories"
        headers = {
            "X-Juejin-Src": "web",
            "X-Juejin-Token": self.token,
            "X-Juejin-Uid": self.user_id
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        return {}

    def create_draft(self, title, category, markdown='', html='', content='', type='markdown'):
        """
        新建草稿方法,
        todo: 暂时还没有加标签的功能，待添加(目前是写死的一个标签)
        Args:
            title: 文章标题
            category: 文章分类 ID
            markdown: markdown 文本内容，默认为空字符
            html: html 文本内容，默认为空字符
            content: 内容，默认为空字符
            type: 发布类型，默认为 markdown
        Returns:
            创建好的草稿 ID
        """
        url = "https://post-storage-api-ms.juejin.im/v1/draftStorage"
        params = {
            "uid" : self.user_id,
            "device_id" : self.client_id,
            "token" : self.token,
            "src" : "web",
            "category" : category,
            "content" : content,
            "html" : html,
            "markdown" : markdown,
            "screenshot" : "",
            "isTitleImageFullscreen" : "",
            "tags" : "5597acede4b08a686ce6b36c",
            "title" : title,
            "type" : type
        }
        res = requests.post(url, data=params)
        if res.status_code == 200:
            post_id = res.json().get('d')[0]
            return post_id
        else:
            raise Exception(f"文章创建失败，接口返回内容:{res.text}")


    def publish_draft(self, post_id):
        """
        发布草稿方法
        Args:
            post_id: 草稿 ID，由发布草稿接口返回
        Returns:
            是否发布成功
        """
        url = "https://post-storage-api-ms.juejin.im/v1/postPublish"
        params = {
            "uid" : self.user_id,
            "device_id" : self.client_id,
            "token" : self.token,
            "src" : "web",
            "postId" : post_id
        }
        res = requests.post(url, data=params)
        if res.json().get('m') != r"文章已发布":
            raise Exception(f"文章发布失败，接口返回内容:{res.text}")
        return True

    def upload_pic(self, file_path, protocol='https'):
        """
        上传图片方法
        Args:
            file_path: 图片在本地的路径
            protocol: 返回链接的协议，默认为 HTTPS，可选还有 HTTP
        Returns:
            指定协议的图片资源链接
        """
        url = "https://cdn-ms.juejin.im/v1/upload?bucket=gold-user-assets"
        files = {"file" : open(file_path, 'rb')}

        res = requests.post(url, files=files)
        if res.status_code == 200:
            pic_uri = res.json().get('d').get('url').get(protocol)
            return pic_uri
        else:
            raise Exception(f"图片上传失败，接口返回内容:{res.text}")

    def get_link_info(self, link):
        """
        抓取链接中的内容方法
        Args:
            link: 链接地址
        Returns:
            网页链接的标题和头图
        """
        url = "https://parser-ms.juejin.im/v1/link/info"
        params = {
            "url" : link,
            "src" : "web"
        }

        res = requests.get(url, params=params)
        if res.status_code == 200:
            title = res.json().get("d").get("title")
            thumb = res.json().get("d").get("thumb")
            return (title, thumb)
        else:
            # raise Exception(f"信息抓取失败，接口返回内容:{res.text}")
            return ('', '')

    def create_boiling(self, content, pictures, url='', url_title='', url_pic='', topic_id=''):
        """
        发布沸点方法
        Args:
            content: 沸点内容，必需
            pictures: 图片地址，没有图片时传空字符串，有多张图片时传列表
            url: 链接，默认为空
            url_title: 链接标题，默认为空
            url_pic: 链接图片，默认为空
            topic_id: 话题 ID，默认为空
        Returns:
            是否发布成功
        """
        if isinstance(pictures, list):
            pictures = [''.join([picture, '|']) for picture in pictures]
            pictures = ''.join(pictures)[:-2]
        api_url = "https://short-msg-ms.juejin.im/v1/create"
        params = {
            "uid" : self.user_id,
            "device_id" : self.client_id,
            "token" : self.token,
            "src" : "web",
            "content" : content,
            "pictures" : pictures,
            "url" : url,
            "urlTitle" : url_title,
            "urlPic" : url_pic,
            "topicId" : topic_id
        }

        res = requests.post(api_url, data=params)
        if res.json().get('m') != "success":
            raise Exception(f"沸点发布失败，接口返回内容:{res.text}")
        return True


def publish_boiling(phone, pwd, **kwargs):
    """
    完整发布沸点的方法
    Args:
        phone: 登录账号的手机号码
        pwd: 登录账号的密码
        content: 沸点内容，必需
        url: 链接
        url_title: 链接标题
        url_pic: 链接图片
        topic_id: 话题 ID
        file_paths: 图片在本地的路径，有多张图片时以列表形式传入
        protocol: 返回链接的协议，默认为 HTTPS，可选还有 HTTP
        extract_link: 是否提取链接中的标题和头图，默认为否，如果传 True 则
                      从网页链接（url字段）中提取出标题（url_title）和图片（url_pic）
    Returns:
        发布的结果
    """
    juejin = JueJin(phone, pwd)
    kwargs.setdefault('protocol', 'https')
    # 根据传进来的文件路径列表上传图片后，获取图片资源路径
    if kwargs.get('file_paths'):
        kwargs['pictures'] = [juejin.upload_pic(file_path, kwargs.get('protocol'))
                              for file_path in kwargs.get('file_paths')]
    # 从网页链接中获取标题和头图
    if kwargs.get('url') and kwargs.get('extract_link'):
        kwargs['url_title'], kwargs['url_pic'] = juejin.get_link_info(kwargs.get('url'))

    kwargs.pop('file_paths')
    kwargs.pop('protocol')
    kwargs.pop('extract_link')

    # 发布沸点
    juejin.create_boiling(**kwargs)


if __name__ == "__main__":
    data = {
        "phone" : "登录手机号码",
        "pwd" : "登录密码",
        "content" : "测试发布沸点，添加了一个链接和两张相同的图片",
        "url" : "https://www.cnblogs.com/bigberg/p/8259903.html",
        "file_paths" : ['Snipaste_2019-07-08_18-55-12.png', 'Snipaste_2019-07-08_18-55-12.png'],
        "extract_link" : True
    }
    publish_boiling(**data)
