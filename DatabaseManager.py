import requests


class DataFetcher:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return None


class NhanVien:
    def __init__(self, data):
        self.HinhAnh = data.get("HinhAnh", "None")
        self.MaNhanVien = data.get("MaNhanVien")
        self.SoDienThoai = data.get("SoDienThoai")
        self.TenNhanVien = data.get("TenNhanVien")
        self.TrangThai = data.get("TrangThai")
        self.Tuoi = data.get("Tuoi")


class NhomQuyen:
    def __init__(self, data):
        self.MaNhomQuyen = data.get("MaNhomQuyen")
        self.TenNhomQuyen = data.get("TenNhomQuyen")
        self.TrangThai = data.get("TrangThai")


class TaiKhoan:
    def __init__(self, data):
        self.MaNhomQuyen = data.get("MaNhomQuyen")
        self.MaTaiKhoan = data.get("MaTaiKhoan")
        self.MatKhau = data.get("MatKhau")
        self.TenTaiKhoan = data.get("TenTaiKhoan")
        self.TrangThai = data.get("TrangThai")


def retrieve_data(url):
    data_fetcher = DataFetcher(url)
    data = data_fetcher.fetch_data()

    tai_khoan_list = []
    nhom_quyen_list = []
    nhan_vien_list = []

    if data:
        # Lấy danh sách tài khoản
        tai_khoan_data = data.get("TaiKhoan", [])[1:]
        for tk_data in tai_khoan_data:
            tai_khoan_list.append(TaiKhoan(tk_data))

        # Lấy danh sách nhóm quyền
        nhom_quyen_data = data.get("NhomQuyen", [])[1:]
        for nq_data in nhom_quyen_data:
            nhom_quyen_list.append(NhomQuyen(nq_data))

        # Lấy danh sách nhân viên
        nhan_vien_data = data.get("NhanVien", [])[1:]
        for nv_data in nhan_vien_data:
            nhan_vien_list.append(NhanVien(nv_data))

    return tai_khoan_list, nhom_quyen_list, nhan_vien_list


def authenticate(TenTaiKhoan, MatKhau, danh_sach_tai_khoan):
    # Kiểm tra xem có dữ liệu đầy đủ không
    if not TenTaiKhoan or not MatKhau:
        print("Tên tài khoản và mật khẩu không được để trống.")
        return False

    # Chống khả năng hack vào database
    if "'" in TenTaiKhoan or "'" in MatKhau:
        print("Tên tài khoản và mật khẩu không hợp lệ.")
        return False

    # Kiểm tra xem có khớp với danh sách tài khoản hay không
    for tai_khoan in danh_sach_tai_khoan:
        if tai_khoan.TenTaiKhoan == TenTaiKhoan:
            if str(tai_khoan.MatKhau) == MatKhau:
                return True

    return False


# Sử dụng hàm retrieve_data
url = "https://waifu-run-7683a-default-rtdb.firebaseio.com/DB.json?print=pretty"
tai_khoan_list, nhom_quyen_list, nhan_vien_list = retrieve_data(url)
print(tai_khoan_list[0].TenTaiKhoan)
print(tai_khoan_list[0].MatKhau)
print(authenticate("Admin", "1234", tai_khoan_list))
