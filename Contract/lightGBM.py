# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 类别特征
categorical_feature = ['合同执行情况表', '客户类型', '创建时间', '客户属性', '销售方式', '库存组织', '生产公司', '合同编号', '合同项次', '关联合同号', '运输方式', '销售部门', '销售人员', '销售人员联系方式', '合同类型', '自动生单类型', '订货方式', '付款信息', '品质', '表面结构', '产品形态', '产品规范编号', '用途码', '用途码描述', '牌号', '产品规格', '履约折扣', '是否超量享受履约折扣', '价格版次', '城市', '定价区域', '收货地址', '合同备注', '包装方式', '单重范围', '交货公差', '结算方式', '后结算', '取价天数', '出库折扣', '客户期望交期', '订单交期', '回传日期', '回传时间', '回传人员', '合同状态', '合同确认日期', '确认时间', '确认人员', '结案时间', '结案原因', '流向确认日期', '海运流向确认日期', '行业类别（一）', '行业类别（二）', '特准价格 文号', '运费担当', '审批报告编号项次', '是否多头', '意向单号']


if __name__ == '__main__':
    data = pd.read_excel('data\\so_contract_01-副本.xlsx', skiprows=[0])
    # 删除客户等级为空的行
    data.replace(' ', np.NaN, inplace=True)
    data.dropna(subset=['客户等级'], inplace=True)
    data['客户类型'].fillna('非协议户', inplace=True)
    data['创建时间'] = data['创建时间'].apply(lambda x: np.NaN if pd.isnull(x) else '白天' if int(x[:2]) >= 6 and int(x[:2]) < 18 else '晚上')
    data['回传时间'] = data['回传时间'].apply(lambda x: np.NaN if pd.isnull(x) else '白天' if int(x[:2]) >= 6 and int(x[:2]) < 18 else '晚上')
    data['确认时间'] = data['确认时间'].apply(lambda x: np.NaN if pd.isnull(x) else '白天' if int(x[:2]) >= 6 and int(x[:2]) < 18 else '晚上')
    # 客户等级字段为分类标签
    le = LabelEncoder()
    le.fit(data['客户等级'])
    target = np.array(le.transform(data['客户等级']))
    data.drop(columns=['客户等级', '客户名称', '收货人', '最终客户', '合同制作人'], inplace=True)
    data[categorical_feature] = data[categorical_feature].astype('category')
    columns = data.columns.tolist()
    categorical_index = [columns.index(x) for x in categorical_feature]

    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2)
    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test)
    params = {
        'objective': 'multiclass',  # 问题类型，'multiclass':表示多分类任务，使用softmax函数作为目标函数
        'boosting_type': 'gbdt', # 基学习器模型算法
        'categorical_feature': categorical_index, # 指定category特征的列
        'num_class': 3, # 多分类任务中的类别数量
        'metric': 'multi_error', # 指定了度量的指标,'multi_error':表示多分类中的分类错误率
        'num_leaves': 120, # 一棵树上的叶子数
        'min_data_in_leaf': 100, # 一个叶子上数据的最小数量. 可以用来处理过拟合.
        'learning_rate': 0.06, # 收缩率
        'feature_fraction': 0.8, # 在每次迭代中随机选择部分特征,用来加速训练/处理过拟合
        'bagging_fraction': 0.8, # 类似于 feature_fraction,将在不进行重采样的情况下随机选择部分数据
        'bagging_freq': 5, # bagging的频率,为启用 bagging,应设置为非零值, 5表示每5次迭代执行bagging
        'lambda_l1': 0.4, # L1 正则
        'lambda_l2': 0.5, # L2 正则
        'min_gain_to_split': 0.2, # 执行切分的最小增益
        'verbose': -1, # <0显示致命的,=0显示错误(警告),>0显示信息
    }
    print('Training:')
    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=1000, # boosting 的迭代次数
                    valid_sets=[lgb_train, lgb_eval], # 训练期间要评估的数据列表
                    verbose_eval=100 # 输出日志详细情况，多少条数据输出一条记录
                    )
    gbm.save_model('data\\model.txt')
    print('\nPredicting:')
    y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
    y_pred = [list(x).index(max(x)) for x in y_pred]
    print(y_pred)
    print("accuracy_score: {}".format(accuracy_score(y_test, y_pred)))

    # 放入训练的属性以及分类的特征值
    import_rate = gbm.feature_importance()
    print(list(import_rate))
    # 转化为百分比
    improt_ratio = np.array(import_rate) / sum(import_rate) * 100
    features = data.columns.tolist()
    data_import_ratio = pd.DataFrame()
    data_import_ratio['特征'] = features
    data_import_ratio['重要程度比率(%)'] = improt_ratio
    data_import_ratio.set_index('特征', inplace=True)
    data_import_ratio.to_excel('data\\特征重要程度2.xlsx')