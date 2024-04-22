from flask import Flask, request, jsonify
import requests

from DatabaseManager import retrieve_data, authenticate

app = Flask(__name__)


@app.route('/authenticate', methods=['POST'])
def authenticate_handler():
    url = "https://waifu-run-7683a-default-rtdb.firebaseio.com/DB.json?print=pretty"
    tai_khoan_list, nhom_quyen_list, nhan_vien_list = retrieve_data(url)
    data = request.json
    if 'TenTaiKhoan' not in data or 'MatKhau' not in data:
        return jsonify({'message': 'Tên tài khoản và mật khẩu là bắt buộc.'}), 400

    TenTaiKhoan = data['TenTaiKhoan']
    MatKhau = data['MatKhau']

    # Kiểm tra xem tên tài khoản và mật khẩu có khớp với danh sách tài khoản hay không
    if authenticate(TenTaiKhoan, MatKhau, tai_khoan_list):
        return jsonify({'authenticated': True}), 200
    return jsonify({'authenticated': False}), 401


def test(TenTaiKhoan, MatKhau):
    url = 'http://127.0.0.1:5000/authenticate'
    data = {
        'TenTaiKhoan': TenTaiKhoan,
        'MatKhau': MatKhau
    }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Đăng nhập thành công!")
    elif response.status_code == 401:
        print("Tên tài khoản hoặc mật khẩu không đúng.")
    else:
        print("Lỗi:", response.status_code)


if __name__ == '__main__':
    app.run(debug=True)
