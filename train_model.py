import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import xgboost as xgb

def train_model():
    # Tải dữ liệu của bạn
    data = pd.read_csv("Du lieu KhamBenhT042024.csv")

    # Chọn các cột cần thiết cho bài toán
    text_columns = ['QUATRINHBENHLY', 'KHAMBENHTOANTHAN', 'KHAMBENHCACBOPHAN', 'LYDODIEUTRI']
    data['van_ban_ket_hop'] = data[text_columns].fillna('').agg(' '.join, axis=1)

    # Loại bỏ các dòng có chuỗi rỗng hoặc chỉ chứa khoảng trắng
    data['van_ban_ket_hop'] = data['van_ban_ket_hop'].replace(r'^\s*$', None, regex=True)
    data = data.dropna(subset=['van_ban_ket_hop', 'TENKHOAPHONG'])

    # Biến mục tiêu: TENKHOAPHONG
    X = data['van_ban_ket_hop']
    y = data['TENKHOAPHONG']

    # Chuyển đổi nhãn chuỗi (tên khoa phòng) thành các nhãn số
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Chia tập dữ liệu thành tập huấn luyện và tập kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Chuyển đổi dữ liệu văn bản sang đặc trưng TF-IDF
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    
    # Huấn luyện mô hình phân loại với XGBoost
    classifier = xgb.XGBClassifier(n_estimators=100, random_state=42)
    classifier.fit(X_train_tfidf, y_train)

    # Dự đoán và đánh giá mô hình
    y_pred = classifier.predict(tfidf_vectorizer.transform(X_test))
    print("Độ chính xác:", accuracy_score(y_test, y_pred))
    unique_classes = label_encoder.classes_[np.unique(y_test)]
    print(classification_report(y_test, y_pred, target_names=unique_classes, labels=np.unique(y_test), zero_division=0))

    # Trả về mô hình và các thành phần cần thiết
    return classifier, tfidf_vectorizer, label_encoder

if __name__ == "__main__":
    train_model()
