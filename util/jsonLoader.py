import json
import csv
import re
from bs4 import BeautifulSoup

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
    """
    def createdb(self):
        db=sqlite3.connect(database=mysql["database"]+".db")
        cursor=db.cursor()
        table_name="records"
        sql_string = f"""CREATE TABLE {table_name} ({",".join(self.loader[0][0])});"""
        cursor.execute(sql_string)
        db.commit()
        db.close()

    def json2db(self):
        db=sqlite3.connect(database=mysql["database"]+".db")
        cursor=db.cursor()
        for ld in self.loader:
            table_name="records"
            cols=self.loader[0][0]
            format_v=','.join(['?'] * len(cols))
            sql_string = f"""INSERT INTO {table_name} ({",".join(cols)}) VALUES ({format_v});""" 
            cursor.executemany(sql_string, self.loader[0][1:])
        db.commit()
        db.close()
    """
        
    def json_proc(self,input:str,d_halo:dict,col=[],col_c=[],mode="w",encoding="utf-8") ->list:
        self.mode=mode
        self.encoding=encoding
        with open(input,'r',encoding=encoding) as f:
            datas=json.load(f)
            if mode=="w":
                loader=[tuple(col+col_c)]
            else:
                loader=[]
            for data in datas["data"]["data"][0]["rows"]:
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
                        bit_h+=(2**d_halo[h])
                    charinfo=[data[c] for c in col]
                    stat=eq+w_match+[str(s_halo)]+[bit_h]
                    stat2=charinfo+stat
                    col2=col+col_c
                    sdict={col2[i]:i for i in range(len(col2))}
                    loader.append(tuple(stat2+[self.typecheck(stat=stat2,sdict=sdict,halo=d_halo)]))
            return loader
        
    def typecheck(self,stat:list,sdict:list,halo:dict):
        default="UNKHNOWN"
        bit_h=stat[sdict.get('bit_h')]
        if stat[sdict.get('char')] == "冥":
            if stat[sdict.get('weapon')] == "反叛者的刺杀弓":
                return "刺杀冥"
            elif stat[sdict.get('weapon')] == "狂信者的荣誉之刃":
                return "刃冥"
            elif stat[sdict.get('weapon')] == "荆棘盾剑":
                return "剑盾冥"
            else:
                return default
        elif stat[sdict.get('char')] == "艾":
            if int(stat[sdict.get('spd')])<3000:
                return "低速艾"
            elif int(stat[sdict.get('spd')])>8000:
                return "高速艾"
            elif int(stat[sdict.get('pdef')])>4500:
                return "中速艾"
            else:
                return "中速艾_低物防"
        elif stat[sdict.get('char')] == "默":
            if stat[sdict.get('weapon')] == "光辉法杖":
                return "神光默"
            elif int(stat[sdict.get('matk')])>20000:
                return "短杖默-高穿"
            else:
                return "短杖默-中穿"
        elif stat[sdict.get('char')] == "命":
            if stat[sdict.get('weapon')] == "反叛者的刺杀弓":
                return "刺杀命"
            else:
                return "神枪命"
        elif stat[sdict.get('char')] == "琳":
            if stat[sdict.get('weapon')] == "反叛者的刺杀弓":
                return "刺杀琳"
            elif stat[sdict.get('weapon')] == "狂信者的荣誉之刃":
                return "沸飓琳"
            elif stat[sdict.get('weapon')] == "幽梦匕首":
                return "飓风琳"
            elif stat[sdict.get('weapon')] == "荆棘盾剑":
                if bit_h&2<<(halo["点到为止"]-2) and bit_h&2<<(halo["铁甲尖刺"]-2):
                    if int(stat[sdict.get('pdef')])>4000:
                        return "高防摆烂琳"
                    else:
                        return "低配摆烂琳"
                else:
                    return "反伤琳"
            else:
                return default
        elif stat[sdict.get('char')] == "薇":
            if int(stat[sdict.get('mp')])>200000:
                return "护盾薇"
            else:
                if( bit_h&2<<(halo["荧光护盾"]-2)):
                    return "荧飓薇"
                elif( bit_h&2<<(halo["钝化锋芒"]-2)):
                    return "钝薇"
                else:
                    return default
        elif stat[sdict.get('char')] == "希":
            if stat[sdict.get('weapon')] == "反叛者的刺杀弓":
                if stat[sdict.get('armor')] == "战线支撑者的荆棘重甲":
                    return "重甲刺杀希"
                if stat[sdict.get('armor')] == "复苏战衣":
                    return "神木刺杀希"
                else:
                    return "???"
            elif stat[sdict.get('weapon')] == "狂信者的荣誉之刃":
                return "沸飓希"
            elif stat[sdict.get('weapon')] == "荆棘盾剑":
                if stat[sdict.get('armor')] == "战线支撑者的荆棘重甲":
                    return "重甲摆烂希"
                if stat[sdict.get('armor')] == "战线支撑者的荆棘重甲":
                    return "神木摆烂希"
            elif stat[sdict.get('weapon')] == "幽梦匕首":
                return "飓风希"
            else:
                return default
        elif stat[sdict.get('char')] == "舞":
            if stat[sdict.get('weapon')] == "荆棘盾剑":
                return "摆烂舞"
            else:
                return "UNKNOWN"
        elif stat[sdict.get('char')] == "伊":
            if stat[sdict.get('weapon')] == "幽梦匕首":
                return "飓风伊"
            else:
                return "UNKNOWN"
        elif stat[sdict.get('char')] == "梦":
            if stat[sdict.get('weapon')] == "狂信者的荣誉之刃":
                return "刃梦"
            if stat[sdict.get('weapon')] == "幽梦匕首":
                return "匕首梦"
            else:
                return "UNKNOWN"

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

