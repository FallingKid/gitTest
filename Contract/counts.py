# 统计每个特征的取值情况
import pandas as pd
import numpy as np

if __name__ == '__main__':
    data = pd.read_excel('data\\so_contract_01.xlsx', skiprows=[0])
    # 删除客户等级为空的行
    data.replace(' ', np.NaN, inplace=True)
    data['客户类型'].fillna('非协议户', inplace=True)
    data.dropna(subset=['客户等级'], inplace=True)
    columns = data.columns.tolist()
    total_count = data['客户等级'].value_counts().sum()
    counts = []
    counts_nan = []
    ratio_lt_half = []
    for column in columns:
        count = data[column].value_counts().sum()
        counts.append(count)
        counts_nan.append(total_count - count)
        ratio = 1 - (count / total_count)
        ratio_lt_half.append('是' if ratio > 0.5 else '否')
    data_count = pd.DataFrame()
    data_count['特征'] = columns
    data_count['计数'] = counts
    data_count['空值计数'] = counts_nan
    data_count['空值占比大于1/2'] = ratio_lt_half
    data_count.set_index('特征', inplace=True)
    data_count.to_excel('data\\计数.xlsx')
