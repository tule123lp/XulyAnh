import cv2
import numpy as np
import sys  # Thư viện này để kiểm tra hệ thống

def print_welcome():
    """In ra thông báo chào mừng (không dấu)"""
    print("--- CHUONG TRINH LOC ANH DSP (Tuy chinh) ---")
    print("Ban se duoc yeu cau nhap 3 thu:")
    print("  1. Ten file anh (dat chung thu muc voi file code nay).")
    print("  2. Cap do mo (mot so LE nhu 3, 5, 9... So cang lon, cang mo).")
    print("  3. Cap do net (nhap 1 hoac 2).\n")

# --- HÀM NÀY KHÔNG CÒN KERNEL CỐ ĐỊNH ---
# Chúng ta sẽ tạo kernel bên trong hàm main()


# --- 2. Hàm chính để xử lý ---
def main():
    
    print_welcome()
    
    # === PHẦN 1: NHẬP LIỆU TỪ NGƯỜI DÙNG ===

    # --- 1a: Nhập tên file ảnh ---
    image_path = input("Buoc 1: Vui long nhap ten file anh (vi du: 'hinh_test.jpg'): ")

    # --- 1b: Nhập độ mờ ---
    try:
        blur_level_str = input("Buoc 2: Nhap cap do mo (mot so LE > 1, vi du: 5, 9, 15): ")
        blur_k = int(blur_level_str) # Chuyển chuỗi sang số
        
        # Kiểm tra điều kiện
        if blur_k <= 1 or blur_k % 2 == 0:
            print(f"LOI: Cap do mo '{blur_k}' khong phai la so LE hoac khong lon hon 1.")
            print("Vui long chay lai chuong trinh.")
            input("Nhan Enter de thoat...")
            sys.exit()

    except ValueError:
        # Bẫy lỗi nếu người dùng nhập chữ thay vì số
        print("LOI: Ban da nhap chu, khong phai so. Vui long chay lai.")
        input("Nhan Enter de thoat...")
        sys.exit()

    # --- 1c: Nhập độ nét ---
    try:
        sharp_level_str = input("Buoc 3: Nhap cap do net (chon 1=Net vua, 2=Net hon): ")
        sharp_k = int(sharp_level_str) # Chuyển chuỗi sang số
        
        # Kiểm tra điều kiện
        if sharp_k != 1 and sharp_k != 2:
            print("LOI: Chi duoc phep nhap 1 hoac 2.")
            print("Vui long chay lai chuong trinh.")
            input("Nhan Enter de thoat...")
            sys.exit()
            
    except ValueError:
        print("LOI: Ban da nhap chu, khong phai so. Vui long chay lai.")
        input("Nhan Enter de thoat...")
        sys.exit()

    print("\n--- Da nhan du thong tin. Bat dau xu ly ---")


    # === PHẦN 2: TẠO KERNEL DỰA TRÊN INPUT ===

    # --- 2a: Tạo Kernel Mờ (Dynamically) ---
    # Kernel size la blur_k (ví dụ: 9)
    # So luong phan tu la blur_k * blur_k (ví dụ: 81)
    kernel_blur = np.ones((blur_k, blur_k), np.float32) / (blur_k * blur_k)
    print(f"Da tao bo loc mo KICH THUOC {blur_k}x{blur_k}.")

    # --- 2b: Tạo Kernel Nét (Based on choice) ---
    if sharp_k == 1:
        kernel_sharpen = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], np.float32)
        print("Da chon bo loc net 'Net vua'.")
    else: # sharp_k == 2
        kernel_sharpen = np.array([
            [-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]
        ], np.float32)
        print("Da chon bo loc net 'Net hon'.")
        

    # === PHẦN 3: ĐỌC ẢNH VÀ ÁP DỤNG BỘ LỌC ===

    # --- 3a: Đọc ảnh ---
    try:
        print(f"Dang tim va doc file: {image_path}...")
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"LOI: Khong the doc anh tu duong dan: {image_path}")
            print("Vui long kiem tra lai ten file.")
            input("Nhan Enter de thoat...")
            sys.exit() 

    except Exception as e:
        print(f"Da xay ra loi khong xac dinh khi doc file: {e}")
        input("Nhan Enter de thoat...")
        sys.exit()

    print(f"Da tai anh '{image_path}' thanh cong.")

    # --- 3b: Áp dụng các bộ lọc (Tích chập 2D) ---
    print("Dang ap dung bo loc lam mo (LPF)...")
    print("Dang ap dung bo loc lam net (HPF)...")
    
    blurred_image = cv2.filter2D(image, -1, kernel_blur)
    sharpened_image = cv2.filter2D(image, -1, kernel_sharpen)
    
    print("Da xu ly xong!")
    print("Nhan phim bat ky tren CUA SO ANH de dong tat ca...")
    
    # --- 3c: Hiển thị kết quả ---
    cv2.imshow('1. Anh Goc', image)
    cv2.imshow(f'2. Anh Lam Mo (Cap do {blur_k})', blurred_image)
    cv2.imshow(f'3. Anh Lam Net (Cap do {sharp_k})', sharpened_image)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("Da dong cua so. Ket thuc chuong trinh.")

# --- Chạy hàm main() khi file được thực thi ---
if __name__ == "__main__":
    main()