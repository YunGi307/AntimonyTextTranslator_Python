from antimony import per, Antimonys


while True:
    raw = pre(input('>>> '))
    ams =  Antimonys(raw.replace('\n', ''), use_api=True)
    ams.write_html('C:/Result.html')
    
