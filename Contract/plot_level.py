import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family']='sans-serif'
mpl.rcParams['font.sans-serif']=[u'SimHei']

count_field = ['客户类型', '客户属性', '销售方式', '运输方式', '合同类型', '自动生单类型', '订货方式', '付款信息', '表面结构', '产品形态', '结案原因',
               '履约折扣', '是否超量享受履约折扣', '结算方式', '出库折扣', '合同状态', '发货情况', '分段合同总金额', '分段合同重量', '分段合同数量']

def split_money(x):
    if pd.isna(x):
        return 'None'
    elif x < 100000:
        return '<10w'
    elif x >= 100000 and x < 500000:
        return '10w-50w'
    elif x >= 500000 and x < 1000000:
        return '50w-100w'
    else:
        return '> 100w'

def split_weight(x):
    if pd.isna(x):
        return 'None'
    elif x < 5000:
        return '<5k'
    elif x >= 5000 and x < 10000:
        return '5k-1w'
    elif x >= 10000 and x < 30000:
        return '1w-3w'
    else:
        return '>3w'

def split_number(x):
    if pd.isna(x):
        return 'None'
    elif x < 10:
        return '<10'
    elif x >= 10 and x < 100:
        return '10-100'
    elif x >= 100 and x < 500:
        return '100-500'
    else:
        return '>500'

if __name__ == '__main__':
    data = pd.read_excel('data\\so_contract_01.xlsx', skiprows=[0])
    data.replace(' ', np.NaN, inplace=True)
    data.dropna(subset=['客户等级'], inplace=True)
    data['客户类型'].fillna('非协议户', inplace=True)

    data['发货情况'] = data['未开发货通知单数量'].apply(lambda x: '发超了' if x < 0 else '没发超')
    data['分段合同总金额'] = data['合同总金额'].apply(split_money)
    data['分段合同重量'] = data['合同重量'].apply(split_weight)
    data['分段合同数量'] = data['合同数量'].apply(split_number)

    for field in count_field:
        fig = plt.figure(figsize=(13, 7))
        sns.countplot(x='客户等级', hue=field, data=data)
        # plt.show()
        plt.savefig("photos\\客户等级\\{}.jpg".format(field))
