# model_trainer.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import xgboost as xgb

class ModelTrainer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.label_encoder = LabelEncoder()
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = xgb.XGBClassifier(n_estimators=100, random_state=42)

    def preprocess_data(self):
        # Chọn các cột cần thiết cho bài toán
        text_columns = ['QUATRINHBENHLY', 'KHAMBENHTOANTHAN', 'KHAMBENHCACBOPHAN', 'LYDODIEUTRI']
        self.data['van_ban_ket_hop'] = self.data[text_columns].fillna('').agg(' '.join, axis=1)

        # Loại bỏ các dòng có chuỗi rỗng hoặc chỉ chứa khoảng trắng
        self.data['van_ban_ket_hop'] = self.data['van_ban_ket_hop'].replace(r'^\s*$', None, regex=True)
        self.data = self.data.dropna(subset=['van_ban_ket_hop', 'TENKHOAPHONG'])

        # Biến mục tiêu: TENKHOAPHONG
        X = self.data['van_ban_ket_hop']
        y = self.data['TENKHOAPHONG']

        # Chuyển đổi nhãn chuỗi (tên khoa phòng) thành các nhãn số
        self.y_encoded = self.label_encoder.fit_transform(y)

        # Chia tập dữ liệu thành tập huấn luyện và tập kiểm tra
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, self.y_encoded, test_size=0.2, random_state=42)

        # Chuyển đổi dữ liệu văn bản sang đặc trưng TF-IDF
        self.X_train_tfidf = self.vectorizer.fit_transform(self.X_train)
        self.X_test_tfidf = self.vectorizer.transform(self.X_test)

    def train_model(self):
        # Huấn luyện mô hình phân loại với XGBoost
        self.classifier.fit(self.X_train_tfidf, self.y_train)

        # Dự đoán
        y_pred = self.classifier.predict(self.X_test_tfidf)

        # Đánh giá mô hình
        print("Độ chính xác:", accuracy_score(self.y_test, y_pred))

        # In báo cáo phân loại
        unique_classes = self.label_encoder.classes_[np.unique(self.y_test)]
        print(classification_report(self.y_test, y_pred, target_names=unique_classes, zero_division=0))

    def predict(self, van_ban_moi):
        van_ban_moi_tfidf = self.vectorizer.transform([van_ban_moi])
        du_doan = self.classifier.predict(van_ban_moi_tfidf)
        khoa_phong_du_doan = self.label_encoder.inverse_transform(du_doan)
        return khoa_phong_du_doan[0]
