# -*- coding= utf-8 -*-
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV

# 类别特征
Categorical_feature = ['客户类型', '创建时间', '客户属性', '销售方式', '运输方式', '合同类型', '订货方式', '付款信息', '履约折扣',
                       '是否超量享受履约折扣', '结算方式', '后结算', '出库折扣', '回传时间', '合同状态', '确认时间', '运费担当', '是否多头']

if __name__ == '__main__':
    data = pd.read_excel('data\\交易作为记录.xlsx')
    # 客户等级字段为分类标签
    le = LabelEncoder()
    le.fit(data['客户等级'])
    target = np.array(le.transform(data['客户等级']))
    data.drop(columns=['客户等级'], inplace=True)
    data[Categorical_feature] = data[Categorical_feature].astype('category')
    columns = data.columns.tolist()
    categorical_index = [columns.index(x) for x in Categorical_feature]

    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2)
    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test)

    parameters = {
        'max_depth': range(4, 8, 1),
        'num_leaves': range(20, 200, 5)
    }
    gbm = lgb.LGBMClassifier(
        objective = 'multiclass',  # 问题类型，'multiclass'=表示多分类任务，使用softmax函数作为目标函数
        boosting_type = 'gbdt', # 基学习器模型算法
        metric = 'multi_error',  # 指定了度量的指标,'multi_error'=表示多分类中的分类错误率
        Categorical_feature = categorical_index, # 指定category特征的列
        num_class = 3, # 多分类任务中的类别数量
        num_leaves = 120, # 一棵树上的叶子数
        learning_rate = 0.1, # 学习率
        feature_fraction = 0.8, # 在每次迭代中随机选择部分特征,用来加速训练/处理过拟合
        bagging_fraction = 1, # 类似于 feature_fraction,将在不进行重采样的情况下随机选择部分数据
        bagging_freq = 2 # bagging的频率,为启用 bagging,应设置为非零值, k表示每k次迭代执行bagging
    )
    # print('Training=')
    # gbm = lgb.train(params,
    #                 lgb_train,
    #                 num_boost_round=1000, # boosting 的迭代次数
    #                 valid_sets=[lgb_train, lgb_eval], # 训练期间要评估的数据列表
    #                 verbose_eval=100 # 输出日志详细情况，多少条数据输出一条记录
    #                 )
    gsearch = GridSearchCV(gbm, param_grid=parameters, scoring='multi_error', cv=3)
    gsearch.fit(X_train, y_train)
    print('参数的最佳取值:{0}'.format(gsearch.best_params_))
    print('最佳模型得分:{0}'.format(gsearch.best_score_))

