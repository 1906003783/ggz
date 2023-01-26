import json
import csv
import re
from bs4 import BeautifulSoup


def json2csv(input,out,d_halo,col=[],col_c=[],mode="w",encoding="utf-8"):
        with open(input,'r',encoding=encoding) as f:
            datas=json.load(f)
            if mode=="w":
                loader=[tuple(col+col_c)]
            else:
                loader=[]
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
                    loader.append(tuple([data[c] for c in col]+eq+w_match+[str(s_halo)]+[bit_h]))
            with open(out,mode=mode,newline="",encoding=encoding) as f2:
                writer=csv.writer(f2)
                writer.writerows(loader)


class JsonLoader():
    def __init__(self,inputs,d_halo,col=[],col_c=[],encoding="utf-8") -> None:
        self.encoding=encoding
        self.d_halo=d_halo
        self.col=col
        self.col_c=col_c
        self.encoding=encoding
        self.loader=[self.json_proc(inputs[0],d_halo,col,col_c,mode="w",encoding=encoding)]
        for i in range(1,len(inputs)):
            self.loader.append(self.json_proc(inputs[i],d_halo,col,col_c,mode="a+",encoding=encoding))

    def json_add(self,input):
        self.mode="a+"
        ld=self.json_proc(input,d_halo=self.d_halo,col=self.col,col_c=self.col_c,mode="a+",encoding=self.encoding)
        self.loader.append(ld)
    
    def json2csv(self,out):
        with open(out,mode="w",newline="",encoding=self.encoding) as f2:
            writer=csv.writer(f2)
            for ld in self.loader:
                writer.writerows(ld)

    def json_proc(self,input,d_halo,col=[],col_c=[],mode="w",encoding="utf-8"):
        self.mode=mode
        self.encoding=encoding
        with open(input,'r',encoding=encoding) as f:
            datas=json.load(f)
            if mode=="w":
                loader=[tuple(col+col_c)]
            else:
                loader=[]
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
                    loader.append(tuple([data[c] for c in col]+eq+w_match+[str(s_halo)]+[bit_h]))
            return loader

if __name__=="__main__":
    from conf import DefaultConfig
    #配置
    cfg_c=DefaultConfig()
    cfg=cfg_c.cfg
    n_chara=cfg['n_chara']
    date_i=cfg["date_i"]
    mysql=cfg["mysql"]["config"]
    halo=cfg["halo"]

    col=tuple(cfg["col"])
    col_c=tuple(cfg["col_c"])
    jloader=JsonLoader(["data/m.json","data/i.json"],d_halo=halo,col=col,col_c=col_c)
    jloader.json2csv("data/rlt.csv")

