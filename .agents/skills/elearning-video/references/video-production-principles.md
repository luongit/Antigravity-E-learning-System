# Quy Chuẩn Sản Xuất Video E-Learning Chung (Video Production Principles)

Tệp này quy định các nguyên tắc mỹ thuật, bố cục, khoảng cách, đồng bộ giọng đọc và trám cảnh B-roll bắt buộc áp dụng cho **TẤT CẢ CÁC ENGINE VIDEO** (`elearning-opencv-video`, `elearning-hyperframes-video`, v.v.).

Bất kể Agent sử dụng engine nào để tạo/render video bài giảng, **BẮT BUỘC** phải tuân thủ nghiêm ngặt toàn bộ các quy chuẩn dưới đây.

---

## 1. Quy Chuẩn Phân Cấp Cỡ Chữ (Typography Hierarchy)

Áp dụng cho mọi slide, cảnh hoạt họa (HTML/SVG hoặc Canvas) trên độ phân giải chuẩn **16:9 ($1920\times 1080$)**:

* **Tiêu đề chính (Slide Title / H1, H2):** **$36\text{px} – 42\text{px}$** (đậm, nổi bật, cố định ở góc trên bên trái, không đổi vị trí giữa các cảnh).
* **Tiêu đề phụ / Tiêu đề khối thẻ (Card Headings / H3, H4):** **$24\text{px} – 32\text{px}$** (đậm, phân cấp rõ ràng với nội dung chi tiết).
* **Nội dung văn bản (Body text / Danh sách / Tính năng):** **$16\text{px} – 18\text{px}$** (dễ đọc, sắc nét, không dùng font quá mỏng).
* **Chú thích nhỏ / Metadata / Tác giả:** Tối thiểu **$14\text{px}$**.
* **Phụ đề đáy màn hình (Bottom Subtitles):**
  * Kích thước lớn: **$44\text{px} – 48\text{px}$**.
  * Font chữ: **Be Vietnam Pro ExtraBold** (hoặc Black) hiển thị tiếng Việt chuẩn xác.
  * **Tuyệt đối KHÔNG có viền đen stroke lem luốc** (`-webkit-text-stroke: none`). Thay vào đó dùng dải phủ mờ gradient đáy (`linear-gradient(to top, rgba(0,0,0,0.85), transparent)`) hoặc `drop-shadow(0 2px 8px rgba(0,0,0,0.7))` để chữ nổi bật trên mọi nền video/slide.
  * Phân đoạn ngắn gọn: 6–8 từ mỗi dòng để người học nắm bắt kịp theo nhịp giọng nói.

---

## 2. Quy Chuẩn Bố Cục Khoảng Cách & Căn Chỉnh Trục Dọc (Spacing & Natural Vertical Centering)

* **Khoảng cách giữa các phần tử (Element Gap):**
  * Nghiêm ngặt từ **$15\text{px} – 30\text{px}$** (chuẩn tối ưu thiết kế là `gap: 18px` đến `24px`).
* **Triệt tiêu khoảng cách rỗng thị giác:**
  * **Cấm kỵ tuyệt đối:** KHÔNG dùng `justify-content: space-between` trên container để kéo dãn các khối dạt ra hai mép trên/dưới khi nội dung ít, gây loãng mắt và đứt gãy thị giác.
* **Căn giữa dọc tự nhiên (Natural Vertical Centering):**
  * Khi slide có ít nội dung (chỉ có 2–3 thẻ hoặc 1 khối sơ đồ ngắn), vùng nội dung bên dưới tiêu đề phải được **căn giữa tự nhiên theo chiều dọc** (`margin: auto 0` hoặc flexbox `justify-content: center` theo trục dọc).
  * Các khối thẻ card chỉ cần **ôm vừa vặn nội dung** với đệm bên trong `padding: 24px–32px`, không kéo dãn cưỡng bức chiều cao $100\%$ làm xuất hiện các khoảng trống vô nghĩa bên trong thẻ.

---

## 3. Quy Chuẩn Trám Cảnh Video Minh Họa Ngữ Nghĩa & Thời Lượng Động (Semantic & Dynamic B-roll Cutaway)

* **Bản chất & Mục đích:**
  * Video minh họa được chèn **Toàn Màn Hình 16:9 ($1920\times 1080$)** cắt ngang dòng thời gian (Full Cutaway) để làm sinh động lời giảng, minh họa thế giới thực và xóa bỏ cảm giác nhàm chán của slide tĩnh.
  * **Tuyệt đối KHÔNG dùng khung nhỏ PiP nổi ở góc màn hình.**
* **Phân biệt thời điểm: Khi nào hiện Slide và Khi nào Trám cảnh?**
  * **Hiển thị Slide:** Khi lời giảng tập trung trực tiếp vào nội dung bài học, đọc tiêu đề bài, hoặc phân tích chi tiết từng gạch đầu dòng/khối thẻ trên slide (áp dụng nghiêm ngặt nguyên tắc **SRT Lockstep: Nói đến đâu hiện đến đó**).
  * **Trám cảnh Minh họa:** Khi lời giảng **thoát ly khỏi các gạch đầu dòng trên slide** để mở rộng liên hệ thực tế, chia sẻ bối cảnh thực trạng ngoài đời, kể câu chuyện doanh nghiệp, đặt vấn đề định hướng, hoặc đúc kết ứng dụng thực tiễn.
* **Thời lượng trám linh hoạt theo ngữ nghĩa (Dynamic Duration):**
  * **Tuyệt đối KHÔNG cố định 4–6 giây.** Thời lượng trám cảnh được xác định chính xác theo độ dài của đoạn lời giảng ngoại cảnh trong file SRT (có thể là 4s, 8s, 12s, 15s hoặc lâu hơn tùy ý đồ sư phạm).
  * Ngay khi lời giảng quay trở lại phân tích nội dung chính của slide, video lập tức chuyển mượt mà (crossfade/cut) về lại slide để tiếp tục hiển thị nội dung học tập.
* **Cơ chế Ghép Nối Đa Clip (Multi-Clip Chaining):**
  * Khi một đoạn giải thích ngoại cảnh kéo dài (ví dụ 10s–16s) mà một clip trong thư viện không đủ dài, hoặc để tránh việc người học nhìn mãi một góc quay tĩnh gây buồn ngủ: Agent **bắt buộc ghép nối liên tiếp 2 đến 3 đoạn video clip khác nhau** (mỗi clip 4–7s) cùng chủ đề để bao trọn thời lượng của đoạn thuyết minh đó như một thước phim phóng sự tài liệu chuyên nghiệp.
* **Lựa chọn nội dung video theo ngữ nghĩa (Content-Aware Matching):**
  * Agent phân tích chính xác chủ đề của đoạn lời giảng đang nói (nói về nhân sự/văn phòng $\to$ clip văn phòng; nói về robot/tự động hóa $\to$ clip AI robotics; nói về máy chủ/hạ tầng/code $\to$ clip máy tính/lập trình; nói về thị trường/kinh doanh $\to$ clip doanh nghiệp...).
* **Hỗ trợ nhiều đợt trám cảnh trong cùng 1 cảnh (Multiple Cutaways per Scene):**
  * Một cảnh có thể có nhiều đợt trám cảnh xen kẽ (ví dụ: Đầu cảnh mở bài $\to$ Trình bày ý 1 $\to$ Trám cảnh thực tế 12s giữa chừng $\to$ Trình bày tiếp ý 2 $\to$ Trám cảnh đúc kết trước khi kết thúc).
* **Lớp hiển thị bảo đảm thông tin:**
  * Phụ đề đáy (`z-index: 1000`) và nhãn phân loại/trạng thái (`z-index: 600`) luôn hiển thị sắc nét trên nền video trám cảnh qua dải gradient tối mờ.
* **Áp dụng đồng bộ cho TẤT CẢ ENGINE (OpenCV, HyperFrames v.v.):**
  * **OpenCV:** Khi đến thời điểm cutaway, tự động chuyển sang đọc frame từ video B-roll (`cv2.VideoCapture`), phủ scrim tối và hiển thị phụ đề chữ trắng tương phản; hết cutaway quay lại ảnh bảng trắng Canny.
  * **HyperFrames:** Điều khiển `<video>` toàn màn hình hoặc crossfade timeline GSAP mượt mà qua `broll_controller.js`.

---

## 4. Quy Chuẩn Đồng Bộ Khớp Giọng Đọc Tuyệt Đối (SRT Lockstep Synchronization)

* **Nguyên tắc tối cao "Nói đến đâu – Hiện đến đó":**
  * Từng bullet point, thẻ card, icon hay sơ đồ thành phần chỉ được xuất hiện chính xác tại giây mà giọng đọc trong file SRT bắt đầu nhắc đến từ khóa đó.
* **Cấm kỵ hiện sớm:**
  * Tuyệt đối KHÔNG để toàn bộ nội dung xuất hiện sẵn trước 3–5 giây so với lời giảng, làm phân tán sự chú ý của người học.
* **Hiệu ứng xuất hiện:**
  * Nhẹ nhàng, tinh tế (fade-in, slide-up 10–20px hoặc spring animation), thời gian chuyển động từ $0.4\text{s} – 0.6\text{s}$.

---

## 5. Hệ Thống Giao Diện Mẫu (Theme Presets)

Mọi cảnh dựng bằng HyperFrames đều hỗ trợ áp dụng bảng màu và phong cách chuẩn:

1. `light-whiteboard`: Nền trắng sáng `#FFFFFF` / `#F8FAFC`, thẻ viền nhẹ, chữ đen xám `#0F172A`, phụ đề đen chữ nổi hoặc nền kính mờ.
2. `dark-modern`: Nền tối xanh than `#0B0F19`, thẻ glassmorphism `#1E293B` bán trong suốt, chữ trắng `#F8FAFC`, phụ đề trắng gradient.
3. `ai-tech-neon`: Nền đen sâu `#050811`, viền neon xanh cyan `#06B6D4` hoặc tím `#8B5CF6`, hiệu ứng công nghệ trí tuệ nhân tạo.
4. `flat-editorial`: Nền giấy xám ấm `#F4F4F0`, typography cổ điển sang trọng, viền kẻ nét đơn tối giản chuẩn phong cách báo chí học thuật.

---

## 6. Quy Chuẩn Bố Cục Kết Hợp Mỏ Neo Thị Giác Khi Ít Nội Dung (Visual Anchor Layout Archetypes)

Khi một slide có lượng nội dung ít (chỉ có 2–3 thẻ hoặc gạch đầu dòng ngắn), việc dàn trải chỉ có chữ trên toàn màn hình sẽ gây cảm giác **đơn điệu, thô sơ và trống trải**. Agent **BẮT BUỘC** áp dụng 1 trong 4 mẫu bố cục kết hợp **Mỏ neo thị giác (Visual Anchor)**:

1. **Mẫu 1: Mỏ neo Trái — Nội dung Phải (`split-left`):**
   - Bên trái chiếm 35%–45% chiều rộng: Hiển thị hình ảnh minh họa chủ đạo (vector SVG hoặc ảnh từ `inputs/image-libraries/`).
   - Bên phải: Tiêu đề và các khối thẻ nội dung xuất hiện theo nhịp giọng đọc.
2. **Mẫu 2: Nội dung Trái — Mỏ neo Phải (`split-right`):**
   - Bên trái: Tiêu đề và các khối thẻ phân tích.
   - Bên phải: Sơ đồ kỹ thuật, icon nổi bật hoặc hình ảnh minh họa lớn.
3. **Mẫu 3: Mỏ neo Trung Tâm — Nội dung Tỏa Ra (`center-anchor` / Orbit):**
   - Trung tâm màn hình: Hình ảnh/biểu tượng mỏ neo cốt lõi (ví dụ: Logo BUNI, Lõi AI, Quả địa cầu kết nối).
   - Hai bên (hoặc 3–4 hướng): Các khối thẻ tính năng đối xứng kết nối về tâm điểm.
4. **Mẫu 4: Khối Trọng Tâm Giữa — Phụ Trợ Bốn Góc (`center-stage-grid`):**
   - Nội dung quan trọng nằm chính giữa, các biểu tượng/họa tiết vector trang trí cân đối ở các góc màn hình.

* **Quy chuẩn nguồn tài nguyên Mỏ neo thị giác:**
  * **Thư viện sẵn có:** Kiểm tra trước trong `inputs/image-libraries/` xem có ảnh/icon phù hợp không.
  * **Tự sinh Vector SVG:** Nếu chưa có sẵn ảnh trong thư viện, Agent tự động thiết kế hình vẽ phẳng vector SVG tinh tế, sắc nét (sinh viên công nghệ, chip AI vi xử lý, sơ đồ mạng lưới doanh nghiệp, quả địa cầu số...).

---

## 7. Chuẩn Hóa Phát Âm Giọng Đọc TTS & Ngôn Ngữ

* **Chuẩn hóa phát âm thuật ngữ IT:**
  * Toàn bộ từ viết tắt/thuật ngữ tiếng Anh (React, Docker, Microservices, Spring Boot, API, Redis, Kafka, Flutter, CI/CD...) phải được chuyển đổi qua bộ từ điển phiên âm tiếng Việt (trong `core/vietnamese_pronunciation.py` và `README.md`) trước khi tổng hợp giọng đọc Edge-TTS để đọc chuẩn âm tiết tiếng Việt.
* **Giọng đọc chuẩn:** Mặc định `vi-VN-NamMinhNeural` (hoặc `vi-VN-HoaiMyNeural`), tốc độ `-5%` đến `-8%` trầm ấm, từ tốn, đúng chuẩn sư phạm.
* **Văn phong tích cực 100%:** Luôn tôn vinh giải pháp, tính thực tiễn và cơ hội nghề nghiệp. Tuyệt đối không chỉ trích, chê bai chương trình đào tạo khác.
* **100% Tiếng Việt có dấu:** Mọi chuỗi ký tự hiển thị trên slide và phụ đề phải là tiếng Việt có dấu chuẩn xác.
