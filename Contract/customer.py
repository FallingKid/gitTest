import pandas as pd

# 找到客户某个字段取值最多的值，如果空白最多则次之
def most_value(field_name) -> pd.Series:
    group = data.groupby('客户名称')[field_name]
    res = []
    for g in group:
        c = g[1].value_counts()
        if len(c) == 1:
            res.append(c.index[0])
        else:
            val = []
            most = c[1] if c.index[0] == ' ' else c[0]
            i = 1 if c.index[0] == ' ' else 0
            while i < len(c):
                if c[i] == most:
                    val.append(c.index[i])
                else:
                    break
                i += 1
            res.append('/'.join(val))
    res = pd.Series(res, index=data.groupby('客户名称').groups.keys(), name=field_name)
    return res
if __name__ == '__main__':
    # 导入数据集,删除客户名称为空的记录(本月中没有),用 ' ' 填充表中空白单元格
    data = pd.read_excel('data\\so_contract_01.xlsx', skiprows=[0])
    data = data.dropna(axis=0, subset=['客户名称'])
    data.fillna(" ", inplace=True)
    # 从客户交易记录中统计客户交易信息，构建客户标签
    customer_label = pd.DataFrame()
    customer_label['交易次数'] = data['客户名称'].value_counts()
    customer_label['合同总金额'] = data.groupby('客户名称')['合同总金额'].sum()
    customer_label['合同总重量'] = data.groupby('客户名称')['合同重量'].sum()
    customer_label['合同总数量'] = data.groupby('客户名称')['合同数量'].sum()
    customer_label['每笔交易平均金额'] = data.groupby('客户名称')['合同总金额'].sum() / data['客户名称'].value_counts()
    customer_label['每个合同平均金额'] = data.groupby('客户名称')['合同总金额'].sum() / data.groupby('客户名称')['合同数量'].sum()
    customer_label['常用付款方式'] = data.groupby('客户名称')['付款信息'].agg(lambda x: x.value_counts().index[0])
    customer_label['常用运输方式'] = most_value('运输方式')
    customer_label['城市'] = most_value('城市')
    customer_label['客户等级'] = most_value('客户等级')
    customer_label['行业类别(一)'] = most_value('行业类别（一）')
    customer_label['行业类别(二)'] = most_value('行业类别（二）')

    customer_label.to_excel('data\\customer_label.xlsx')
