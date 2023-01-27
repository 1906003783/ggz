import pandas as pd
import numpy as np
import datetime
from util import JsonLoader,DBProcer
from conf import DefaultConfig

#配置
cfg_c=DefaultConfig()
cfg=cfg_c.cfg
n_chara=cfg['n_chara']
date_i=cfg["date_i"]
mysql=cfg["mysql"]["config"]
dbname=mysql.get('database')
halo=cfg["halo"]

col=tuple(cfg["col"])
col_c=tuple(cfg["col_c"])

jloader=JsonLoader(["data/m.json","data/i1.json","data/i2.json"],d_halo=halo,col=col,col_c=col_c)
loader=jloader.export_loader()
jloader.json2csv("data/rlt.csv")

#连接数据库    
dbs=DBProcer("{}".format(dbname))
dbs.json2db("records",loader)

df=pd.read_csv("data/SSS.csv",encoding="utf-8")
#pd.set_option('display.max_columns',None)
name=[c for c in df.columns]
date_t=datetime.date(date_i[0],date_i[1],date_i[2])

sql="SELECT * FROM cnt;"
rlt= dbs.select(sql_string=sql)


if rlt is not None:
    weight=dict()
    for r in rlt:
        weight[r[0]]=r[1]


weight=[float(weight[(name[2*i*(n_chara+1)].strip("\t"))[0]])/sum(weight.values()) for i in range(n_chara)]
weight=np.array(weight)

dp=len(df.index)
avg_i=dict()
avg_w=dict()
for k in range(dp):
    c_date=date_t+datetime.timedelta(k)
    c_date="{0}-{1}".format(c_date.month,c_date.day)
    avg_i[c_date]=dict()
    avg_w[c_date]=dict()
    for i in range(n_chara*2):
        di=[]
        for j in range(n_chara*i+1+i,n_chara*(i+1)+1+i):
            di.append(float(df[name[j]][k].strip('%'))/100)
        arr=np.array(di)
        avg_i[c_date][name[i*(n_chara+1)]]=np.mean(arr)
        rlt=arr*weight
        #df[name[i*(n_chara+1)]][k]=round(rlt.sum(),3)
        avg_w[c_date][name[i*(n_chara+1)]]=round(rlt.sum(),3)
#df.to_csv("out.csv",columns=[name[i*(n_chara+1)] for i in range(n_chara*2) ],encoding="gbk")
avg_w=pd.DataFrame(avg_w)
avg_w.sort_values(by=c_date,ascending=False,inplace=True)
avg_w.to_csv("data/out_w.csv",encoding="gbk")
avg_i=pd.DataFrame(avg_i)
avg_i.sort_values(by=c_date,ascending=False,inplace=True)
avg_i.to_csv("data/out_i.csv",encoding="gbk")