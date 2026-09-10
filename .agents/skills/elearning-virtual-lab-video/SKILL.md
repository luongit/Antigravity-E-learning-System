---
name: elearning-virtual-lab-video
description: Giai đoạn 5 - Render video E-Learning và mô phỏng trực quan Phòng Thí Nghiệm Ảo Khoa học Tự nhiên & STEM (Quang học Ray Optics, Mạch điện DC & RC, Sóng cơ học & Dao động, Điện trường Coulomb và Cơ học 2D) bằng các thư viện mở MIT & Apache-2.0.
---

# E-Learning Stage 5 — Virtual Lab: Mô Phỏng Thí Nghiệm Ảo Khoa Học Tự Nhiên & STEM

Kỹ năng này chuyên dùng để tạo video bài giảng, hình ảnh slide Infographic 16:9 và trang HTML tương tác cho các bài học Khoa học Tự nhiên, Vật lý và Kỹ thuật STEM bằng hệ thống **Virtual Lab tự chủ**, sạch 100% về bản quyền thương mại (cấp phép MIT & Apache-2.0, không phụ thuộc PhET).

---

## 1. Vai Trò & Năng Lực Điều Phối

Virtual Lab không dùng một framework duy nhất mà điều phối đa thư viện mở chuyên biệt theo ngôn ngữ tự nhiên:

1. **Quang học (Ray Optics — Apache-2.0):**
   - Khảo sát tia sáng, định luật khúc xạ ánh sáng (Định luật Snell $n_1 \sin\theta_1 = n_2 \sin\theta_2$).
   - Định luật phản xạ và góc tới hạn phản xạ toàn phần $\theta_c = \arcsin(n_2/n_1)$.
   - Thấu kính mỏng (hội tụ, phân kỳ, tiêu cự $f$, ảnh thật / ảnh ảo), gương phẳng, lăng kính.
   - Thước đo góc tròn Protractor 360° đo trực tiếp tia tới và tia khúc xạ.
2. **Cơ học 2D (Matter.js — MIT):**
   - Rơi tự do, ném ngang, ném xiên trong trọng trường.
   - Va chạm đàn hồi và va chạm mềm 1D/2D (bảo toàn động lượng).
   - Ma sát, mặt phẳng nghiêng, con lắc đơn, con lắc lò xo, hệ ròng rọc.
3. **Mạch điện & Điện tử (Circuit Lab — MIT):**
   - Khảo sát Định luật Ohm: $I = U/R$, công suất $P = UI$.
   - Đoạn mạch mắc nối tiếp và song song.
   - Mạch nạp & xả tụ điện RC, quan sát điện áp hàm mũ thời gian thực.
   - Đồng hồ Vôn kế, Ampe kế và dòng electron chuyển động trực quan.
4. **Sóng & Dao động (Waves — MIT):**
   - Sóng hình sin truyền trên sợi dây đàn hồi: $u(x,t) = A\sin(\omega t - kx)$.
   - Khảo sát bước sóng $\lambda$, tần số $f$, chu kỳ $T$, vận tốc truyền pha $v = \lambda f$.
   - Sóng dừng với các nút sóng (nodes) và bụng sóng (antinodes), phản xạ đầu cố định/tự do.
   - Giao thoa 2 nguồn sóng kết hợp.
5. **Điện trường tĩnh (Electric Fields — MIT):**
   - Tương tác điện tích điểm tĩnh điện theo định luật Coulomb.
   - Lưới véc-tơ cường độ điện trường $\vec{E}$ và họ đường sức điện liên tục.

---

## 2. Quy Trình Sản Xuất Video & Slide Bài Giảng

### Bước 1: Tiếp nhận yêu cầu bằng ngôn ngữ tự nhiên
Người dùng không cần chỉ định tên thư viện, chỉ cần ra lệnh tự nhiên:
- *"Minh họa định luật khúc xạ ánh sáng Snell từ không khí vào nước"*
- *"Xây dựng mô phỏng mạch điện nối tiếp khảo sát định luật Ohm"*
- *"Mô phỏng sóng cơ học trên sợi dây và bước sóng"*
- *"Trực quan hóa đường sức điện trường của 2 điện tích trái dấu"*
- *"Khảo sát chuyển động ném xiên với góc 45 độ và vận tốc đầu 24m/s"*

### Bước 2: Tự động biên dịch cấu hình và HTML
```powershell
python -c "from core.virtual_lab_engine import VirtualLabEngine; lab = VirtualLabEngine('output/<ma-mon-hoc>/video-<x>'); cfg = lab.dispatch_experiment('khúc xạ ánh sáng'); lab.generate_html(cfg)"
```

### Bước 3: Chụp ảnh slide 16:9 ($1920\times 1080$)
```powershell
python engines/virtual_lab/render.py "output/<ma-mon-hoc>/video-<x>" --query "khúc xạ ánh sáng" --mode still
```

### Bước 4: Đóng gói PowerPoint (.pptx) và PDF 16:9
```powershell
python engines/virtual_lab/export_slides.py "output/<ma-mon-hoc>/video-<x>" --query "khúc xạ ánh sáng" --name "slides_quang_hoc"
```

### Bước 5: Render Video Full HD 1080p 30fps
```powershell
python engines/virtual_lab/render.py "output/<ma-mon-hoc>/video-<x>" --query "khúc xạ ánh sáng" --mode video --duration 10.0
```

---

## 3. Quy Chuẩn Xuất Bản
- **Độ phân giải:** $1920\times 1080$ Full HD, 30fps / 60fps.
- **Tiêu chuẩn bản quyền:** 100% Permissive Open Source (MIT / Apache-2.0), sẵn sàng thương mại hóa và chuyển giao doanh nghiệp.
- **Tính năng sư phạm:** Bảng đo lường Telemetry HUD hiển thị công thức định luật, thông số đại lượng đo lường thời gian thực.
