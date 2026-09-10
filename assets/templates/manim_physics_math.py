"""
assets/templates/manim_physics_math.py
Template chuẩn diễn họa Vật lý Lý thuyết & Toán học Cao cấp bằng Manim Community Edition.
Hỗ trợ:
- Tích phân, Đồ thị hàm số Gauss, Tổng Riemann
- Sóng cơ học, Dao động điều hòa & Phương trình vi phân
- Mặt phẳng phức, Vòng tròn lượng giác đơn vị & Đẳng thức Euler
- Cơ chế tự động nhận diện LaTeX: Tự động dùng MathTex nếu có MiKTeX/TeXLive,
  tự động chuyển sang Text Unicode (Be Vietnam Pro) nếu chưa cài LaTeX để tránh lỗi.
"""

import shutil
import numpy as np
from manim import *


def create_math_label(latex_str: str, unicode_fallback: str, color="#38BDF8", scale: float = 1.0):
    """Tạo đối tượng công thức an toàn: Dùng MathTex nếu hệ thống có latex, ngược lại dùng Text với font Cambria Math."""
    if shutil.which("latex"):
        try:
            return MathTex(latex_str, color=color).scale(scale)
        except Exception:
            pass
    return Text(unicode_fallback, font="Cambria Math", font_size=int(28 * scale), color=color)


class PhysicsMathScene(Scene):
    """Mô phỏng Tích phân Gauss và Tổng Riemann hình học."""
    def construct(self):
        # Thiết lập màu nền tối sang trọng chuẩn E-Learning
        self.camera.background_color = "#0F172A"

        # Badge thể loại bài giảng
        category_badge = Text(
            "VẬT LÝ LÝ THUYẾT & TOÁN HỌC STEM",
            font="Be Vietnam Pro",
            font_size=16,
            color="#38BDF8"
        ).to_corner(UL, buff=0.6)
        self.add(category_badge)

        # Tiêu đề & Công thức tích phân Gauss
        title = create_math_label(
            r"f(x) = \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}",
            "f(x) = ∫₀^∞ e^(-x²) dx = √π / 2",
            color="#38BDF8",
            scale=1.15
        )
        title.to_edge(UP, buff=0.9)

        # Hệ trục tọa độ 2D
        axes = Axes(
            x_range=[-3.2, 3.2, 1],
            y_range=[0, 1.4, 0.5],
            x_length=9,
            y_length=4.5,
            axis_config={
                "color": "#64748B",
            },
        ).shift(DOWN * 0.6)

        x_lbl = Text("x", font="Be Vietnam Pro", font_size=20, color="#94A3B8").next_to(axes.x_axis.get_end(), DR, buff=0.1)
        y_lbl = Text("f(x)", font="Be Vietnam Pro", font_size=20, color="#94A3B8").next_to(axes.y_axis.get_end(), UL, buff=0.1)
        axes_labels = VGroup(x_lbl, y_lbl)

        # Đường cong phân phối chuẩn Gauss
        graph = axes.plot(lambda x: np.exp(-x**2), color="#F59E0B", stroke_width=4)
        graph_label = Text("y = e^(-x²)", font="Be Vietnam Pro", font_size=20, color="#F59E0B")
        graph_label.next_to(axes.c2p(1.2, np.exp(-1.44)), UR, buff=0.2)

        # Diện tích tích phân bằng các hình chữ nhật Riemann
        area = axes.get_riemann_rectangles(
            graph,
            x_range=[-2.2, 2.2],
            dx=0.15,
            color="#EF4444",
            fill_opacity=0.45,
            stroke_width=0.5
        )

        # Diễn hoạt xuất hiện
        self.play(Write(title), run_time=1.5)
        self.play(Create(axes), Write(axes_labels), run_time=1.2)
        self.play(Create(graph), FadeIn(graph_label), run_time=1.5)
        self.play(FadeIn(area), run_time=1.5)
        self.wait(2)


class WaveSimulationScene(Scene):
    """Mô phỏng Truyền sóng điều hòa 2D: y(x, t) = A * sin(k*x - omega*t)."""
    def construct(self):
        self.camera.background_color = "#0F172A"

        category = Text("DAO ĐỘNG & SÓNG CƠ HỌC", font="Be Vietnam Pro", font_size=16, color="#10B981")
        category.to_corner(UL, buff=0.6)
        self.add(category)

        formula = create_math_label(
            r"u(x, t) = A \cdot \cos(\omega t - kx + \varphi)",
            "u(x, t) = A · cos(ωt - kx + φ)",
            color="#38BDF8",
            scale=1.1
        ).to_edge(UP, buff=0.9)

        axes = Axes(
            x_range=[0, 4 * np.pi, np.pi],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=4.5,
            axis_config={"color": "#475569"},
        ).shift(DOWN * 0.5)

        sine_wave = axes.plot(lambda x: np.sin(x), color="#38BDF8", stroke_width=4)

        self.play(Write(formula))
        self.play(Create(axes), Create(sine_wave), run_time=1.5)
        self.wait(2)


class EulerIdentityScene(Scene):
    """Mô phỏng Đẳng thức Euler e^(i*pi) + 1 = 0 trên Mặt phẳng phức."""
    def construct(self):
        self.camera.background_color = "#0F172A"

        header = Text("ĐẲNG THỨC EULER TRONG MẶT PHẲNG PHỨC", font="Be Vietnam Pro", font_size=20, color="#F59E0B")
        header.to_corner(UL, buff=0.6)
        self.add(header)

        euler_eq = create_math_label(
            r"e^{i\pi} + 1 = 0",
            "e^(iπ) + 1 = 0",
            color="#EF4444",
            scale=1.5
        ).to_edge(UP, buff=1.0)

        plane = ComplexPlane(
            x_range=[-2, 2, 1],
            y_range=[-1.5, 1.5, 1],
            axis_config={"color": "#64748B"},
        ).shift(DOWN * 0.5)

        unit_circle = Circle(radius=plane.get_x_unit_size(), color="#38BDF8", stroke_width=2.5).move_to(plane.c2p(0, 0))

        dot = Dot(plane.c2p(1, 0), color="#F59E0B", radius=0.1)
        vector = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), buff=0, color="#F59E0B")

        self.play(Write(euler_eq))
        self.play(Create(plane), Create(unit_circle))
        self.play(GrowArrow(vector), FadeIn(dot))
        self.wait(2)
