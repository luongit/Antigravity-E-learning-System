# HyperFrames JSON Scene Specification v2 (Agent-Friendly Spec)

Tài liệu quy chuẩn cấu trúc dữ liệu JSON Scene Spec v2 cho **HyperFrames Engine**.
Thiết kế theo chuẩn **Declarative JSON Spec** giúp AI Agent dễ dàng lập kế hoạch, sinh kịch bản và điều phối render mà không cần viết mã lệnh giao diện phức tạp.

---

## 1. Cấu Trúc Tổng Quan (Root Schema)

```json
{
  "schema": "hyperframes-scene-v2",
  "meta": {
    "title": "Tên Bài Giảng",
    "fps": 30,
    "width": 1920,
    "height": 1080,
    "theme": "dark-modern"
  },
  "settings": {
    "bgColor": "#0F172A",
    "accentColor": "#38BDF8",
    "fontFamily": "'Be Vietnam Pro', sans-serif"
  },
  "globalAudio": [
    { "type": "narration", "src": "mp3/mp3-1.mp3", "srt": "mp3/mp3-1.srt", "volume": 1.0 },
    { "type": "bgm", "src": "assets/audio/bg-lofi-tech.mp3", "volume": 0.12, "loop": true }
  ],
  "scenes": [
    {
      "id": "sc1",
      "duration": 48.5,
      "layout": "cards-grid",
      "title": "TIÊU ĐỀ SLIDE CHÍNH",
      "badge": "Phân mục / Chuyên đề",
      "slideNumber": 1,
      "visualAnchor": {
        "type": "buni-ecosystem",
        "size": 460,
        "accentColor": "#38BDF8"
      },
      "elements": [],
      "cutaways": []
    }
  ]
}
```

---

## 2. Bảng Phân Loại Theme & Layout

### 2.1 Theme Presets
- `dark-modern`: Nền xanh than đậm `#0F172A`, text trắng sáng `#F8FAFC`, card glassmorphism. Phù hợp CNTT, AI, Khoa học Kỹ thuật.
- `light-whiteboard`: Nền trắng ngà `#F8FAFC`, text đen `#0F172A`, nét vẽ chuẩn sư phạm, card viền mỏng.
- `ai-tech-neon`: Nền đen sâu `#050814`, viền phát sáng cyan/purple, gradient công nghệ cao.
- `flat-editorial`: Nền trung tính trang nhã, màu pastel báo chí chuyên sâu.

### 2.2 Layout Presets
- `cards-grid`: Lưới thẻ nội dung (2-3 cột) kết hợp biểu tượng minh họa lớn (Visual Anchor) ở bên phải hoặc trung tâm.
- `split-left`: Cột trái là Visual Anchor / Trực quan hóa, cột phải là các thẻ nội dung chi tiết.
- `split-right`: Cột trái là danh sách thẻ hoặc tiêu điểm, cột phải là Code Studio / Mô phỏng.
- `center-anchor`: Visual Anchor ở trung tâm, nội dung xoay quanh theo quỹ đạo.

---

## 3. Danh Sách Phần Tử Nội Dung (`elements`)

### 3.1 Card Element (`type: "card"`)
```json
{
  "id": "card-1",
  "type": "card",
  "content": {
    "tag": "BẢN QUYỀN ĐÀO TẠO",
    "title": "Mô Hình: 'Làm Trước Học Sau'",
    "desc": "Kế thừa bản quyền số 7190/2021/QTG của Bachkhoa Aptech.",
    "icon": "📌"
  },
  "style": {
    "accentColor": "#FF7043"
  },
  "animation": {
    "preset": "springUp",
    "appearSec": 8.5
  }
}
```

### 3.2 Code Studio Element (`type: "code"`)
```json
{
  "id": "code-1",
  "type": "code",
  "language": "python",
  "filename": "pipeline.py",
  "content": "def run_pipeline():\n    engine = HFEngine()\n    return engine.render()",
  "animation": {
    "preset": "typewriter",
    "delay": 1.5,
    "charDuration": 4.0
  }
}
```

### 3.3 Text Element (`type: "text"`)
```json
{
  "id": "text-heading",
  "type": "text",
  "content": "Tổng kết lộ trình 4 cấp độ dự án",
  "style": {
    "fontSize": 38,
    "fontWeight": 800,
    "color": "#F8FAFC"
  },
  "animation": {
    "preset": "fadeInDown",
    "delay": 0.5,
    "duration": 0.6
  }
}
```

---

## 4. Visual Anchors Đồ Họa 2D/SVG (`visualAnchor`)

Hỗ trợ 7 preset Vector SVG độc quyền + custom image:
1. `buni-ecosystem`: Logo & con dấu liên kết hệ sinh thái PTIT & Bachkhoa Aptech.
2. `buni-student`: Hình ảnh sinh viên thực chiến, profile và mạng lưới kết nối.
3. `ai-robotics`: Lục giác vi mạch AI, chip bán dẫn và mạng nơ-ron thông minh.
4. `tech-orbit`: Chu trình xoay vòng 3 bước "Làm trước học sau".
5. `four-stages`: Lộ trình 4 cấp độ dự án OJT (Vỡ lòng -> Cơ sở -> Chuyên sâu -> Doanh nghiệp).
6. `career-passport`: Biểu tượng Hộ chiếu nghề nghiệp Career Passport.
7. `enterprise-network`: Tòa nhà trung tâm và mạng lưới doanh nghiệp đối tác.
8. `custom-image`: Hình ảnh tải lên từ thư mục học liệu (`imageSrc`).

---

## 5. B-roll Cutaway Minh Họa Ngữ Nghĩa (`cutaways`)

```json
{
  "startSec": 15.0,
  "endSec": 24.5,
  "label": "LIÊN HỆ THỰC TIỄN DOANH NGHIỆP",
  "clips": [
    { "src": "van-phong/clip_1.mp4", "duration": 5.0 },
    { "src": "van-phong/clip_2.mp4", "duration": 4.5 }
  ]
}
```
- Tự động cắt toàn màn hình $1920\times 1080$, mượt mà, không giật khung hình.
- Phụ đề SRT 48px Be Vietnam Pro ExtraBold nổi sắc nét phía trên với `z-index: 1000`.
