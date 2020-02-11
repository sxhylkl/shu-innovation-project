# %%
from pyecharts import options as opts
from pyecharts.charts import Map
import pandas as pd
import numpy as np
import os


def MapShow(datapath,renderName="FangMapShow"):#传入数据文件夹路径,扫描文件夹下所有记录,统计条目数,地图显示分布,默认输出在当前路径下的renderName.html文件
    ErPosToVal={}#二手房记录 地点:条目数
    XinPosToVal={}#新房记录 地点:条目数
    ZuPosToVal={}#租房记录 地点:条目数
    TotalDic={"二手房":ErPosToVal,"新房":XinPosToVal,"租房":ZuPosToVal}
    
    oridata=os.walk(datapath)
    #对所有数据进行遍历,统计条目数,用于地图显示
    for path,dir_list,file_list in oridata:#遍历路径下所有文件,搜集条目数  
        for file_name in file_list:
            oneDataPath=os.path.join(path, file_name)#单个文件路径
            Position,Type=file_name.split(' ')#从 上海 二手房.csv 中 分割出 上海 二手房.csv
            Type,extName=Type.split('.')#从 二手房.csv 中 分割出 二手房 .csv

            oneData=pd.read_csv(oneDataPath)
            PosToVal=TotalDic[Type]
            PosToVal[Position]=PosToVal.get(Position,0)+oneData.shape[0]#字典更新
    
    MapChart= (
        Map()
        .add("二手房", [list(z) for z in zip(ErPosToVal.keys(),ErPosToVal.values())], "china")
        .add("新房", [list(z) for z in zip(XinPosToVal.keys(),XinPosToVal.values())], "china")
        .add("租房", [list(z) for z in zip(ZuPosToVal.keys(),ZuPosToVal.values())], "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-基本示例"),
            visualmap_opts=opts.VisualMapOpts(max_=max(PosToVal.values())),
            )
    )

    MapChart.render(renderName+".html")

#%%示例程序
#MapShow("C:\\MyWorkSpace\\shu-innovation-project\\data")