from flask import Flask, render_template, request
import csv
import re

app = Flask(__name__)

app = Flask(__name__)

# Danh sách khoa phòng
khoa_phong = {
  
    'Pk Chấn Thương': [
        'chấn thương', 'xương', 'gãy', 'nẹp xương', 'cố định', 'đau',
        'trật khớp', 'vết thương', 'tái tạo xương', 'phục hồi chức năng',
        'cải thiện vận động', 'các triệu chứng chấn thương', 'bong gân',
        'đau nhức', 'chấn thương thể thao', 'gãy xương hở', 'gãy xương kín',
        'đau lưng', 'đau cổ', 'đau vai', 'đau khớp', 'đau đầu gối', 'đau chân',
        'chấn thương ở trẻ em', 'chấn thương dây chằng', 'điều trị chấn thương',
        'phẫu thuật chấn thương', 'thăm khám chấn thương', 'các phương pháp điều trị',
        'giá trị chấn thương', 'tư vấn điều trị chấn thương', 'các bài tập phục hồi',
        'xét nghiệm chấn thương', 'chẩn đoán hình ảnh', 'sử dụng thuốc giảm đau',
        'các phương pháp chữa trị', 'khám sức khỏe thể chất', 'các dấu hiệu của chấn thương',
        'hỗ trợ chấn thương', 'sức khỏe sau chấn thương', 'điều trị đau mãn tính',
        'điều trị đau cấp tính', 'các dịch vụ điều trị', 'sử dụng thiết bị hỗ trợ',
        'chăm sóc sau phẫu thuật', 'các phương pháp vật lý trị liệu',
        'sức khỏe tinh thần sau chấn thương', 'các bài tập phục hồi chức năng',
        'chăm sóc sức khỏe thể chất', 'ngăn ngừa chấn thương', 'thể dục thể thao an toàn',
        'các phương pháp giảm đau', 'kỹ thuật phục hồi', 'khám chấn thương thể thao',
        'khám và điều trị', 'các vấn đề về xương khớp', 'bệnh lý xương khớp',
        'điều trị gãy xương', 'điều trị chấn thương thể thao', 'các loại chấn thương',
        'tình trạng chấn thương', 'tư vấn phục hồi', 'phương pháp vật lý trị liệu',
        'khám và điều trị chấn thương', 'các dịch vụ y tế liên quan đến chấn thương',
        'điều trị vết thương', 'các kỹ thuật phẫu thuật', 'phẫu thuật tái tạo',
        'chẩn đoán và điều trị', 'chăm sóc sức khỏe sau phẫu thuật', 'các bài tập vật lý',
        'chăm sóc sức khỏe sau chấn thương', 'hỗ trợ tinh thần', 'tư vấn tâm lý',
        'phục hồi sức khỏe', 'các phương pháp kiểm tra', 'điều trị bệnh lý xương',
        'các triệu chứng chấn thương thể thao', 'khám chấn thương nội khoa', 'các bệnh lý liên quan',
        'phương pháp điều trị đau', 'chăm sóc toàn diện', 'tư vấn sức khỏe', 'điều trị tê bì',
        'các dịch vụ tư vấn', 'chuyên gia về chấn thương', 'các công nghệ mới trong điều trị'
    ],

      'Pk Da Liễu': [
        'da', 'da liễu', 'ngứa', 'bong da', 'mẩn ngứa', 'viêm da', 'chàm',
        'khô da', 'mụn', 'vảy nến', 'trứng cá', 'bị dị ứng', 'viêm da tiếp xúc',
        'mụn cóc', 'nấm da', 'nổi mề đay', 'bệnh chàm', 'hắc lào', 'bệnh vẩy nến',
        'bệnh trứng cá', 'bệnh nấm', 'da nhờn', 'da khô', 'mụn đầu đen', 'mụn đầu trắng',
        'tăng sắc tố da', 'suy giáp', 'rối loạn nội tiết', 'bệnh da liễu ở trẻ em',
        'viêm da bã nhờn', 'dị ứng thuốc', 'bệnh lý sắc tố', 'các bệnh da mãn tính',
        'dễ bị tổn thương da', 'các vấn đề về da mặt', 'sạch da', 'trẻ hóa da',
        'lão hóa da', 'sạm da', 'nám da', 'da nhạy cảm', 'da không đều màu',
        'bệnh da vùng kín', 'điều trị thẩm mỹ da', 'chăm sóc da hàng ngày',
        'các sản phẩm dưỡng da', 'chế độ ăn uống cho da', 'thực phẩm tốt cho da',
        'bệnh da di truyền', 'bệnh da do ánh sáng', 'bệnh lý ngoài da', 'điều trị mụn',
        'phẫu thuật thẩm mỹ da', 'bệnh da do tiếp xúc hóa chất', 'thăm khám da',
        'tư vấn da liễu', 'các dấu hiệu bệnh da', 'bệnh da do virus', 'bệnh da do vi khuẩn',
        'bệnh da do nấm', 'khám da', 'trị liệu da', 'điều trị bệnh da', 'chăm sóc sắc đẹp',
        'tư vấn làm đẹp da', 'bệnh da tự miễn', 'các bệnh viêm da', 'bệnh lý về chân tóc',
        'các phương pháp điều trị da', 'sử dụng thuốc bôi da', 'các bệnh lý mô mềm',
        'viêm nang lông', 'bệnh lý da nhiễm trùng', 'tìm hiểu về da', 'kiến thức về da',
        'các triệu chứng bệnh da', 'bệnh da mãn tính', 'bệnh viêm da dị ứng', 'da nhiễm trùng',
        'bệnh vẩy nến toàn thân', 'bệnh chàm thể tạng', 'màng nhầy miệng', 'viêm nướu',
        'sử dụng sản phẩm tự nhiên cho da', 'các thành phần chăm sóc da', 'phân loại bệnh da',
        'hỗ trợ điều trị bệnh da', 'bệnh lý da ở người già', 'da nhạy cảm với thời tiết',
        'hói đầu', 'rụng tóc', 'gàu', 'bệnh da do côn trùng cắn', 'dị ứng thực phẩm',
        'các bệnh lý liên quan đến mụn', 'bệnh da do di truyền', 'khám tổng quát da'
    ],
    'Pk Tai Mũi Họng': [
        'tai', 'mũi', 'họng', 'nghe', 'thính lực', 'đau họng', 'khó thở', 'ù tai', 'viêm',
        'viêm xoang', 'dị ứng', 'bệnh tai', 'bệnh mũi', 'bệnh họng', 'đau tai', 'sổ mũi',
        'cảm lạnh', 'viêm amidan', 'viêm thanh quản', 'ngạt mũi', 'khó ngửi', 'nghe kém',
        'mũi chảy máu', 'tê môi', 'nói khàn', 'điếc', 'rối loạn thính giác', 'nhiễm trùng tai',
        'bệnh lý mũi', 'mũi khô', 'các triệu chứng viêm xoang', 'viêm tai giữa', 'mũi nấm',
        'điều trị mũi', 'khám tai', 'chẩn đoán viêm xoang', 'chẩn đoán tai mũi họng',
        'khám thính lực', 'khám chức năng hô hấp', 'các bệnh lý hô hấp', 'khó thở khi nằm',
        'khó thở khi hoạt động', 'khám sức khỏe tai mũi họng', 'thăm khám viêm họng',
        'các triệu chứng tai', 'chẩn đoán và điều trị', 'thuốc tai mũi họng',
        'bệnh lý tai mũi họng', 'khám tổng quát tai mũi họng', 'bệnh lý về thính lực',
        'các dịch vụ tai mũi họng', 'các phương pháp điều trị', 'tư vấn bệnh tai',
        'sử dụng thuốc trị viêm', 'các bài tập phục hồi', 'tư vấn chăm sóc sức khỏe',
        'các bệnh lý cấp cứu', 'sức khỏe tai', 'tư vấn tiêm phòng', 'phẫu thuật tai',
        'các triệu chứng về mũi', 'phẫu thuật mũi', 'bệnh lý về họng', 'chẩn đoán nhanh',
        'tư vấn chuyên khoa', 'khám tổng quát sức khỏe', 'dị ứng thuốc', 'các dấu hiệu bất thường',
        'chăm sóc sức khỏe tai', 'thăm khám sức khỏe', 'các triệu chứng khô họng',
        'các dấu hiệu viêm', 'chẩn đoán và điều trị viêm', 'khám và điều trị',
        'tư vấn về điều trị', 'điều trị bệnh lý', 'hỗ trợ chăm sóc sức khỏe',
        'tư vấn sức khỏe', 'các dịch vụ y tế', 'bệnh lý hô hấp ở trẻ em', 'khám tai cho trẻ',
        'khám và điều trị hô hấp', 'bệnh viêm mũi dị ứng', 'bệnh lý phổi', 'các vấn đề về thính lực'
    ],
    'Pk Mắt': [
        'mắt', 'thị lực', 'thị giác', 'mờ mắt', 'đau mắt', 'khô mắt', 'cận thị', 'viễn thị',
        'lão thị', 'bệnh lý mắt', 'đau nhức mắt', 'các triệu chứng mắt', 'khám mắt',
        'các bệnh về mắt', 'bệnh lý thị giác', 'điều trị mắt', 'tư vấn thị lực', 'mắt cận',
        'mắt viễn', 'điều trị khô mắt', 'các phương pháp kiểm tra', 'tư vấn chăm sóc mắt',
        'sử dụng kính', 'phẫu thuật mắt', 'mắt yếu', 'mắt nheo', 'mắt đỏ', 'các vấn đề về thị lực',
        'các triệu chứng thị lực', 'bệnh lý mắt ở trẻ em', 'khám mắt cho trẻ', 'tư vấn về kính',
        'các sản phẩm cho mắt', 'hỗ trợ thị lực', 'các dấu hiệu bất thường của mắt',
        'khám và điều trị mắt', 'chăm sóc mắt hàng ngày', 'các triệu chứng đau mắt',
        'bệnh lý do ánh sáng', 'bệnh khô mắt', 'các triệu chứng rối loạn thị giác',
        'bệnh lý mắt do tuổi', 'mắt đa sắc', 'mắt viễn thị', 'các phương pháp điều trị',
        'tư vấn chăm sóc thị lực', 'các bệnh lý mãn tính', 'tư vấn khúc xạ', 'bệnh lý giác mạc',
        'bệnh lý võng mạc', 'điều trị giác mạc', 'khám tổng quát mắt', 'các triệu chứng chói',
        'các bệnh về thủy tinh thể', 'khám mắt thường xuyên', 'điều trị bệnh lý mắt',
        'phẫu thuật giác mạc', 'sử dụng thuốc nhỏ mắt', 'các triệu chứng mỏi mắt',
        'chăm sóc mắt cho người già', 'tư vấn thuốc mắt', 'các dấu hiệu cảnh báo',
        'các dịch vụ mắt', 'mắt yếu', 'bệnh lý bẩm sinh về mắt', 'các triệu chứng mắt khô',
        'sức khỏe mắt', 'tư vấn khám mắt', 'phẫu thuật thẩm mỹ mắt', 'các dịch vụ thẩm mỹ mắt',
        'điều trị đau mắt', 'tư vấn về phẫu thuật mắt'
    ],
    'Pk Cấp Cứu': [
        'cấp cứu', 'khẩn cấp', 'nguy cấp', 'sốt', 'buồn nôn', 'đau bụng', 'ngất xỉu', 
        'chấn thương', 'đau ngực', 'hô hấp', 'các triệu chứng cấp cứu', 'điều trị cấp cứu', 
        'khám cấp cứu', 'bệnh lý cấp cứu', 'các bệnh lý cấp cứu', 'điều trị khẩn cấp', 
        'tình trạng cấp cứu', 'tư vấn cấp cứu', 'khám và điều trị', 'điều trị cấp cứu cho trẻ', 
        'các phương pháp cấp cứu', 'các dấu hiệu cảnh báo', 'các bệnh lý nội khoa cấp', 
        'phục hồi sau cấp cứu', 'bệnh lý tim mạch cấp', 'cấp cứu ngộ độc', 'cấp cứu bệnh lý nặng', 
        'khám sức khỏe khẩn cấp', 'các dấu hiệu khẩn cấp', 'phương pháp sơ cứu', 
        'các bước sơ cứu', 'bệnh lý nhiễm trùng cấp', 'cấp cứu hô hấp', 'bệnh lý nội khoa',
        'tình trạng nguy cấp', 'sử dụng thuốc cấp cứu', 'khám và điều trị cấp cứu', 
        'bệnh lý cấp tính', 'khám tổng quát cấp cứu', 'điều trị khẩn cấp cho bệnh nhân', 
        'điều trị ngộ độc', 'các triệu chứng cần cấp cứu', 'tư vấn sức khỏe cấp cứu', 
        'các bệnh lý cấp cứu thường gặp', 'bệnh lý ngoại khoa cấp cứu', 'các dịch vụ cấp cứu',
        'chăm sóc sức khỏe cấp cứu', 'bệnh lý tim mạch khẩn cấp', 'các bước cần làm trong cấp cứu', 
        'các phương pháp xử lý cấp cứu', 'tình huống cấp cứu thường gặp', 'các dịch vụ cấp cứu 24/7',
        'tình trạng ngất xỉu', 'tình trạng đau ngực', 'điều trị cấp cứu cho người già', 
        'bệnh lý cấp cứu ở trẻ em', 'các dấu hiệu cần cấp cứu khẩn cấp', 'tư vấn khám cấp cứu',
        'các triệu chứng cấp cứu cần lưu ý', 'chăm sóc sức khỏe sau cấp cứu', 
        'các vấn đề cấp cứu phổ biến', 'các dịch vụ y tế khẩn cấp', 'tình trạng cần cấp cứu',
        'các triệu chứng nguy cấp'
    ],
    'Pk Răng Hàm Mặt': [
        'răng', 'hàm', 'mặt', 'nha khoa', 'viêm', 'sâu răng', 'viêm nướu', 
        'trám răng', 'niềng răng', 'khớp cắn', 'các vấn đề về răng', 'chăm sóc răng miệng', 
        'khám răng miệng', 'điều trị răng', 'các triệu chứng nha khoa', 'các bệnh lý răng miệng', 
        'chăm sóc răng cho trẻ', 'tẩy trắng răng', 'bệnh lý răng', 'các bệnh lý về nướu', 
        'hôi miệng', 'các vấn đề về hàm', 'điều trị viêm nướu', 'các triệu chứng đau răng', 
        'niềng răng cho trẻ em', 'điều trị bệnh răng miệng', 'tư vấn chăm sóc răng', 
        'các dấu hiệu cần điều trị', 'khám và điều trị răng miệng', 'các dịch vụ nha khoa', 
        'bệnh lý viêm nướu', 'các vấn đề về hàm mặt', 'điều trị sâu răng', 'các triệu chứng nha khoa',
        'khám tổng quát răng miệng', 'chăm sóc răng miệng hàng ngày', 'tư vấn về nha khoa',
        'các phương pháp điều trị răng', 'các sản phẩm chăm sóc răng', 'răng khôn', 
        'các dấu hiệu bệnh lý răng miệng', 'tư vấn niềng răng', 'răng giả', 'bệnh lý viêm tủy',
        'các vấn đề về nướu', 'khám và điều trị nướu', 'điều trị nha chu', 'các triệu chứng nướu', 
        'các bệnh lý về răng miệng mãn tính', 'khám và điều trị răng cho trẻ', 
        'các dấu hiệu bất thường ở răng', 'điều trị mòn răng', 'các bệnh lý liên quan', 
        'bệnh lý về miệng', 'các triệu chứng miệng', 'tư vấn sức khỏe răng miệng', 
        'các dịch vụ chăm sóc răng miệng', 'khám răng miệng định kỳ', 'điều trị tình trạng răng', 
        'các dấu hiệu bệnh lý răng miệng', 'khám và điều trị tình trạng răng', 
        'điều trị viêm chân răng', 'tư vấn khám răng'
    ],
    'PK Nhi tại khoa': [
        'nhi', 'trẻ em', 'đau bụng', 'tiêm chủng', 'khám sức khỏe', 
        'bệnh thường gặp', 'phát triển trẻ em', 'bệnh nhi', 'bệnh lý nhi khoa', 
        'bệnh truyền nhiễm ở trẻ em', 'các dấu hiệu bất thường ở trẻ', 'khám sức khỏe định kỳ', 
        'tư vấn về sức khỏe trẻ em', 'điều trị bệnh trẻ em', 'chăm sóc sức khỏe trẻ em', 
        'các bệnh lý mãn tính ở trẻ em', 'bệnh lý hô hấp ở trẻ em', 'bệnh lý tiêu hóa', 
        'các vấn đề về phát triển', 'khám và điều trị', 'các triệu chứng bệnh nhi', 
        'tư vấn dinh dưỡng cho trẻ', 'các dịch vụ nhi khoa', 'bệnh lý da ở trẻ em', 
        'các vấn đề về răng miệng ở trẻ', 'tiêm chủng cho trẻ', 'các triệu chứng thường gặp', 
        'khám tổng quát sức khỏe trẻ em', 'các dấu hiệu cần khám', 'các bệnh lý viêm', 
        'bệnh lý nhiễm trùng', 'tư vấn sức khỏe dinh dưỡng', 'các bệnh lý dị ứng', 
        'điều trị bệnh tiêu hóa', 'bệnh lý hô hấp cấp tính', 'các triệu chứng cần theo dõi', 
        'chăm sóc sức khỏe cho trẻ sơ sinh', 'các triệu chứng nhi khoa cần lưu ý', 
        'bệnh lý tim mạch ở trẻ em', 'tình trạng trẻ em cần theo dõi', 
        'các phương pháp điều trị bệnh nhi', 'tư vấn chăm sóc sức khỏe trẻ sơ sinh', 
        'bệnh lý nội khoa ở trẻ em', 'các dấu hiệu cần điều trị', 'bệnh lý thần kinh', 
        'các triệu chứng về mắt', 'tư vấn tiêm chủng', 'điều trị các bệnh lý về sức khỏe', 
        'bệnh lý nội tiết', 'bệnh lý nhi khoa mãn tính', 'các dịch vụ y tế cho trẻ em', 
        'bệnh lý tiêu hóa ở trẻ em', 'điều trị dị ứng ở trẻ em', 'khám sức khỏe cho trẻ'
    ],

        'Pk Nội I': [
        'nội', 'khám nội', 'bệnh lý nội khoa', 'huyết áp', 'đái tháo đường', 
        'mỡ máu', 'tim mạch', 'tiêu hóa', 'hô hấp', 'nhiễm trùng', 
        'mệt mỏi', 'đau bụng', 'rối loạn tiêu hóa', 'viêm phổi', 'huyết áp thấp',
        'khám sức khỏe', 'chăm sóc sức khỏe', 'tư vấn điều trị', 'bệnh lý mãn tính',
        'khám và chẩn đoán', 'điều trị nội khoa', 'xét nghiệm', 'điều trị bảo tồn',
        'bệnh lý tiêu hóa', 'bệnh lý hệ hô hấp', 'khám định kỳ', 'bệnh lý tim mạch',
        'huyết áp cao', 'tư vấn dinh dưỡng', 'chăm sóc người cao tuổi', 'tình trạng sức khỏe',
        'các triệu chứng cần theo dõi', 'tư vấn bệnh lý nội khoa', 'hệ tiêu hóa', 
        'điều trị bệnh nội khoa', 'các vấn đề về sức khỏe', 'phòng ngừa bệnh tật', 
        'bệnh lý truyền nhiễm', 'các triệu chứng nội khoa', 'khám sức khỏe tổng quát',
        'bệnh lý thận', 'điều trị các bệnh lý nội khoa', 'tư vấn chăm sóc sức khỏe', 
        'bệnh lý xương khớp', 'bệnh lý tiểu đường', 'tình trạng sức khỏe cần theo dõi'
    ],

        'Pk Ung bướu yêu cầu': [
        'ung thư', 'u bướu', 'chẩn đoán ung thư', 'điều trị ung thư', 'xét nghiệm ung thư',
        'khám ung bướu', 'bệnh ung thư', 'ung thư vú', 'ung thư phổi', 'ung thư đại trực tràng',
        'ung thư dạ dày', 'điều trị hóa trị', 'hóa trị liệu', 'xạ trị', 'chăm sóc bệnh nhân ung thư',
        'tư vấn sức khỏe ung thư', 'bệnh lý u bướu', 'triệu chứng ung thư', 'tư vấn dinh dưỡng cho bệnh nhân ung thư',
        'theo dõi ung thư', 'bệnh lý di căn', 'các phương pháp điều trị ung thư', 'ung thư gan', 
        'tư vấn di truyền', 'bệnh lý ung thư máu', 'bệnh lý u não', 'bệnh lý u bướu lành tính',
        'chẩn đoán hình ảnh ung thư', 'các triệu chứng cần theo dõi', 'tư vấn chăm sóc sức khỏe', 
        'điều trị triệu chứng ung thư', 'bệnh lý ung thư cổ tử cung', 'bệnh lý ung thư tuyến giáp', 
        'các dịch vụ khám ung bướu', 'theo dõi điều trị ung thư', 'bệnh lý ung thư tuyến tiền liệt'
    ],
    'Pk Nội Tiết-Đái Tháo Đường2': [
    'đái tháo đường', 'tiết nội', 'điều trị đái tháo đường', 'tiêu chuẩn kiểm soát đường huyết', 
    'bệnh lý nội tiết', 'bệnh lý chuyển hóa', 'chăm sóc bệnh nhân đái tháo đường', 
    'tư vấn dinh dưỡng', 'bệnh lý tim mạch', 'huyết áp', 
    'bệnh lý thận', 'bệnh lý mắt', 'tình trạng sức khỏe', 
    'khám và điều trị đái tháo đường', 'điều trị biến chứng đái tháo đường', 
    'kiểm tra đường huyết', 'bệnh lý rối loạn lipid', 'sử dụng insulin', 
    'bệnh lý tuyến giáp', 'bệnh lý hạ đường huyết', 'tư vấn cách sống khỏe', 
    'các loại thuốc điều trị đái tháo đường', 'theo dõi sức khỏe', 
    'bệnh lý mạch máu', 'điều trị bệnh lý nội tiết', 'tư vấn sức khỏe nội tiết', 
    'các triệu chứng bệnh đái tháo đường', 'khám sức khỏe định kỳ', 
    'các biện pháp phòng ngừa', 'chế độ ăn uống cho bệnh nhân đái tháo đường', 
    'các biến chứng nội tiết', 'tình trạng đường huyết không ổn định'
],

    'Pk Tăng Huyết Áp_2': [
    'tăng huyết áp', 'huyết áp cao', 'điều trị tăng huyết áp', 'kiểm soát huyết áp', 
    'chăm sóc bệnh nhân tăng huyết áp', 'triệu chứng cao huyết áp', 
    'biến chứng của tăng huyết áp', 'bệnh lý tim mạch', 'tư vấn dinh dưỡng', 
    'chế độ ăn uống cho người huyết áp cao', 'các loại thuốc điều trị', 
    'tăng huyết áp thứ phát', 'huyết áp thấp', 'theo dõi huyết áp', 
    'các yếu tố nguy cơ', 'bệnh lý mạch máu', 'tình trạng sức khỏe', 
    'khám sức khỏe định kỳ', 'các biện pháp phòng ngừa', 
    'đo huyết áp', 'các triệu chứng cần lưu ý', 
    'tư vấn sức khỏe tim mạch', 'điều trị biến chứng huyết áp cao', 
    'huyết áp không ổn định', 'huyết áp tâm thu', 
    'huyết áp tâm trương', 'các bệnh lý nội tiết liên quan', 
    'điều chỉnh lối sống', 'tập thể dục cho người tăng huyết áp'
],

    'Pk Cơ Xương Khớp': [
    'cơ xương khớp', 'đau khớp', 'viêm khớp', 'bệnh lý xương', 
    'gãy xương', 'thoái hóa khớp', 'đau lưng', 'đau cơ', 
    'các triệu chứng cơ xương khớp', 'chấn thương', 
    'chăm sóc bệnh nhân cơ xương khớp', 'tư vấn dinh dưỡng', 
    'các biện pháp điều trị', 'điều trị viêm khớp', 
    'vật lý trị liệu', 'các bài tập phục hồi', 
    'khám sức khỏe định kỳ', 'bệnh lý liên quan đến tuổi tác', 
    'các yếu tố nguy cơ', 'điều trị đau nhức', 
    'hạn chế vận động', 'sử dụng thuốc giảm đau', 
    'bệnh lý gút', 'các vấn đề về vận động', 
    'các triệu chứng cần lưu ý', 'tình trạng sức khỏe', 
    'điều trị thoái hóa khớp', 'tư vấn lối sống lành mạnh'
]
,
    'Pk Tăng Huyết Áp 3 - Tim Mạch': [
    'tim mạch', 'tăng huyết áp', 'bệnh tim', 'các bệnh lý tim mạch', 
    'điều trị tăng huyết áp', 'kiểm soát huyết áp', 'các triệu chứng tim mạch', 
    'bệnh mạch vành', 'suy tim', 'các yếu tố nguy cơ', 
    'tư vấn dinh dưỡng', 'chế độ ăn uống cho bệnh nhân tim mạch', 
    'tập thể dục cho tim mạch', 'biến chứng của huyết áp cao', 
    'các loại thuốc điều trị', 'theo dõi huyết áp', 
    'điều trị bệnh lý tim', 'huyết áp không ổn định', 
    'khám sức khỏe định kỳ', 'các biện pháp phòng ngừa', 
    'huyết áp tâm thu', 'huyết áp tâm trương', 
    'tình trạng sức khỏe', 'bệnh lý huyết áp', 
    'điều trị các biến chứng', 'tư vấn sức khỏe tim mạch', 
    'các triệu chứng cần lưu ý', 'điều chỉnh lối sống', 
    'các phương pháp điều trị hiện đại', 'chăm sóc bệnh nhân tim mạch'
],

    'Pk Y Học Cổ Truyền': [
    'y học cổ truyền', 'thuốc đông y', 'điều trị bằng thảo dược', 
    'châm cứu', 'bấm huyệt', 'các phương pháp y học cổ truyền', 
    'điều trị bệnh mãn tính', 'tư vấn sức khỏe', 
    'các loại thảo dược', 'các bài thuốc dân gian', 
    'thái độ với y học cổ truyền', 'phòng bệnh bằng y học cổ truyền', 
    'các liệu pháp điều trị', 'tác dụng của thảo dược', 
    'các chứng bệnh thường gặp', 'bệnh lý liên quan đến khí huyết', 
    'cân bằng âm dương', 'các phương pháp trị liệu', 
    'khám sức khỏe định kỳ', 'sức khỏe tinh thần', 
    'điều trị các vấn đề về tiêu hóa', 'bệnh lý xương khớp', 
    'các triệu chứng cần lưu ý', 'cách sử dụng thuốc đông y', 
    'điều trị bằng phương pháp tự nhiên', 'y học cổ truyền và hiện đại', 
    'tư vấn dinh dưỡng', 'bệnh lý thần kinh', 
    'phương pháp nâng cao sức khỏe', 'y học cổ truyền trong điều trị bệnh'
],
















    'Pk Nội Tiết-đái Tháo Đường': [
    'đái tháo đường', 'tiết nội', 'khát nước nhiều', 'tiểu nhiều', 
    'mệt mỏi', 'đói nhiều', 'sụt cân', 'mờ mắt', 
    'ngứa ngáy', 'vết thương lâu lành', 'nhiễm trùng thường xuyên', 
    'đau đầu', 'đau nhức cơ bắp', 'tê bì tay chân', 
    'khó thở', 'buồn nôn', 'rối loạn tiêu hóa', 
    'mồ hôi ra nhiều', 'chóng mặt', 'thay đổi về da', 
    'huyết áp cao', 'đi tiểu đêm', 'cảm giác không bình thường', 
    'vấn đề về tình dục', 'bệnh lý tim mạch', 
    'tăng cholesterol', 'suy giảm khả năng miễn dịch', 
    'tăng huyết áp', 'đau bụng', 'các triệu chứng về thần kinh'
],

    'Pk Quản lý Parkinson - Sa sút trí tuệ': [
    'parkinson', 'trí tuệ', 'run tay', 'cứng cơ', 
    'khó khăn khi di chuyển', 'mất thăng bằng', 
    'trí nhớ kém', 'khó nói', 'mệt mỏi', 
    'thay đổi tâm trạng', 'giảm khả năng chú ý', 
    'khó khăn trong việc hoàn thành công việc', 
    'rối loạn giấc ngủ', 'cảm giác chán nản', 
    'suy giảm nhận thức', 'mất khả năng tư duy', 
    'các triệu chứng cảm xúc', 'vấn đề về thị lực', 
    'khó khăn trong giao tiếp', 'các triệu chứng về tâm lý', 
    'suy giảm khả năng tự chăm sóc', 'các triệu chứng liên quan đến hành vi', 
    'thay đổi thói quen sinh hoạt', 'tình trạng trầm cảm', 
    'những thay đổi trong sự phối hợp', 'các vấn đề về ngôn ngữ', 
    'bệnh lý thần kinh', 'tăng cảm giác đau', 
    'các triệu chứng về thể chất'
],

    'Pk Truyền Nhiễm': [
    'truyền nhiễm', 'sốt', 'đau đầu', 'ho', 
    'khó thở', 'đau họng', 'mệt mỏi', 
    'đổ mồ hôi đêm', 'giảm cân', 'buồn nôn', 
    'nôn', 'tiêu chảy', 'đau bụng', 
    'cảm lạnh', 'phát ban', 'ngứa', 
    'sưng hạch bạch huyết', 'đau cơ', 'chán ăn', 
    'khó nuốt', 'các triệu chứng hô hấp', 
    'cảm giác mệt mỏi kéo dài', 'nhiễm khuẩn', 
    'bệnh lây truyền qua đường tình dục', 'bệnh do vi rút', 
    'bệnh do vi khuẩn', 'bệnh ký sinh trùng', 
    'bệnh do nấm', 'các dấu hiệu nhiễm trùng', 
    'đau ngực', 'các triệu chứng tiêu hóa', 
    'mẩn ngứa', 'tình trạng sốt cao'
]
,
    'Pk Nội Thận - Tiết niệu và Lọc Máu': [
    'tiết niệu', 'lọc máu', 'đau lưng', 'tiểu buốt', 
    'tiểu nhiều', 'tiểu ít', 'khó tiểu', 
    'đái ra máu', 'sưng phù', 'mệt mỏi', 
    'chán ăn', 'buồn nôn', 'mất nước', 
    'cảm giác mệt mỏi kéo dài', 'nhức đầu', 
    'tăng huyết áp', 'các vấn đề về nước tiểu', 
    'thay đổi màu sắc nước tiểu', 'các triệu chứng về thận', 
    'đau bụng dưới', 'đau bên hông', 'các vấn đề về thận', 
    'các triệu chứng suy thận', 'khó khăn khi tiểu', 
    'các dấu hiệu nhiễm trùng tiết niệu', 'các triệu chứng liên quan đến lọc máu', 
    'đi tiểu đêm', 'mồ hôi ra nhiều', 
    'cảm giác khó chịu trong cơ thể', 'bệnh lý thận mạn tính', 
    'tăng kali trong máu', 'các triệu chứng liên quan đến thận'
]
,
    'PK Ngoại Thần Kinh': [
    'thần kinh', 'đau đầu', 'chóng mặt', 
    'khó khăn trong việc đi lại', 'yếu cơ', 
    'tê bì tay chân', 'mất cảm giác', 
    'run tay', 'co giật', 'đau lưng', 
    'cảm giác nóng rát', 'rối loạn giấc ngủ', 
    'thay đổi tâm trạng', 'khó khăn trong việc nói', 
    'mệt mỏi', 'các triệu chứng về trí nhớ', 
    'khó khăn trong việc tập trung', 'các vấn đề về nhận thức', 
    'cảm giác châm chích', 'các triệu chứng về thần kinh', 
    'suy giảm trí nhớ', 'các vấn đề về thăng bằng', 
    'suy yếu thể chất', 'tình trạng lo âu', 
    'trầm cảm', 'các triệu chứng về cảm xúc', 
    'đau dây thần kinh', 'đi lại khó khăn', 
    'các triệu chứng liên quan đến đột quỵ', 'các vấn đề về giao tiếp', 
    'bệnh lý thần kinh', 'tình trạng mất ngủ'
]
,
    'Pk Huyết Học Lâm Sàng': [
    'huyết học', 
    'thiếu máu', 
    'đau nhức xương', 
    'chảy máu cam', 
    'bầm tím', 
    'mệt mỏi', 
    'khó thở', 
    'tim đập nhanh', 
    'choáng váng', 
    'suy giảm miễn dịch', 
    'đau bụng', 
    'tăng bạch cầu', 
    'giảm bạch cầu', 
    'các triệu chứng về da', 
    'màu da nhợt nhạt', 
    'cảm giác lạnh', 
    'sưng hạch bạch huyết'
]
,
    'PK Nội tiết - YHHN': [
    'nội tiết', 
    'thay đổi cân nặng', 
    'mệt mỏi', 
    'khát nước nhiều', 
    'tiểu nhiều', 
    'tăng huyết áp', 
    'rối loạn kinh nguyệt', 
    'dễ bị lạnh', 
    'cảm giác nóng bừng', 
    'tăng cường độ cảm giác thèm ăn', 
    'giảm ham muốn tình dục', 
    'các triệu chứng về da', 
    'huyết áp không ổn định', 
    'các vấn đề về giấc ngủ', 
    'tâm trạng lo âu', 
    'trầm cảm', 
    'rối loạn tiêu hóa'
]
,
    'Pk Phục Hồi Chức Năng': [
    'phục hồi', 
    'chức năng', 
    'yếu cơ', 
    'khó khăn trong việc di chuyển', 
    'đau nhức cơ', 
    'khó khăn trong việc thực hiện các hoạt động hàng ngày', 
    'tê bì tay chân', 
    'cảm giác mệt mỏi', 
    'giảm sức mạnh cơ bắp', 
    'suy giảm khả năng thăng bằng', 
    'khó khăn trong việc phối hợp', 
    'cảm giác đau', 
    'các triệu chứng về tinh thần', 
    'trầm cảm', 
    'lo âu', 
    'giảm khả năng tập trung'
]
,
    'Pk Ngoại Tim mạch - Lồng ngực': [
    'tim mạch', 
    'ngoại khoa', 
    'đau ngực', 
    'khó thở', 
    'đánh trống ngực', 
    'mệt mỏi', 
    'chóng mặt', 
    'sưng phù chân', 
    'đau bụng', 
    'cảm giác nặng nề ở ngực', 
    'tiểu khó', 
    'tăng huyết áp', 
    'mồ hôi đổ nhiều', 
    'buồn nôn', 
    'các triệu chứng về tuần hoàn', 
    'tê bì tay chân', 
    'cảm giác châm chích'
]
,
    'Pk Yêu cầu': [
    'yêu cầu', 
    'khó khăn trong việc giao tiếp', 
    'cảm giác lo lắng', 
    'khó khăn trong việc đưa ra quyết định', 
    'tâm trạng thất vọng', 
    'cảm giác áp lực', 
    'mệt mỏi về tinh thần', 
    'khó khăn trong việc tổ chức công việc', 
    'thiếu sự hỗ trợ', 
    'khó khăn trong việc quản lý thời gian', 
    'cảm giác cô đơn', 
    'các vấn đề về tương tác xã hội', 
    'khó khăn trong việc theo dõi thông tin', 
    'khó khăn trong việc thích nghi với thay đổi', 
    'cảm giác mất kiểm soát', 
    'cảm giác bất an'
]
,
    'pk.Ngoại Tiết niệu': [
    'tiết niệu', 
    'đau bụng dưới', 
    'tiểu đau', 
    'tiểu gắt', 
    'tiểu ra máu', 
    'khó tiểu', 
    'tiểu nhiều lần', 
    'mùi nước tiểu bất thường', 
    'đau lưng', 
    'sưng phù vùng bụng', 
    'mệt mỏi', 
    'sốt', 
    'cảm giác buồn nôn', 
    'các triệu chứng về tiểu đường', 
    'rối loạn chức năng thận', 
    'cảm giác khô miệng'
]
,
    'Pk Y Học Hạt Nhân': [
    'hạt nhân', 
    'đau nhức xương', 
    'mệt mỏi', 
    'khó thở', 
    'tiêu chảy', 
    'buồn nôn', 
    'nôn', 
    'giảm cân không rõ lý do', 
    'thay đổi trong vị giác', 
    'rụng tóc', 
    'suy giảm miễn dịch', 
    'đau đầu', 
    'các triệu chứng về da', 
    'khó khăn trong việc hồi phục', 
    'sốt', 
    'cảm giác mệt mỏi kéo dài'
]
,
    'Pk Ung bướu': [
    'ung bướu', 
    'mệt mỏi', 
    'giảm cân không rõ lý do', 
    'đau nhức', 
    'cảm giác buồn nôn', 
    'nôn', 
    'thay đổi trong thói quen đi tiêu', 
    'khó nuốt', 
    'đau ngực', 
    'sưng hạch bạch huyết', 
    'các triệu chứng về da', 
    'đổ mồ hôi ban đêm', 
    'cảm giác chán ăn', 
    'thay đổi màu sắc da', 
    'khó thở', 
    'các vấn đề về trí nhớ'
]
,
    'Pk Tâm Thần': [
    'tâm thần', 
    'trầm cảm', 
    'lo âu', 
    'rối loạn giấc ngủ', 
    'cảm giác mệt mỏi', 
    'khó khăn trong việc tập trung', 
    'thay đổi tâm trạng', 
    'cảm giác cô đơn', 
    'suy giảm trí nhớ', 
    'các triệu chứng hoang tưởng', 
    'các triệu chứng ảo giác', 
    'cảm giác bồn chồn', 
    'khó khăn trong việc giao tiếp', 
    'tâm trạng thất vọng', 
    'suy giảm khả năng quyết định', 
    'khó khăn trong việc xử lý cảm xúc'
]
,
    'Pk Lão khoa - Bảo Vệ Sức Khoẻ': [
    'lão khoa', 
    'mệt mỏi', 
    'đau khớp', 
    'đau cơ', 
    'giảm trí nhớ', 
    'khó ngủ', 
    'khó thở', 
    'huyết áp cao', 
    'tiểu đường', 
    'tăng cholesterol', 
    'suy giảm thị lực', 
    'suy giảm thính lực', 
    'suy giảm cân nặng', 
    'cảm giác chóng mặt', 
    'các vấn đề về thăng bằng', 
    'tình trạng lo âu'
]
,
    'Pk Nhi': [
    'nhi', 
    'sốt', 
    'ho', 
    'chảy nước mũi', 
    'nôn', 
    'tiêu chảy', 
    'đau bụng', 
    'khó thở', 
    'mệt mỏi', 
    'cảm giác đau họng', 
    'nổi mẩn ngứa', 
    'mất nước', 
    'đau tai', 
    'thay đổi trong khẩu vị', 
    'cảm giác bồn chồn', 
    'thay đổi tâm trạng'
]
,
    'Pk Phụ Sản': [
    'phụ sản', 
    'đau bụng', 
    'chảy máu âm đạo', 
    'mệt mỏi', 
    'buồn nôn', 
    'tiểu nhiều lần', 
    'khó thở', 
    'cảm giác căng tức ngực', 
    'các triệu chứng tiền kinh nguyệt', 
    'thay đổi tâm trạng', 
    'đau lưng', 
    'dễ bị chuột rút', 
    'các triệu chứng về tiểu đường thai kỳ', 
    'suy giảm ham muốn tình dục', 
    'cảm giác lo âu', 
    'cảm giác mệt mỏi kéo dài'
]
,
'Pk Thần Kinh': [
    'thần kinh', 
    'đau đầu', 
    'chóng mặt', 
    'yếu cơ', 
    'tê bì tay chân', 
    'mất cảm giác', 
    'run tay', 
    'co giật', 
    'cảm giác châm chích', 
    'khó khăn trong việc đi lại', 
    'suy giảm trí nhớ', 
    'các vấn đề về tập trung', 
    'thay đổi tâm trạng', 
    'các triệu chứng về cảm xúc', 
    'khó khăn trong việc nói', 
    'mệt mỏi'
]
,
    'Pk Ngoại': [
    'ngoại khoa', 
    'đau bụng', 
    'sưng tấy', 
    'vết thương hở', 
    'đau ngực', 
    'khó thở', 
    'sốt', 
    'cảm giác mệt mỏi', 
    'đau lưng', 
    'tiểu ra máu', 
    'các triệu chứng về da', 
    'đau đầu', 
    'cảm giác buồn nôn', 
    'khó khăn trong việc di chuyển', 
    'cảm giác chóng mặt', 
    'các triệu chứng về tuần hoàn'
]
,
    'Pk Sản': [
    'sản khoa', 
    'đau bụng', 
    'chảy máu âm đạo', 
    'mệt mỏi', 
    'buồn nôn', 
    'tiểu nhiều lần', 
    'khó thở', 
    'căng tức ngực', 
    'dễ bị chuột rút', 
    'các triệu chứng tiền kinh nguyệt', 
    'thay đổi tâm trạng', 
    'đau lưng', 
    'dễ bị kiệt sức', 
    'các triệu chứng về tiêu hóa', 
    'cảm giác lo âu', 
    'các triệu chứng về da'
]
,
    'Pk phụ sản dịch vụ': [
    'phụ sản', 
    'dịch vụ', 
    'đau bụng', 
    'chảy máu âm đạo', 
    'mệt mỏi', 
    'buồn nôn', 
    'khó thở', 
    'cảm giác căng tức ngực', 
    'thay đổi tâm trạng', 
    'đau lưng', 
    'khó chịu vùng bụng', 
    'dễ bị chuột rút', 
    'các triệu chứng về da', 
    'cảm giác lo âu', 
    'thay đổi trong chu kỳ kinh nguyệt', 
    'các triệu chứng về sinh lý'
]
,
    'Pk Ngoại Nhi': [
    'ngoại nhi', 
    'đau bụng', 
    'sốt', 
    'chảy máu', 
    'sưng tấy', 
    'đau đầu', 
    'khó thở', 
    'nôn', 
    'tiêu chảy', 
    'cảm giác mệt mỏi', 
    'đau tai', 
    'dễ bị ngã', 
    'các triệu chứng về da', 
    'thay đổi trong hành vi', 
    'cảm giác lo âu', 
    'khó khăn trong việc đi lại'
]
,
    'Pk Trưởng Khoa': [
    'trưởng khoa', 
    'quản lý nhân sự', 
    'cảm giác áp lực', 
    'khó khăn trong việc ra quyết định', 
    'mệt mỏi', 
    'cảm giác lo âu', 
    'tâm trạng thất vọng', 
    'khó khăn trong việc tổ chức công việc', 
    'cảm giác cô đơn', 
    'khó khăn trong việc giao tiếp', 
    'suy giảm tập trung', 
    'cảm giác không đủ thời gian', 
    'dễ bị căng thẳng', 
    'các triệu chứng về sức khỏe tâm thần', 
    'khó khăn trong việc quản lý xung đột', 
    'cảm giác bất an'
]
,
    'PK Nội Tiết Dịch Vụ': [
    'dịch vụ', 
    'nội tiết', 
    'thay đổi cân nặng', 
    'khát nước nhiều', 
    'tiểu nhiều lần', 
    'mệt mỏi', 
    'rối loạn kinh nguyệt', 
    'dễ bị lạnh', 
    'cảm giác nóng bừng', 
    'tăng huyết áp', 
    'giảm ham muốn tình dục', 
    'thay đổi tâm trạng', 
    'các triệu chứng về da', 
    'tăng cường độ cảm giác thèm ăn', 
    'suy giảm trí nhớ', 
    'các triệu chứng về tiêu hóa'
]
,
    'Pk Yêu cầu CXK': [
    'yêu cầu', 
    'khó khăn trong việc giao tiếp', 
    'cảm giác lo lắng', 
    'khó khăn trong việc đưa ra quyết định', 
    'tâm trạng thất vọng', 
    'cảm giác áp lực', 
    'mệt mỏi về tinh thần', 
    'khó khăn trong việc tổ chức công việc', 
    'thiếu sự hỗ trợ', 
    'cảm giác cô đơn', 
    'các vấn đề về tương tác xã hội', 
    'khó khăn trong việc theo dõi thông tin', 
    'khó khăn trong việc thích nghi với thay đổi', 
    'cảm giác mất kiểm soát', 
    'cảm giác bất an'
]
,
    'PK TT Tạo Hình Thẩm Mỹ': [
    'tạo hình', 
    'thẩm mỹ', 
    'đau nhức', 
    'sưng tấy', 
    'cảm giác khó chịu', 
    'mệt mỏi', 
    'cảm giác lo âu', 
    'các triệu chứng về da', 
    'cảm giác ngứa', 
    'thay đổi trong cảm giác', 
    'cảm giác không hài lòng với kết quả', 
    'các vấn đề về hồi phục', 
    'đỏ vùng phẫu thuật', 
    'cảm giác đau nhói', 
    'các triệu chứng về tâm lý', 
    'cảm giác mất tự tin'
]
,
    'PK Ưu tiên': [
    'ưu tiên', 
    'cảm giác áp lực', 
    'mệt mỏi', 
    'khó khăn trong việc đưa ra quyết định', 
    'cảm giác lo âu', 
    'thay đổi tâm trạng', 
    'khó khăn trong việc quản lý thời gian', 
    'cảm giác không đủ thời gian', 
    'các triệu chứng về tinh thần', 
    'cảm giác bất an', 
    'cảm giác cô đơn', 
    'dễ bị căng thẳng', 
    'cảm giác thất vọng', 
    'các triệu chứng về giao tiếp', 
    'khó khăn trong việc tương tác xã hội'
]
,
    'Pk Nội Tim Mạch tại khoa': [
    'tim mạch', 
    'đau ngực', 
    'khó thở', 
    'mệt mỏi', 
    'nhịp tim không đều', 
    'sưng phù chân', 
    'đau đầu', 
    'chóng mặt', 
    'cảm giác hồi hộp', 
    'tăng huyết áp', 
    'huyết áp thấp', 
    'cảm giác choáng', 
    'các triệu chứng về tuần hoàn', 
    'thay đổi trong hoạt động thể chất', 
    'các triệu chứng về tiêu hóa', 
    'suy tim'
]
,
    'Pk Phó khoa (P227)': [
    'phó khoa', 
    'cảm giác áp lực', 
    'mệt mỏi', 
    'khó khăn trong việc quản lý thời gian', 
    'cảm giác không đủ hỗ trợ', 
    'khó khăn trong việc ra quyết định', 
    'cảm giác lo âu', 
    'thay đổi tâm trạng', 
    'các vấn đề về giao tiếp', 
    'cảm giác cô đơn', 
    'căng thẳng', 
    'cảm giác bất an', 
    'khó khăn trong việc tổ chức công việc', 
    'các triệu chứng về sức khỏe tâm thần', 
    'suy giảm khả năng tập trung'
]
,
    'Pk Tư Vấn Tiêm Chủng': [
    'tiêm chủng', 
    'đau tại vị trí tiêm', 
    'sưng tấy', 
    'mệt mỏi', 
    'sốt nhẹ', 
    'đau đầu', 
    'buồn nôn', 
    'chóng mặt', 
    'cảm giác khó chịu', 
    'các triệu chứng về da', 
    'tăng cảm giác lo âu', 
    'thay đổi tâm trạng', 
    'cảm giác không thoải mái', 
    'khó ngủ', 
    'các triệu chứng dị ứng', 
    'cảm giác lạnh hoặc ớn lạnh'
]
,
    'Pk Nội Tiêu Hoá Dịch vụ': [
    'tiêu hóa', 
    'dịch vụ', 
    'đau bụng', 
    'tiêu chảy', 
    'buồn nôn', 
    'nôn', 
    'đầy hơi', 
    'khó tiêu', 
    'cảm giác chướng bụng', 
    'thay đổi khẩu vị', 
    'sụt cân', 
    'mệt mỏi', 
    'đau dạ dày', 
    'cảm giác khó chịu sau ăn', 
    'các triệu chứng về đại tràng', 
    'các vấn đề về tiêu hóa'
]
,
    'Pk Phó Khoa': [
    'phó khoa', 
    'cảm giác áp lực', 
    'mệt mỏi', 
    'khó khăn trong việc quản lý thời gian', 
    'cảm giác không đủ hỗ trợ', 
    'khó khăn trong việc ra quyết định', 
    'cảm giác lo âu', 
    'thay đổi tâm trạng', 
    'các vấn đề về giao tiếp', 
    'cảm giác cô đơn', 
    'căng thẳng', 
    'cảm giác bất an', 
    'khó khăn trong việc tổ chức công việc', 
    'các triệu chứng về sức khỏe tâm thần', 
    'suy giảm khả năng tập trung'
]
,
    'Pk Nội Tiết-Đái Tháo Đường': [
    'đái tháo đường', 
    'khát nước nhiều', 
    'tiểu nhiều lần', 
    'mệt mỏi', 
    'tăng cân', 
    'giảm cân không rõ lý do', 
    'đau đầu', 
    'thị lực mờ', 
    'cảm giác ngứa', 
    'vết thương lâu lành', 
    'các triệu chứng về da', 
    'cảm giác tê bì tay chân', 
    'suy giảm ham muốn tình dục', 
    'các triệu chứng về tiêu hóa', 
    'cảm giác lo âu', 
    'khó ngủ'
]
,
    'Pk Khám và Tư Vấn Dinh Dưỡng': [
    'dinh dưỡng', 
    'mệt mỏi', 
    'sụt cân', 
    'tăng cân', 
    'cảm giác đói liên tục', 
    'thiếu năng lượng', 
    'cảm giác thèm ăn bất thường', 
    'các vấn đề về tiêu hóa', 
    'da khô', 
    'rụng tóc', 
    'cảm giác buồn nôn', 
    'các triệu chứng về sức khỏe tâm thần', 
    'hệ miễn dịch yếu', 
    'các triệu chứng về tuần hoàn', 
    'khó ngủ', 
    'tâm trạng thất vọng'
]

}

def match_department(QUATRINHBENHLY, KHAMBENHTOANTHAN, KHAMBENHCACBOPHAN, LYDODIEUTRI):
    scores = {k: 0 for k in khoa_phong.keys()}
    input_data = [QUATRINHBENHLY, KHAMBENHTOANTHAN, KHAMBENHCACBOPHAN, LYDODIEUTRI]

    for department, keywords in khoa_phong.items():
        for keyword in keywords:
            keyword = keyword.lower()
            for entry in input_data:
                if keyword in entry.lower():
                    scores[department] += 1

    max_score = max(scores.values())
    best_departments = [dept for dept, score in scores.items() if score == max_score]

    return best_departments[0] if best_departments else 'Khoa phòng không xác định'

# Hàm để làm sạch mức lương (được điều chỉnh cho phù hợp)
def clean_data(data_str):
    return data_str.strip() if data_str else "N/A"

# Đọc dữ liệu từ file CSV
def get_dataset():
    dataset = []
    with open('data/Du-lieu-KhamBenhT042024.csv', mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Làm sạch và lấy dữ liệu từ các cột
            age = clean_data(row.get('TUOI'))
            gender = clean_data(row.get('TENPHAI'))
            province = clean_data(row.get('TENTINHTHANH'))
            district = clean_data(row.get('TENQUANHUYEN'))
            date = clean_data(row.get('NGAYKHAM'))
            insurance_type = clean_data(row.get('MADOITUONG'))
            insurance_name = clean_data(row.get('TENDOITUONG'))
            diagnosis_code = clean_data(row.get('MAICD'))
            main_disease = clean_data(row.get('BENHCHINH'))
            fee_name = clean_data(row.get('TENGIAVIENPHI'))
            department_name = clean_data(row.get('TENKHOAPHONG'))
            fee_type = clean_data(row.get('TENLOAIVIENPHI'))
            medical_history = clean_data(row.get('QUATRINHBENHLY'))
            general_examination = clean_data(row.get('KHAMBENHTOANTHAN'))
            specific_examination = clean_data(row.get('KHAMBENHCACBOPHAN'))
            treatment_reason = clean_data(row.get('LYDODIEUTRI'))

            dataset.append({
                'age': age,
                'gender': gender,
                'province': province,
                'district': district,
                'date': date,
                'insurance_type': insurance_type,
                'insurance_name': insurance_name,
                'diagnosis_code': diagnosis_code,
                'main_disease': main_disease,
                'fee_name': fee_name,
                'department_name': department_name,
                'fee_type': fee_type,
                'medical_history': medical_history,
                'general_examination': general_examination,
                'specific_examination': specific_examination,
                'treatment_reason': treatment_reason
            })
    
    return dataset

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

@app.route('/dataset')
def dataset():
    # Đọc dữ liệu từ tệp CSV
    data = get_dataset()
    return render_template('dataset.html', data=data)

@app.route('/xgboost')
def xgboost():
    # Hiển thị giải thích thuật toán XGBoost
    return render_template('xgboost.html')

@app.route('/about')
def about():
    # Hiển thị thông tin tác giả
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)