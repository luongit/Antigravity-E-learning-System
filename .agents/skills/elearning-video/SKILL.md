---
name: elearning-video
description: Giai đoạn 5 - Định tuyến xuất video bài giảng giữa OpenCV, HyperFrames, Manim, 3Dmol, Matter.js, VexFlow, Cesium, Molstar và Virtual Lab. Dùng khi người dùng yêu cầu tạo video, render, animation hoặc bước 5; hỏi engine nếu chưa được chỉ rõ.
---

# Giai đoạn 5: Định tuyến & Chọn engine video bài giảng

Skill này là điểm vào chung cho toàn bộ Giai đoạn 5, không tự ý render và không mặc định chọn engine.

---

## ⚠️ NGUYÊN TẮC SẢN XUẤT CHUNG (BẮT BUỘC)

Trước khi thực hiện bất kỳ engine nào, Agent **BẮT BUỘC ĐỌC VÀ TUÂN THỦ** toàn bộ các nguyên tắc mỹ thuật, bố cục, khoảng cách 15–30px, phân cấp cỡ chữ, SRT Lockstep và trám cảnh B-roll ngữ nghĩa động trong tệp quy chuẩn:

👉 **[Quy Chuẩn Sản Xuất Video E-Learning Chung](references/video-production-principles.md)**

---

## Quy Trình Chọn Engine

1. **Xác định video mục tiêu:** Xác định video đang được yêu cầu trong `output/<ma-mon-hoc>/video-<x>/`. Nếu yêu cầu nhiều video, xử lý từng thư mục độc lập; không trộn lẫn kịch bản.
2. **Kiểm tra lựa chọn engine:** Đọc lựa chọn engine trong yêu cầu hiện tại hoặc lựa chọn đã được người dùng xác nhận cho tác vụ đang tiếp tục. Lệnh gọi trực tiếp skill OpenCV/HyperFrames/Manim/3Dmol/Matter.js/VexFlow/Cesium/Molstar/Virtual Lab cũng là lựa chọn rõ ràng. Yêu cầu mới ghi đè lựa chọn cũ; không tự áp dụng lựa chọn của video khác.
3. **Hỏi người dùng nếu chưa rõ:** Nếu chưa rõ engine, hỏi đúng câu: **"Bạn muốn xuất video bằng OpenCV, HyperFrames, Manim, 3Dmol, Matter.js, VexFlow, Cesium, Molstar hay Virtual Lab?"** và đợi câu trả lời. 
   - Có thể kiểm kê tài nguyên (Pre-flight) trong lúc chờ.
   - Tuyệt đối không tự động chọn theo tài nguyên đang có. Quy tắc này áp dụng cả khi chạy toàn trình (`0`), phím tắt `5`, `/goal` hoặc khi đã có đủ MP3/SRT/ảnh.
4. **Kích hoạt Sub-Skill tương ứng:**
   - **`OpenCV`** (Whiteboard Animation với OpenCV): Đọc và thực thi [elearning-opencv-video](../elearning-opencv-video/SKILL.md). Giữ quy trình: ảnh slide → Canny → tô màu → bàn tay → phụ đề → MP4.
   - **`HyperFrames`** (Animation với HTML/SVG/GSAP & JSON Spec v2): Đọc và thực thi [elearning-hyperframes-video](../elearning-hyperframes-video/SKILL.md). Bắt đầu bằng `script.md` riêng và prompt thiết kế, dựng cảnh HTML/SVG, đồng bộ audio, áp dụng theme preset, Spring animation, Typewriter code studio và tự động lồng ghép video B-roll minh họa từ `inputs/video-libraries/`.
   - **`Manim`** (Diễn họa Giải thuật IT & Toán STEM): Đọc và thực thi [elearning-manim-video](../elearning-manim-video/SKILL.md). Dựng cảnh bằng Python Manim Community, diễn họa cấu trúc dữ liệu, đồ thị, ma trận, công thức toán và xuất video MP4 cùng slide PPTX/PDF.
   - **`3Dmol`** (Mô phỏng Hóa học & Cấu trúc Phân tử 3D): Đọc và thực thi [elearning-3dmol-video](../elearning-3dmol-video/SKILL.md). Dựng cảnh phân tử WebGL 3Dmol.js kết hợp tính toán RDKit từ mã SMILES, xuất video MP4 và slide PPTX/PDF.
   - **`Matter.js`** (Vật lý Cơ học 2D & Động lực học Vật chất cứng): Đọc và thực thi [elearning-matterjs-video](../elearning-matterjs-video/SKILL.md). Tự động tính toán quỹ đạo parabol, ném xiên/ngang, va chạm đàn hồi, con lắc, lò xo, xuất video MP4 và slide PPTX/PDF.
   - **`VexFlow`** (Giáo dục Âm nhạc, Ký âm & Piano Synth): Đọc và thực thi [elearning-vexflow-video](../elearning-vexflow-video/SKILL.md). Render ký âm khuông nhạc chuẩn quốc tế, mô phỏng thanh cuộn Playhead, phím đàn Piano sáng đèn và xuất video MP4 cùng slide PPTX/PDF.
   - **`Cesium`** (Địa lý Tự nhiên, Quả địa cầu 3D & Bản đồ số): Đọc và thực thi [elearning-cesium-video](../elearning-cesium-video/SKILL.md). Diễn họa Quả địa cầu 3D, độ cao địa hình, tọa độ và quỹ đạo camera Fly-to, xuất video MP4 và slide PPTX/PDF.
   - **`Molstar`** (Sinh học Phân tử, Chuỗi ADN/RNA & Protein 3D): Đọc và thực thi [elearning-molstar-video](../elearning-molstar-video/SKILL.md). Diễn họa cấu trúc sinh học từ ngân hàng RCSB PDB, Cartoon ribbon, Ball-and-Stick, bảng màu bazơ nitơ A-T/G-X, xuất video MP4 và slide PPTX/PDF.
   - **`Virtual Lab`** (Khoa học Tự nhiên & Thí nghiệm Ảo Đa miền): Đọc và thực thi [elearning-virtual-lab-video](../elearning-virtual-lab-video/SKILL.md). Mô phỏng thí nghiệm tương tác Quang học (Ray Optics Snell, thấu kính, lăng kính), Cơ học 9 bài thí nghiệm (Matter.js), Mạch điện DC/Ohm/RC, Sóng cơ học và Điện trường Coulomb; xuất video MP4 và slide PPTX/PDF.
   - Nếu câu trả lời không xác định được engine: Tiếp tục giữ câu hỏi đang chờ, không tự suy diễn.

---

## Pre-flight Check

Chạy từ gốc dự án, thay đường dẫn bằng video thực tế:

```powershell
python core/preflight.py "output/<ma-mon-hoc>/video-<x>" --stage video --json
```

`STATUS_NEED_VIDEO_ENGINE` yêu cầu hỏi câu hỏi lựa chọn trên. 
`STATUS_NEED_SCENE_PREPARATION` chỉ xác nhận đã có script để đọc, không có nghĩa là đã kiểm tra xong nội dung hay sẵn sàng render.

- Không bắt nhánh HyperFrames phải có sẵn ảnh slide phẳng. 
- Không tự đổi sang OpenCV nếu HyperFrames gặp lỗi. Báo lỗi cụ thể và xử lý đúng phạm vi kỹ năng được giao.


---

## Bàn Giao Đầu Ra

Toàn bộ các engine đều phải xuất video MP4 chất lượng cao chuẩn **$1920\times 1080$ (Full HD, 30fps)**, giữ nguyên quy chuẩn sư phạm, văn phong tích cực 100%, giọng đọc chuẩn và phụ đề sắc nét của dự án.
Báo cáo rõ engine đã dùng kèm đường dẫn tệp sản phẩm sau khi đã kiểm tra tệp thực tế.
