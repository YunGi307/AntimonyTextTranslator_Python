from antimony import pre, Antimonys


while True:
    raw = pre(input('>>> '))
    ams =  Antimonys(raw.replace('\n', ''), use_api=True)  # 使用网络提供图片
    ams.write_html('C:/Result.html')
    
