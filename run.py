from util import json2csv
from conf import DefaultConfig

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