import yaml
import os

class SetConfig():
    def __init__(self,path,encoding="utf-8"):
        with open(path,"r",encoding=encoding) as f:
            self.cfg=yaml.safe_load(f)
            
    def loaddata(self,fname) :
        try:
            cfg_f=self.cfg["path_data"]
            path_w=cfg_f["path_data"]
            return os.path.join(path_w,cfg_f[fname])
        except ValueError as e:
            print(e)
            return
        
class DefaultConfig():
    def __init__(self,path="conf/config.yaml",encoding="utf-8"):
        with open(path,"r",encoding=encoding) as f:
            self.cfg=yaml.safe_load(f)
    def loaddata(self,fname) :
        try:
            cfg_f=self.cfg["path_data"]
            path_w=cfg_f["path_data"]
            return os.path.join(path_w,cfg_f[fname])
        except ValueError as e:
            print(e)
            return

if (__name__=="main"):
    path="config.yaml"
    cfg=DefaultConfig(path=path)
    print(cfg.loaddata("json_i"))

