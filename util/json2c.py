import json
import csv
import re
from bs4 import BeautifulSoup
from conf import DefaultConfig

def json2csv(input,out,d_halo,col=[],col_c=[],mode="w",encoding="utf-8"):
        with open(input,'r',encoding=encoding) as f:
            datas=json.load(f)
            if mode=="w":
                fcsv=[tuple(col+col_c)]
            else:
                fcsv=[]
            for data in datas["data"]["data"][0]["rows"]:
                if data["char"]=="野怪":
                    pass
                else:
                    bs = BeautifulSoup(data["log"],"html.parser")
                    l_eq=bs.find_all(name="button",attrs={"data-original-title":True},limit=8)[4:]
                    eq=list()
                    for e in l_eq:
                        eq+=[e.attrs['data-original-title'],e.text ]    #装备
                    tf=bs.find(name="div",attrs={"class":"col-md-7 fyg_tl"})    #属性
                    w_match=re.findall("(?<=:)\d+(?=])",tf.text)
                    halo=bs.find(name="div",attrs={"class":"col-md-5 fyg_tr"})  #光环
                    s_halo=re.findall(r"(?<=\|)[^|]\S{3}(?=|)",halo.text)
                    bit_h=0
                    for h in s_halo:
                        bit_h+=(2**d_halo[h])
                    fcsv.append(tuple([data[c] for c in col]+eq+w_match+[s_halo]+[bit_h]))
            with open(out,mode=mode,newline="",encoding=encoding) as f2:
                writer=csv.writer(f2)
                writer.writerows(fcsv)

if __name__=="__main__":
    #配置
    cfg_c=DefaultConfig()
    cfg=cfg_c.cfg
    n_chara=cfg['n_chara']
    date_i=cfg["date_i"]
    mysql=cfg["mysql"]["config"]
    halo=cfg["halo"]

    col=tuple(cfg["col"])
    col_c=tuple(cfg["col_c"])
    json2csv("data/m.json","data/rlt.csv",d_halo=halo,col=col,col_c=col_c)
    json2csv("data/i.json","data/rlt.csv",d_halo=halo,col=col,col_c=col_c,mode="a+")

