# 元字符
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


def stru(text: str, s=0, adding: str=''):
    """
    构成汉字结构
    s: 结构编码，如下
    0 1 2 3  4 5 6 7 8 9 10 11
    ⿰⿱⿲ ⿳ ⿴⿵ ⿶⿷⿸ ⿹ ⿺ ⿻
    adding: 附加偏旁
    """
    if isinstance(s, int):
        trans = '⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻'
        if adding:
           return stru(trans[s] + text, adding)
        else:
            return trans[s] + text
    elif isinstance(s, str) and adding == '':
        if s == '气':  # 添加气字头
            return stru(s + text, 9)
        else:  # 添加左右结构的偏旁
            return stru(s + text, 0)
    else:
        raise ValueError(text)

# 在锑星文字中
# “石”为顺时针旋转90度，“酉”为逆时针旋转90度
# “气”为旋转180度，“氵”为水平翻转，“火”为竖直翻转
# “手”为字符翻转后与原字符结合

# 映射表
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

# 英文字母直接按照顺序写了，一个一个手写映射太麻烦，下面会用一个循环直接生成映射表
map = (stru('目丸', 0 , '扌'), stru('皿官'), '圤', 
       stru(stru('卜土', 1), '皿'), '钼',
       '金', stru('圤目'), '基', '立', stru('皿廾', 1),
       stru('扌丸', 1, '皿'), stru('火饣'),
       stru('亻皿'), '人', stru('圤土'), stru('皿宀', 1),
       stru('土丸', 1, '圤'), stru('皿' + stru('宀丸', 1), 1),
       stru('圤' + stru('卜土'), 1), stru('目皿', 1),
       stru(stru('皿十', 1) + stru('皿十', 1)), stru('丸扌'), stru('丸亻'),
       stru(stru('丸扌') + '执', 1), stru(stru('丸扌') + '皿', 1), stru('石人'),
       # 下面是小写字母
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


# 特殊单词
SPEC = {'Ce': '垁',
        'Fb': stru(stru('圤' + stru('卜土', 0), 1) + '弟', 0),
        'Ca', '埌'}