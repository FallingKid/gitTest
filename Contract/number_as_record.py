# 将每次交易（由同一合同编号组成）作为一条记录，提取新的分类特征
import pandas as pd
import numpy as np

# 11-21.docx中筛选出的35个留存特征字段
Feature = ['客户类型', '创建时间', '客户属性', '销售方式', '运输方式', '合同类型','订货方式', '付款信息', '品质', '表面结构', '产品形态',
           '纵切母卷宽度', '合同单价', '合同数量', '履约折扣', '履约折扣占用量', '是否超量享受履约折扣', '履约折扣占用超量', '合同重量',
           '合同支数(支/件)', '合同总金额', '已开订单数量', '已开订单重量', '结算方式', '后结算', '取价天数', '网价运费', '出库折扣',
           '回传时间', '合同状态', '确认时间', '结案原因', '运费担当', '违约单价', '是否多头']
Feature_category = ['客户类型', '创建时间', '客户属性', '销售方式', '运输方式', '合同类型','订货方式', '付款信息', '表面结构',
                    '履约折扣', '是否超量享受履约折扣', '结算方式', '后结算', '出库折扣', '回传时间', '合同状态', '确认时间',
                    '结案原因', '运费担当', '是否多头']
Feature_sum = ['合同单价', '履约折扣占用量', '履约折扣占用超量', '合同重量', '合同支数(支/件)', '合同总金额',
               '已开订单数量', '已开订单重量']
Feature_avg = ['纵切母卷宽度', '合同数量', '取价天数', '网价运费', '违约单价']

def drop_category_feature(data):
    num_sample = len(data)
    for feat in Feature_category:
        num_feature_nan = len(data[pd.isna(data[feat])])
        if num_feature_nan > num_sample / 5:
            Feature_category.remove(feat)

def transform_date_field(data):
    data['创建时间'] = data['创建时间'].apply(
        lambda x: np.NaN if pd.isnull(x) else '白天' if int(x[:2]) >= 6 and int(x[:2]) < 18 else '晚上')
    data['回传时间'] = data['回传时间'].apply(
        lambda x: np.NaN if pd.isnull(x) else '白天' if int(x[:2]) >= 6 and int(x[:2]) < 18 else '晚上')
    data['确认时间'] = data['确认时间'].apply(
        lambda x: np.NaN if pd.isnull(x) else '白天' if int(x[:2]) >= 6 and int(x[:2]) < 18 else '晚上')

def most_value(group, field_name) -> pd.Series:
    group_field = group[field_name]
    res = []
    for g in group_field:
        c = g[1].value_counts()
        if len(c) == 0:
            res.append(np.NaN)
        else:
            res.append(c.index[0])
    res = pd.Series(res, index=group.groups.keys(), name=field_name)
    return res

def sum_value(group, field_name) -> pd.Series:
    group_field = group[field_name]
    res = []
    for g in group_field:
        res.append(np.sum(g[1]))
    res = pd.Series(res, index=group.groups.keys(), name=field_name)
    return res

def avg_value(group, field_name) -> pd.Series:
    group_field = group[field_name]
    res = []
    for g in group_field:
        res.append(np.average(g[1]))
    res = pd.Series(res, index=group.groups.keys(), name=field_name)
    return res

if __name__ == '__main__':
    data = pd.read_excel('data\\so_contract_01-副本.xlsx', skiprows=[0])
    data.replace(' ', np.NaN, inplace=True)
    # 删除客户等级为空的记录
    data.dropna(subset=['客户等级'], inplace=True)
    # 将客户类型缺失值填充为非协议户
    data['客户类型'].fillna('非协议户', inplace=True)
    # 去除类别缺失值超过样本1/5的特征
    drop_category_feature(data)
    # 将时间特征字段转换为取值为早上、晚上
    transform_date_field(data)

    group = data.groupby('合同编号')
    new_data = pd.DataFrame()
    new_data['客户等级'] = most_value(group, '客户等级')
    for feat in Feature_category:
        new_data[feat] = most_value(group, feat)
    for feat in Feature_sum:
        new_data[feat] = sum_value(group, feat)
    for feat in Feature_avg:
        new_data[feat] = avg_value(group, feat)
    new_data.set_index('客户等级', inplace=True)
    new_data.to_excel('data\\交易作为记录.xlsx')



