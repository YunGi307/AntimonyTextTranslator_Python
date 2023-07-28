from urllib.parse import quote
from os import path

import requests

metachars = {
'Cl': '盐',
'Fe': '铁',
'3': '官',
'H': '基',
'In': '音',
'Sb': '锑',
'Na': '食',
'△': '热',
'⌬': '苯'
}

DIR_PATH = 'C:/锑星文图象/'  # 自行修改

def stru(text: str, s=0, adding: str=''):
    """
    构成汉字结构
    s: 结构编码，如下
    0 1 2 3  4 5 6 7 8 9 10 11
    ⿰⿱⿲ ⿳ ⿴⿵ ⿶⿷⿸ ⿹ ⿺ ⿻
    adding: 附加偏旁
    """
    if isinstance(s, int):
        trans = \
        ['0 1 2 3  4 5 6 7 8 9 10 11',
         '⿰⿱⿲ ⿳ ⿴⿵ ⿶⿷⿸ ⿹ ⿺ ⿻'.replace(' ', '')]
        if adding:
           return stru(trans[1][s] + text, adding)
        else:
            return trans[1][s] + text
    elif isinstance(s, str) and adding == '':
        if s == '气':  # 添加气字头
            return stru(s + text, 9)
        else:  # 添加偏旁
            return stru(s + text, 0)
    else:
        raise ValueError(f'{text}')

# “石”为顺时针旋转90度，“酉”为逆时针旋转90度
# “气”为旋转180度，“氵”为水平翻转，“火”为竖直翻转
# “手”为字符翻转后与原字符结合

trans = {
'0': stru('土土', 0),
'1': '血',
'2': '宜',
'3': '官',
'4': stru('扌囬'),
'5': stru('饣㠯'),
'6': stru('土㠯'),
'7': stru('目扌', 1),
'8': stru('手官'),
'9': stru(stru('土㠯'), '气')
}

map = (stru('目丸', 0 , '扌'), stru('皿官'), '圤', 
       stru(stru('卜土', 1), '皿'), '钼',
       '金', stru('圤目'), '基', '立', stru('皿廾', 1),
       stru('扌丸', 1, '皿'), stru('火饣'),
       stru('亻皿'), '人', stru('圤土'), stru('皿宀', 1),
       stru('土丸', 1, '圤'), stru('皿' + stru('宀丸', 1), 1),
       stru('圤' + stru('卜土'), 1), stru('目皿', 1),
       stru(stru('皿十', 1) + stru('皿十', 1)), stru('丸扌'), stru('丸亻'),
       stru(stru('丸扌') + '执', 1), stru(stru('丸扌') + '皿', 1), stru('石人'),
       
       '良', '弟', stru('氵㠯'), '涕', '失', stru('艹' + stru('目皿', 1), 1),
       stru('火良'), stru('皿日', 1), stru('口皿', 1), stru(stru('口皿', 1) + '廾', 1),
       stru('皿' + stru('扌丸', 1), 1), '皿', '田', '日', stru('手㠯'), '焍',
       stru('弟', '气'), stru('皿丶', 1), stru(stru('氵宀') + '㠯', 1),
       stru('皿' + stru('目廾', 1), 1), stru('日', '气'),
       stru('丸扌'), stru('丸亻'), stru(stru('丸扌') + '执', 1),
       stru(stru('丸扌') + '扌', 1), stru('石人')
       )
       
for i in range(len(map)):
    trans.update({'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'[i]: map[i]})


class CharImg:
    def __init__(self, code: str, ext='svg', small=False, use_api=True):
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
        # 我的 html 烂的一批...
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
        with requests.get(self.url) as req:
            response = req.content
        with open(path, 'wb') as f:
            f.write(response)
    
    



class Antimony:
    '''单个锑星字符'''
    def __init__(self, raw: str, use_api=True):
        self.raw = raw
        assert (len(self.raw) == 1) or (self.raw in metachars)
        self.char = self.find_char()
        if self.char is None:
            raise ValueError(f'cannot translate {self.raw}')
        self.inunicode =  self.char[0] not in '⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻'
        if self.char in 'vwxyz':
            self.img = CharImg(self.char, small=True, use_api=use_api)
        else:
            self.img = CharImg(self.char, use_api=use_api)
    
    def __repr__(self):
        return f'<AntimonyChar, raw={self.raw}>'
    
    def find_char(self):
        res = metachars.get(self.raw, None)
        if res is not None:
            return res
        return trans.get(self.raw, None)
    
    def to_html_code(self):
        return self.img.html


class Antimonys:
    '''一句锑星文字组成的话'''
    def __init__(self, raw: str, use_api=True):
        self.raw = raw
        self.splits = []
        for i in range(len(raw)):
            if raw[i: i + 2] in metachars:
                self.splits.append(raw[i: i + 2])
            elif raw[i - 1: i + 1] in metachars:
                continue
            else:
                self.splits.append(raw[i])
        self.chars = []
        for c in self.splits:
            try:
                self.chars.append(Antimony(c, use_api))
            except ValueError:
                self.chars.append(c)
    
    def __repr__(self):
        return f'<Antimonys, raw={self.raw}>'
    
    def to_html_code(self):
        header = self.raw
        result = []
        for c in self.chars:
            if isinstance(c, Antimony):
                result.append(c.to_html_code())
            else:
                result.append(str(c).replace(' ', '&nbsp;' * 4))
        return ''.join(result)
    
    def write_html(self, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_html_code())
    
def pre(text: str):
    """预处理文本"""
    res = text.replace('Δ', '△')
    return res

