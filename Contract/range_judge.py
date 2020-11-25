#提取1-9月合同数据，确定部分难以判断是否有取值范围的类别特征
import pandas as pd
import numpy as np
import os

Feature = ['库存组织', '生产公司', '销售部门', '港杂单价', '批量优惠', '订货方式', '付款信息', '品质', '表面结构', '产品形态']

if __name__ == '__main__':
    data_list = ["data\\销售数据1-9\\{}".format(x) for x in os.listdir('data\\销售数据1-9')]
    for data_name in data_list:
        data = pd.read_excel(data_name)
        for feat in Feature:
            value_list = [str(x) for x in data[feat].value_counts().index]
            with open("data\\特征取值范围判断\\{}.txt".format(feat), 'a')as f:
                f.write(', '.join(value_list))
                f.write('\n')