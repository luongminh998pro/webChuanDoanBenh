import pandas as pd
import numpy as np  # Thêm import NumPy
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import xgboost as xgb
import pickle

# Tải dữ liệu của bạn
data = pd.read_csv("data/Du lieu KhamBenhT042024.csv")


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
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Huấn luyện mô hình phân loại với XGBoost
classifier = xgb.XGBClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train_tfidf, y_train)

# Dự đoán
y_pred = classifier.predict(X_test_tfidf)

# Giải mã nhãn dự đoán từ số về tên khoa phòng
y_pred_labels = label_encoder.inverse_transform(y_pred)

# Đánh giá mô hình
print("Độ chính xác:", accuracy_score(y_test, y_pred))

# Chỉ định các lớp hiện có trong y_test
unique_classes = label_encoder.classes_[np.unique(y_test)]

# In báo cáo phân loại
print(classification_report(y_test, y_pred, target_names=unique_classes, labels=np.unique(y_test), zero_division=0))

# Kiểm tra sự phân bố của nhãn
print("Số lượng nhãn trong y_train:", np.unique(y_train, return_counts=True))
print("Số lượng nhãn trong y_test:", np.unique(y_test, return_counts=True))

# In ra các dự đoán dưới dạng tên khoa phòng
print("Dự đoán tên khoa phòng:", y_pred_labels)

# Lưu model
with open('model/model.pkl', 'wb') as model_file:
    pickle.dump(classifier, model_file)

# Lưu TF-IDF vectorizer
with open('model/tfidf_vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(tfidf_vectorizer, vectorizer_file)

# Lưu label encoder để giải mã nhãn số thành nhãn chuỗi
with open('model/label_encoder.pkl', 'wb') as le_file:
    pickle.dump(label_encoder, le_file)
