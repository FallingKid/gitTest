import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family']='sans-serif'
mpl.rcParams['font.sans-serif']=[u'SimHei']

def drawPie(data, field_name):
    data[field_name].fillna('(空白)', inplace=True)
    field = data[field_name].value_counts()
    plt.pie(field, autopct='%1.1f%%')
    plt.legend(data[field_name].value_counts().index)
    plt.title('%s占比' %field_name)
    plt.show()


if __name__ == '__main__':
    # 导入数据集,删除客户名称为空的记录(本月中没有)
    data_contract = pd.read_excel('data\\so_contract_01.xlsx', skiprows=[0], index_col=0, parse_dates=['创建日期'])
    data_contract.dropna(axis=0, subset=['客户名称'], inplace=True)
    data_customer = pd.read_excel('data\\customer_label.xlsx', index_col=0)

    # 各字段占比情况
    fields_name = ['客户类型', '客户属性', '销售方式', '客户等级', '运输方式', '自动生单类型', '付款信息', '表面结构', '履约折扣', '结算方式']
    for field_name in fields_name:
        drawPie(data_contract, field_name=field_name)

    # 客户合同总重量和合同总金额的散点图
    plt.scatter(data_customer['合同总重量'], data_customer['合同总金额'])
    plt.xlabel('合同总重量')
    plt.ylabel('合同总金额')
    plt.show()

