import requests


class CharImg:
    def __init__(self, code: str, ext='svg', small=False, use_api=True):
        """code: 文字的结构编码，比如 "⿰钅圆"
        ext: 文件扩展名，只能是 svg 或者 png
        small: 该字符是否为下标
        use_api: 是否用网络提供图片，如果为 False ，则第一次会自动从网络下载图片到本地，并使用本地图片，不再依赖网络"""
        self.code = code
        self.ext = ext.lower().lstrip('.')
        assert self.ext in ['svg', 'png']
        self.use_api = use_api
        self.encoding = quote(self.code)
        self.url = f'http://zu.zi.tools/{self.encoding}.{self.ext}'
        
        self.inunicode =  self.code[0] not in '⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻'

        if self.inunicode:
            if small:
                self.html = '<small><small>' + self.code + '</small></small> '
            else:
                self.html = self.code + ' '
        else:
            if self.use_api:  # 使用网络 api 插入图片
                src = self.url
            else:  # 使用本地文件
                src = path.join(DIR_PATH, f'{self.code}.{self.ext}')
                if not path.exists(src):
                    self.to_file(src)
            if small:
                self.html = f'<img src="{src}" alt="{src}" ' + \
                             'style="vertical-align:middle;position:relative;top:1px;" ' + \
                             'height="12.5px"/>\n'
            else:
                self.html = f'<img src="{src}" alt="{src}" ' + \
                             'style="vertical-align:middle;position:relative;top:-2px;" ' + \
                             'height="18px"/>\n'
            
        
    def to_file(self, path: str):
        """下载该字符的图片"""
        with requests.get(self.url) as req:
            response = req.content
        with open(path, 'wb') as f:
            f.write(response)

