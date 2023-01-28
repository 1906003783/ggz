import json
import csv
import re
from bs4 import BeautifulSoup
import tqdm

class JsonLoader():
    def __init__(self,inputs:list,d_halo:dict,col=[],col_c=[],encoding="utf-8") -> None:
        self.encoding=encoding
        self.d_halo=d_halo
        self.col=col
        self.col_c=col_c
        self.encoding=encoding
        self.loader=[self.json_proc(inputs[0],d_halo,col,col_c,mode="w",encoding=encoding)]
        for i in range(1,len(inputs)):
            self.loader.append(self.json_proc(inputs[i],d_halo,col,col_c,mode="a+",encoding=encoding))

    def export_loader(self) ->list:
        return self.loader

    def json_add(self,inputs:list):
        self.mode="a+"
        for i in range(len(inputs)):
            self.loader.append(self.json_proc(inputs[i],d_halo=self.d_halo,col=self.col,col_c=self.col_c,mode=self.mode,encoding=self.encoding))
    
    def json2csv(self,out:str):
        with open(out,mode="w",newline="",encoding=self.encoding) as f2:
            writer=csv.writer(f2)
            for ld in self.loader:
                writer.writerows(ld)

    def json_proc(self,input:str,d_halo:dict,col=[],col_c=[],mode="w",encoding="utf-8") ->list:
        self.mode=mode
        self.encoding=encoding
        self.halo=d_halo
        with open(input,'r',encoding=encoding) as f:
            datas=json.load(f)
            if mode=="w":
                loader=[tuple(col+col_c)]
            else:
                loader=[]
            for data in tqdm.tqdm(datas["data"]["data"][0]["rows"]):
                if data.get("char") == "野怪":
                    pass
                else:
                    bs = BeautifulSoup(data["log"],"html.parser")
                    l_eq=bs.find_all(name="button",attrs={"data-original-title":True},limit=8)[4:]
                    eq=list()
                    for e in l_eq:
                        eq+=[e.attrs.get('data-original-title'),e.text ]    #装备
                    tf=bs.find(name="div",attrs={"class":"col-md-7 fyg_tl"})    #属性
                    w_match=re.findall("(?<=:)\d+(?=])",tf.text)
                    halo=bs.find(name="div",attrs={"class":"col-md-5 fyg_tr"})  #光环
                    s_halo=re.findall(r"(?<=\|)[^|]\S{3}(?=|)",halo.text)
                    bit_h=0
                    for h in s_halo:
                        bit_h|=(1<<d_halo[h])
                    charinfo=[data[c] for c in col]
                    stat=eq+w_match+[str(s_halo)]+[bit_h]
                    stat2=charinfo+stat
                    col2=col+col_c
                    sdict={col2[i]:i for i in range(len(col2))}
                    loader.append(tuple(stat2+[self.typecheck(stat=stat2,sdict=sdict)]))
            return loader
        
    def isThisHalo(self,gname:str,bit_h:int):
        return bit_h&(1<<(self.halo[gname]))
        
    def typecheck(self,stat:list,sdict:list):
        bit_h=stat[sdict.get('bit_h')]
        chara=stat[sdict.get('char')]
        default="UNKHNOWN"+chara
        weapon=stat[sdict.get('weapon')]
        armor=stat[sdict.get('armor')]
        spd=int(stat[sdict.get('spd')])
        matk=int(stat[sdict.get('matk')])
        if chara == "冥":
            dMING={"反叛者的刺杀弓":"刺杀冥","狂信者的荣誉之刃":"刃冥","荆棘盾剑":"剑盾冥"}
            return dMING.get(weapon,default)
        elif chara == "艾":
            if spd<3000:
                return "低速艾"
            elif spd>8000:
                return "高速艾"
            elif int(stat[sdict.get('pdef')])>4500:
                return "中速艾"
            else:
                return "中速艾_低物防"
        elif chara == "默":
            if weapon == "光辉法杖":
                return "神光默"
            elif matk>20000:
                return "短杖默-高穿"
            else:
                return "短杖默-中穿"
        elif chara == "命":
            dMin={"反叛者的刺杀弓":"刺杀命","饮血魔剑":"神枪命","荆棘盾剑":"低穿转盘命"}
            return dMin.get(weapon,default)
        elif chara == "琳":
            if weapon == "反叛者的刺杀弓":
                return "刺杀琳"
            elif weapon == "狂信者的荣誉之刃":
                return "沸飓琳"
            elif weapon == "幽梦匕首":
                return "飓风琳"
            elif weapon == "荆棘盾剑":
                if self.isThisHalo("点到为止",bit_h) and self.isThisHalo("铁甲尖刺",bit_h):
                    if int(stat[sdict.get('pdef')])>4000:
                        return "高防摆烂琳"
                    else:
                        return "低配摆烂琳"
                elif self.isThisHalo("忍无可忍",bit_h):
                    return "反伤琳_忍"
                else:
                    return "反伤琳"
            else:
                return default
        elif chara == "薇":
            if int(stat[sdict.get('mp')])>200000:
                return "护盾薇"
            elif self.isThisHalo("荧光护盾",bit_h):
                return "荧飓薇"
            elif self.isThisHalo("钝化锋芒",bit_h):
                return "钝薇"
            else:
                return default
        elif chara == "希":
            if weapon == "反叛者的刺杀弓":
                dXi={"战线支撑者的荆棘重甲":"重甲刺杀希","复苏战衣":"神木刺杀希"}
                return dXi.get(armor,default)
            elif weapon == "狂信者的荣誉之刃":
                return "沸飓希"
            elif weapon == "荆棘盾剑":
                dXi={"战线支撑者的荆棘重甲":"重甲摆烂希","复苏战衣":"神木摆烂希"}
                return dXi.get(armor,default)
            elif weapon == "幽梦匕首":
                return "飓风希"
            else:
                return default
        elif chara == "舞":
            dWU={"荆棘盾剑":"摆烂舞","幽梦匕首":"飓风舞","反叛者的刺杀弓":"沸舞"}
            return dWU.get(weapon,default)
        elif chara == "伊":
            dYI={"荆棘盾剑":"打野盾伊","幽梦匕首":"飓风伊","陨铁重剑":"打野神剑伊"}
            return dYI.get(weapon,default)
        elif chara == "梦":
            dMeng={"幽梦匕首":"匕首梦","狂信者的荣誉之刃":"刃梦","荆棘盾剑":"摆烂梦"}
            return dMeng.get(weapon,default)
        else:
            return "new card?"+default

if __name__=="__main__":
    from conf import DefaultConfig
    #配置
    cfg_c=DefaultConfig()
    cfg=cfg_c.cfg
    n_chara=cfg['n_chara']
    date_i=cfg["date_i"]
    mysql=cfg["mysql"]["config"]
    halo=cfg["halo"]

    col=cfg["col"]
    col_c=cfg["col_c"]

    jloader=JsonLoader(["data/f.json",],d_halo=halo,col=col,col_c=col_c)
    #loader=jloader.export_loader()
    from util import DBProcer
    #dbs=DBProcer("tmp.ts.db")
    #dbs.droper("table","rcd")
    #dbs.json2db("rcd",loader)

