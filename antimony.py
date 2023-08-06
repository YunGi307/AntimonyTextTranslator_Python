from urllib.parse import quote
from os import path

import requests

from charimg import CharImg
from database import metachars, trans. SPEC

DIR_PATH = 'C:/锑星文图象/'  # 储存锑星文字图片的文件夹，请自行修改



class Antimony:
    '''单个锑星字符'''
    def __init__(self, raw: str, use_api=True):
        self.raw = raw
        self.char = self.find_char()
        if self.char is None:
            raise ValueError(f'cannot translate {self.raw}')
        self.inunicode =  self.char[0] not in '⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻'
        if self.char in 'vwxyz':  # 这些字符需要下标
            self.img = CharImg(self.char, small=True, use_api=use_api)
        else:
            self.img = CharImg(self.char, use_api=use_api)
    
    def __repr__(self):
        return f'<AntimonyChar, raw={self.raw}>'
    
    def find_char(self):
        """在映射表里找到该字符"""
        if self.raw in metachars:
            return metachars[self.raw]
        if self.raw in SPEC:
            return SPEC[self.raw]
        return trans.get(self.raw, None)
    
    def to_html_code(self):
        return self.img.html


class Antimonys:
    '''一句锑星文字组成的话'''
    def __init__(self, raw: str, use_api=True):
        self.raw = raw
        self.splits = []
        for i in range(len(raw)):
            right = raw[i: i + 2]
            if right in metachars:
                self.splits.append(right)
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
                result.append(str(c).replace(' ', '&nbsp;' * 4).replace('\n', '<br/>'))
        return ''.join(result)
    
    def write_html(self, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_html_code())
    
def pre(text: str):
    """预处理文本"""
    res = text.replace('Δ', '△')
    return res

