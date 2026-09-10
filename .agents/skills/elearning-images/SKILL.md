---
name: elearning-images
description: Giai đoạn 2 - Tạo Ảnh Bài Giảng: Thiết kế Prompt Infographic 16:9 chuẩn Tiếng Việt 100%, font Be Vietnam Pro, cấm tuyệt đối vẽ tay người / bút vẽ trên ảnh; xuất các file prompt-X.txt và hỗ trợ tự động hóa sinh ảnh slide qua Browser Subagent (Google Flow) hoặc công cụ sinh ảnh. Dùng khi người dùng yêu cầu tạo prompt hoặc tạo ảnh slide.
---

# E-Learning Stage 2: Tạo Ảnh Slide Infographic Bài Giảng

## 1. Vai trò & Mục tiêu
Chuyên trách toàn diện **Giai đoạn Tạo ảnh**: Chuyển đổi kịch bản slide thành các câu lệnh thiết kế (Design Prompts) 16:9 hoàn chỉnh, sau đó tự động hóa quá trình sinh ảnh slide Infographic phẳng 2D chất lượng cao (1920x1080) sẵn sàng đưa vào slide bài giảng và video whiteboard.

- **Thư mục đầu vào:** `output/<ma-mon-hoc>/script.md` hoặc `output/<ma-mon-hoc>/video-<x>/script.md` (hoặc mô tả nội dung slide từ người dùng).
- **Thư mục đầu ra:**
  - File Prompts: `output/<ma-mon-hoc>/video-<x>/prompts/prompt-X.txt`
  - File Ảnh slide: `output/<ma-mon-hoc>/video-<x>/images/slide-X.png` (hoặc `.jpeg`)

---

## 2. Quy Chuẩn Thiết Kế Prompt Bắt Buộc

Mỗi câu prompt là một **lệnh thiết kế toàn diện cho một slide Infographic hoàn chỉnh**, bắt buộc tuân thủ 6 nguyên tắc bất biến:

### 1. Tỷ lệ & Màu nền
- **Tỷ lệ 16:9 chuẩn màn hình trình chiếu** (1920x1080).
- **Nền trắng tinh khiết (#FFFFFF)**, sạch sẽ, không có viền lề thừa, không dùng hoa văn chìm gây nhiễu khi render hoạt ảnh whiteboard.

### 2. Font chữ & Ngôn ngữ (Quy tắc cưỡng chế 100% Tiếng Việt có dấu)
- **Lệnh ngôn ngữ tối cao bắt buộc ở đầu MỌI Prompt:**
  Mọi câu prompt tạo ảnh BẮT BUỘC phải mở đầu bằng đúng đoạn lệnh sau:
  > `[YÊU CẦU NGÔN NGỮ TỐI CAO: Toàn bộ chữ hiển thị trên ảnh BẮT BUỘC 100% LÀ TIẾNG VIỆT CÓ DẤU CHÍNH XÁC. TUYỆT ĐỐI KHÔNG CÓ CHỮ TIẾNG ANH, TỪ NGỮ TIẾNG ANH HAY KÝ TỰ VÔ NGHĨA. ALL TEXT IN IMAGE MUST BE VIETNAMESE ONLY, STRICTLY NO ENGLISH WORDS, NO GIBBERISH LETTERS.]`
- **Font chữ:** Nhấn mạnh ngay sau lệnh ngôn ngữ: `"Font chữ Be Vietnam Pro in đậm sắc nét xuyên suốt toàn bộ slide"`.
- **Chỉ định chuỗi ký tự chính xác:** Toàn bộ tiêu đề, nhãn thẻ, dòng chữ hiển thị trên ảnh BẮT BUỘC được liệt kê rõ ràng trong dấu ngoặc kép `"..."`. Tuyệt đối không mô tả chung chung để tránh AI tự suy diễn chữ sang tiếng Anh hoặc sinh ra chữ vô nghĩa (gibberish).
- **Tuyệt đối KHÔNG có chữ tiếng Anh trên ảnh:** Kể cả các thuật ngữ kỹ thuật (như Start $\to$ Bắt đầu, End $\to$ Kết thúc, Decision $\to$ Rẽ nhánh, Input $\to$ Nhập liệu, Process $\to$ Xử lý, Output $\to$ Đầu ra, Flowchart $\to$ Sơ đồ luồng, Module $\to$ Mô-đun).

### 3. Phong cách Đồ họa
- **Minh họa vector nét vẽ phẳng 2D (Flat 2D Vector Illustration)**, đường nét thanh thoát, rõ ràng.
- **Bảng màu:** Tối giản và hài hòa, sử dụng nền trắng với 1–2 màu nhấn chủ đạo (như Xanh dương Navy/Teal kết hợp Cam/Vàng ấm).
- **Tuyệt đối KHÔNG dùng:** 3D realism, isometric phức tạp, đổ bóng quá gắt hoặc hoạt hình trẻ con lòe loẹt.

### 4. Bố cục Không gian
- Phân định rõ các vùng không gian: Trái / Phải hoặc Trên / Dưới.
- Luôn tạo **Mỏ neo thị giác (Visual Anchor)**: Một hình minh họa lớn ở một bên, bên còn lại là tiêu đề và các khối nội dung xếp lớp rõ ràng.
- Đảm bảo khoảng trắng thoáng đãng giữa các khối để phục vụ bóc tách hoạt ảnh chuyển động.

### 5. ĐIỀU CẤM KỴ TUYỆT ĐỐI & NEGATIVE PROMPT (Chốt chặn cuối mỗi Prompt)
Bắt buộc gắn toàn bộ đoạn ràng buộc sau vào cuối MỌI prompt tạo ảnh:
> `[ĐIỀU CẤM KỴ TUYỆT ĐỐI & NEGATIVE PROMPT: Không có chữ tiếng Anh, không có từ tiếng Anh, không có chữ cái Latin vô nghĩa. Cấm vẽ bàn tay người, cánh tay, ngón tay, bút vẽ, bút chì, bút lông. Negative prompt: English text, English words, Latin gibberish, foreign language, misspelled English words, human hands, human arms, fingers, pens, markers, pencils, realistic 3D, blur, watermark]`  
*(Lý do: Vừa triệt tiêu chữ tiếng Anh ngẫu nhiên do AI sinh ra, vừa ngăn vẽ tay/bút để phần mềm video tự render hoạt họa).*

---

## 3. Quy Trình Sản Xuất & Tự Động Hóa Sinh Ảnh

### Bước 1: Xuất file Prompt độc lập
Lưu từng prompt thành file text riêng biệt:  
`output/<ma-mon-hoc>/video-<x>/prompts/prompt-1.txt`, `prompt-2.txt`...  
Điều này giúp việc tự động hóa đọc tệp tin cậy, không bị chặn bởi bảo mật clipboard.

### Bước 2: Tự động hóa qua Browser Subagent (Google Flow)
Khi người dùng yêu cầu "Tạo ảnh", Agent kích hoạt `browser_subagent` thực hiện:
1. Truy cập `https://flow.google.com/`.
2. Tạo dự án mới đặt tên theo tên Video.
3. **Chiến lược Fire-and-Forget (Gửi nhanh, không chờ):**
   - Đọc nội dung từng `prompt-X.txt`.
   - Dán vào ô nhập lệnh $\to$ Bấm Tạo (Generate).
   - **Chờ đúng 3 giây** rồi chuyển ngay sang slide tiếp theo, **không chờ render xong**.
   - Google Flow sẽ tự quản lý hàng đợi render trên máy chủ.
4. Thông báo người dùng tải ảnh hoàn thiện và lưu vào:  
   `output/<ma-mon-hoc>/video-<x>/images/slide-1.png`, `slide-2.png`...
