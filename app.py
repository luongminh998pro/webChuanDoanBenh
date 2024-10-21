from flask import Flask, render_template, request

app = Flask(__name__)

# Danh sách khoa phòng
khoa_phong = {
    'Pk Da Liễu': ['da', 'da liễu', 'ngứa', 'bong da', 'mẩn ngứa'],
    'Pk Chấn Thương': ['chấn thương', 'xương', 'gãy', 'nẹp xương', 'cố định'],
    'Pk Tai Mũi Họng': ['tai', 'mũi', 'họng', 'nghe', 'thính lực'],
    'Pk Mắt': ['mắt', 'thị lực', 'thị giác'],
    'Pk Cấp Cứu': ['cấp cứu', 'khẩn cấp'],
    'Pk Răng Hàm Mặt': ['răng', 'hàm', 'mặt', 'nha khoa'],
    'PK Nhi tại khoa': ['nhi', 'trẻ em'],
    'Pk Nội I': ['nội', 'khám nội'],
    'Pk Ung bướu yêu cầu': ['ung thư', 'u bướu'],
    'Pk Nội Tiết-Đái Tháo Đường2': ['đái tháo đường', 'tiết nội'],
    'Pk Tăng Huyết Áp_2': ['tăng huyết áp', 'huyết áp cao'],
    'Pk Cơ Xương Khớp': ['cơ xương khớp', 'đau khớp'],
    'Pk Tăng Huyết Áp 3 - Tim Mạch': ['tim mạch', 'tăng huyết áp'],
    'Pk Y Học Cổ Truyền': ['y học cổ truyền'],
    'Pk Nội Tiết-đái Tháo Đường': ['đái tháo đường', 'tiết nội'],
    'Pk Quản lý Parkinson - Sa sút trí tuệ': ['parkinson', 'trí tuệ'],
    'Pk Truyền Nhiễm': ['truyền nhiễm'],
    'Pk Nội Thận - Tiết niệu và Lọc Máu': ['tiết niệu', 'lọc máu'],
    'PK Ngoại Thần Kinh': ['thần kinh'],
    'Pk Huyết Học Lâm Sàng': ['huyết học'],
    'PK Nội tiết - YHHN': ['nội tiết'],
    'Pk Phục Hồi Chức Năng': ['phục hồi', 'chức năng'],
    'Pk Ngoại Tim mạch - Lồng ngực': ['tim mạch', 'ngoại khoa'],
    'Pk Yêu cầu': ['yêu cầu'],
    'pk.Ngoại Tiết niệu': ['tiết niệu'],
    'Pk Y Học Hạt Nhân': ['hạt nhân'],
    'Pk ung bướu': ['ung bướu'],
    'Pk Tâm Thần': ['tâm thần'],
    'Pk Lão khoa - Bảo Vệ Sức Khoẻ': ['lão khoa'],
    'Pk Nhi': ['nhi'],
    'Pk Phụ Sản': ['phụ sản'],
    'Pk Thần Kinh': ['thần kinh'],
    'Pk Ngoại': ['ngoại khoa'],
    'Pk Sản': ['sản khoa'],
    'Pk phụ sản dịch vụ': ['phụ sản', 'dịch vụ'],
    'PK Sản Phụ Khoa Dịch Vụ Chất Lượng Cao': ['dịch vụ', 'phụ khoa'],
    'Pk Ngoại Nhi': ['ngoại nhi'],
    'Pk Trưởng Khoa': ['trưởng khoa'],
    'PK Nội Tiết Dịch Vụ': ['dịch vụ', 'nội tiết'],
    'Pk Yêu cầu CXK': ['yêu cầu'],
    'PK TT Tạo Hình Thẩm Mỹ': ['tạo hình', 'thẩm mỹ'],
    'PK Ưu tiên': ['ưu tiên'],
    'Pk Nội Tim Mạch tại khoa': ['tim mạch'],
    'Pk Phó khoa (P227)': ['phó khoa'],
    'Pk Tư Vấn Tiêm Chủng': ['tiêm chủng'],
    'Pk Nội Tiêu Hoá Dịch vụ': ['tiêu hóa', 'dịch vụ'],
    'Pk Phó Khoa': ['phó khoa'],
    'Pk Nội Tiết-Đái Tháo Đường3': ['đái tháo đường'],
    'Pk Khám và Tư Vấn Dinh Dưỡng': ['dinh dưỡng']
}

# Hàm so sánh để tìm khoa phòng phù hợp
def match_department(QUATRINHBENHLY, KHAMBENHTOANTHAN, KHAMBENHCACBOPHAN, LYDODIEUTRI):
    scores = {k: 0 for k in khoa_phong.keys()}

    # Tạo danh sách từ khóa cho từng trường nhập liệu
    input_data = [QUATRINHBENHLY, KHAMBENHTOANTHAN, KHAMBENHCACBOPHAN, LYDODIEUTRI]

    # Duyệt qua từng khoa phòng và tính điểm số
    for department, keywords in khoa_phong.items():
        for keyword in keywords:
            for entry in input_data:
                if keyword in entry.lower():
                    scores[department] += 1

    # Tìm khoa phòng có điểm cao nhất
    max_score = max(scores.values())
    best_departments = [dept for dept, score in scores.items() if score == max_score]

    # Trả về khoa phòng phù hợp
    return best_departments[0] if best_departments else 'Khoa phòng không xác định'

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = ""
    if request.method == 'POST':
        QUATRINHBENHLY = request.form['quatrinh_benhly']
        KHAMBENHTOANTHAN = request.form['kham_benh_toanthan']
        KHAMBENHCACBOPHAN = request.form['kham_benh_cac_bophan']
        LYDODIEUTRI = request.form['ly_do_dieu_tri']
        
        prediction = match_department(QUATRINHBENHLY, KHAMBENHTOANTHAN, KHAMBENHCACBOPHAN, LYDODIEUTRI)
    
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
