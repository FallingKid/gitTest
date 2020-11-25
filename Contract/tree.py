from sklearn.tree import DecisionTreeClassifier#引入决策树算法包
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from IPython.display import Image
from sklearn import tree

test_feature = ['合同执行情况表', '合同总金额', '合同数量', '客户类型']

if __name__ == '__main__':
    data = pd.read_excel('data\\so_contract_01-副本.xlsx', skiprows=[0])
    # 删除客户等级为空的行
    data.replace(' ', np.NaN, inplace=True)
    data.dropna(subset=['客户等级'], inplace=True)
    data['客户类型'].fillna('非协议户', inplace=True)
    target = data['客户等级'].tolist()
    data = data[test_feature]

    le = LabelEncoder()
    le.fit(data['合同执行情况表'])
    data['合同执行情况表'] = le.transform(data['合同执行情况表'])
    le.fit(data['客户类型'])
    data['客户类型'] = le.transform(data['客户类型'])

    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2)
    clf = DecisionTreeClassifier(max_depth=4)
    clf.fit(X_train, y_train)

    with open('data\\tree.dot', 'w', encoding='utf-8')as f:
        dot_data = tree.export_graphviz(clf, out_file=f,
                                        feature_names=test_feature,
                                        class_names=['重要客户', '一般客户', '战略用户'],
                                        filled=True, rounded=True,
                                        special_characters=True)

    iris_y_predict = clf.predict(X_test)
    score = clf.score(X_test, y_test, sample_weight=None)
    print('iris_y_predict = ', iris_y_predict)
    print('iris_y_test = ', y_test)
    print('Accuracy:', score)



