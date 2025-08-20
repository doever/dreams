import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import numpy as np

try:
     # 读取 Excel 文件
     file_path = 'C:/Users/15643/Desktop/数据/毕业论文数据/工作簿 1_填充缺失值.xlsx'  # 替换为实际文件路径
     df = pd.read_excel(file_path)

     # 处理缺失值
     df = df.dropna()

     # 提取自变量、协变量和因变量
     X = df.drop(columns=['抑郁_SELECT'])
     y = df['抑郁_SELECT']

     # 确保所有特征都是数值类型
     X = X.apply(pd.to_numeric, errors='coerce')
     X = X.dropna(axis=1)

     # 划分训练集和测试集
     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

     # 数据标准化
     scaler = StandardScaler()
     X_train = scaler.fit_transform(X_train)
     X_test = scaler.transform(X_test)

     # 构建逻辑回归模型
     model = LogisticRegression(max_iter=1000)
     model.fit(X_train, y_train)

     # 在测试集上进行预测
     y_pred = model.predict(X_test)

     # 评估模型性能
     accuracy = accuracy_score(y_test, y_pred)
     precision = precision_score(y_test, y_pred)
     recall = recall_score(y_test, y_pred)
     f1 = f1_score(y_test, y_pred)
     conf_matrix = confusion_matrix(y_test, y_pred)

     # 输出模型评估指标
     print(f'准确率：{accuracy}')
     print(f'精确率：{precision}')
     print(f'召回率：{recall}')
     print(f'F1得分：{f1}')
     print(f'混淆矩阵：\n{conf_matrix}')

except FileNotFoundError:
     print(f"错误：未找到文件 {file_path}")
except Exception as e:
     print(f"发生未知错误：{e}")