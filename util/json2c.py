import json
import csv

def json2csv(input,out,col=(),mode="w",encoding="utf-8"):
        with open(input,'r',encoding=encoding) as f:
            datas=json.load(f)
            if mode=="w":
                fcsv=[col]
            else:
                fcsv=[]
            for data in datas["data"]["data"][0]["rows"]:
                fcsv.append(tuple([data[c] for c in col]))
            with open(out,mode=mode,newline="",encoding=encoding) as f2:
                writer=csv.writer(f2)
                writer.writerows(fcsv)