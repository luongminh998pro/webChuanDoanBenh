# app.py

from flask import Flask, request, render_template
from train_model import ModelTrainer

app = Flask(__name__)

# Khởi tạo ModelTrainer
trainer = ModelTrainer("data/Du lieu KhamBenhT042024.csv")
trainer.preprocess_data()
trainer.train_model()

@app.route('/', methods=['GET', 'POST'])
def predict_khoa_phong():
    if request.method == 'POST':
        quatrinh_benhly = request.form['quatrinh_benhly']
        kham_benh_toanthan = request.form['kham_benh_toanthan']
        kham_benh_cac_bophan = request.form['kham_benh_cac_bophan']
        ly_do_dieu_tri = request.form['ly_do_dieu_tri']
        van_ban_moi = ' '.join([quatrinh_benhly, kham_benh_toanthan, kham_benh_cac_bophan, ly_do_dieu_tri])
        khoa_phong_du_doan = trainer.predict(van_ban_moi)
        return render_template('index.html', prediction=khoa_phong_du_doan)
    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run()
