import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from flask import Flask, request, render_template
import xgboost as xgb

# Tạo ứng dụng Flask
app = Flask(__name__)

# Huấn luyện mô hình và lưu các thành phần vào bộ nhớ
def load_model():
    data = pd.read_csv("Du lieu KhamBenhT042024.csv")
    text_columns = ['QUATRINHBENHLY', 'KHAMBENHTOANTHAN', 'KHAMBENHCACBOPHAN', 'LYDODIEUTRI']
    data['van_ban_ket_hop'] = data[text_columns].fillna('').agg(' '.join, axis=1)
    data['van_ban_ket_hop'] = data['van_ban_ket_hop'].replace(r'^\s*$', None, regex=True)
    data = data.dropna(subset=['van_ban_ket_hop', 'TENKHOAPHONG'])

    X = data['van_ban_ket_hop']
    y = data['TENKHOAPHONG']
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, _, y_train, _ = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)

    classifier = xgb.XGBClassifier(n_estimators=100, random_state=42)
    classifier.fit(X_train_tfidf, y_train)

    return classifier, tfidf_vectorizer, label_encoder

# Tải mô hình vào bộ nhớ khi khởi động ứng dụng
classifier, tfidf_vectorizer, label_encoder = load_model()

# Hàm để xử lý dự đoán
def du_doan_khoa_phong(quatrinh_benhly, kham_benh_toanthan, kham_benh_cac_bophan, ly_do_dieu_tri):
    van_ban_moi = ' '.join([quatrinh_benhly, kham_benh_toanthan, kham_benh_cac_bophan, ly_do_dieu_tri])
    van_ban_moi_tfidf = tfidf_vectorizer.transform([van_ban_moi])
    du_doan = classifier.predict(van_ban_moi_tfidf)
    khoa_phong_du_doan = label_encoder.inverse_transform(du_doan)
    return khoa_phong_du_doan[0]

# Route chính để hiển thị trang web
@app.route('/', methods=['GET', 'POST'])
def predict_khoa_phong():
    if request.method == 'POST':
        quatrinh_benhly = request.form['quatrinh_benhly']
        kham_benh_toanthan = request.form['kham_benh_toanthan']
        kham_benh_cac_bophan = request.form['kham_benh_cac_bophan']
        ly_do_dieu_tri = request.form['ly_do_dieu_tri']
        khoa_phong_du_doan = du_doan_khoa_phong(quatrinh_benhly, kham_benh_toanthan, kham_benh_cac_bophan, ly_do_dieu_tri)
        return render_template('index.html', prediction=khoa_phong_du_doan)
    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run()
