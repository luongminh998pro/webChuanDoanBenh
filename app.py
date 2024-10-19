from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load mô hình đã huấn luyện và vectorizer từ file .pkl
with open('model/model.pkl', 'rb') as model_file:
    classifier = pickle.load(model_file)

with open('model/tfidf_vectorizer.pkl', 'rb') as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)

with open('model/label_encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)


# Hàm để xử lý dự đoán
def du_doan_khoa_phong(quatrinh_benhly, kham_benh_toanthan, kham_benh_cac_bophan, ly_do_dieu_tri):
    # Kết hợp văn bản từ các trường được nhập vào
    van_ban_moi = ' '.join([quatrinh_benhly, kham_benh_toanthan, kham_benh_cac_bophan, ly_do_dieu_tri])

    # Chuyển đổi văn bản mới sang đặc trưng TF-IDF
    van_ban_moi_tfidf = tfidf_vectorizer.transform([van_ban_moi])

    # Sử dụng mô hình đã huấn luyện để dự đoán
    du_doan = classifier.predict(van_ban_moi_tfidf)

    # Giải mã nhãn dự đoán từ số về tên khoa phòng
    khoa_phong_du_doan = label_encoder.inverse_transform(du_doan)

    # Trả về kết quả dự đoán
    return khoa_phong_du_doan[0]

# Route chính để hiển thị trang web
@app.route('/', methods=['GET', 'POST'])
def predict_khoa_phong():
    if request.method == 'POST':
        # Lấy dữ liệu từ form nhập liệu
        quatrinh_benhly = request.form['quatrinh_benhly']
        kham_benh_toanthan = request.form['kham_benh_toanthan']
        kham_benh_cac_bophan = request.form['kham_benh_cac_bophan']
        ly_do_dieu_tri = request.form['ly_do_dieu_tri']

        # Gọi hàm dự đoán
        khoa_phong_du_doan = du_doan_khoa_phong(quatrinh_benhly, kham_benh_toanthan, kham_benh_cac_bophan, ly_do_dieu_tri)

        # Render lại trang với kết quả dự đoán
        return render_template('index.html', prediction=khoa_phong_du_doan)

    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run()
