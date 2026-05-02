"""
═══════════════════════════════════════════════════════════════════════════════
  NEXRO PLANT AI  —  Diagnóstico Inteligente de Cultivos
  Nexro Systems © 2026
═══════════════════════════════════════════════════════════════════════════════
"""
import sys
import os
import datetime
import shutil
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QFileDialog, QScrollArea, QFrame, QProgressBar,
    QStackedWidget, QLineEdit, QMessageBox, QDialog, QGraphicsDropShadowEffect,
    QComboBox, QSplashScreen, QMenu, QToolButton, QSizePolicy
)
from PyQt6.QtCore import (Qt, QThread, pyqtSignal, QSize, QTimer, QPropertyAnimation,
                          QEasingCurve, QRect, QPoint)
from PyQt6.QtGui import (QPixmap, QImage, QFont, QColor, QPalette, QCursor,
                         QAction, QKeySequence, QShortcut, QPainter, QPen, QBrush,
                         QLinearGradient, QFontDatabase)
import cv2
from PIL import Image
from ultralytics import YOLO

# Módulos locales
from nexro_data import (INFO, CULTIVOS, CLASE_A_CULTIVO,
                        C_BG, C_BG2, C_CARD, C_CARD2, C_ACC, C_ACC2, C_ACC_DK,
                        C_TEXT, C_SUB, C_SUB2, C_BOR, C_DANGER, C_WARN,
                        GSEV, GSEV_LABEL, GSEV_BG)
from nexro_utils import (cargar_historial, guardar_historial, limpiar_historial,
                         validar_imagen, exportar_reporte_excel, exportar_catalogo_excel,
                         exportar_reporte_pdf)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")
CACHE_DIR  = os.path.join(BASE_DIR, ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)

APP_VERSION = "3.0 Pro"

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS DE UI
# ═══════════════════════════════════════════════════════════════════════════════
def add_shadow(widget, blur=20, color=(0, 229, 160, 40), offset=(0, 4)):
    """Añade sombra suave a un widget."""
    s = QGraphicsDropShadowEffect()
    s.setBlurRadius(blur)
    s.setColor(QColor(*color))
    s.setOffset(*offset)
    widget.setGraphicsEffect(s)


def make_label(text, style="", align=None, wrap=False):
    l = QLabel(text)
    if style: l.setStyleSheet(style)
    if align: l.setAlignment(align)
    if wrap:  l.setWordWrap(True)
    return l


def make_button(text, bg, fg, hover, height=42, width=None, bold=True, border=None):
    btn = QPushButton(text)
    btn.setFixedHeight(height)
    if width: btn.setFixedWidth(width)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    b = f"border:2px solid {border};" if border else "border:none;"
    btn.setStyleSheet(f"""
        QPushButton {{
            background:{bg}; color:{fg};
            border-radius:10px; font-size:13px;
            font-weight:{'700' if bold else '500'};
            {b}
        }}
        QPushButton:hover {{ background:{hover}; }}
        QPushButton:disabled {{ background:{C_BOR}; color:{C_SUB}; border:none; }}
    """)
    return btn


# ═══════════════════════════════════════════════════════════════════════════════
# HILO DE INFERENCIA
# ═══════════════════════════════════════════════════════════════════════════════
class InferenceThread(QThread):
    finished = pyqtSignal(object, object, float)
    error    = pyqtSignal(str)

    def __init__(self, model, path):
        super().__init__()
        self.model = model
        self.path  = path

    def run(self):
        try:
            import time
            t0 = time.time()
            r  = self.model(self.path, conf=0.01, verbose=False)
            elapsed = time.time() - t0
            self.finished.emit(r[0].plot(), r[0], elapsed)
        except Exception as e:
            self.error.emit(str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# SPLASH SCREEN
# ═══════════════════════════════════════════════════════════════════════════════
class SplashScreen(QSplashScreen):
    def __init__(self):
        pix = QPixmap(500, 320)
        pix.fill(QColor(C_BG))
        super().__init__(pix)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SplashScreen |
                            Qt.WindowType.WindowStaysOnTopHint)

    def drawContents(self, painter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fondo con borde degradado
        painter.setPen(QPen(QColor(C_ACC), 2))
        painter.setBrush(QBrush(QColor(C_BG)))
        painter.drawRoundedRect(0, 0, 499, 319, 16, 16)

        # Logo
        painter.setPen(QColor(C_TEXT))
        f = QFont("Segoe UI", 36, QFont.Weight.Black)
        painter.setFont(f)
        painter.drawText(QRect(0, 70, 500, 60), Qt.AlignmentFlag.AlignCenter, "🌿")

        f2 = QFont("Segoe UI", 22, QFont.Weight.Black)
        painter.setFont(f2)
        painter.setPen(QColor(C_TEXT))
        painter.drawText(QRect(0, 140, 500, 40), Qt.AlignmentFlag.AlignCenter, "Nexro Plant AI")

        f3 = QFont("Segoe UI", 10)
        painter.setFont(f3)
        painter.setPen(QColor(C_SUB))
        painter.drawText(QRect(0, 180, 500, 20), Qt.AlignmentFlag.AlignCenter,
                         "Diagnóstico Inteligente de Cultivos con IA")

        # Línea accent
        painter.setPen(QPen(QColor(C_ACC), 3))
        painter.drawLine(180, 220, 320, 220)

        f4 = QFont("Segoe UI", 9)
        painter.setFont(f4)
        painter.setPen(QColor(C_SUB))
        painter.drawText(QRect(0, 240, 500, 20), Qt.AlignmentFlag.AlignCenter,
                         "Cargando modelo YOLOv8...")

        painter.setPen(QColor(C_SUB2))
        painter.drawText(QRect(0, 280, 500, 20), Qt.AlignmentFlag.AlignCenter,
                         f"v{APP_VERSION}  ·  Nexro Systems © 2026")


# ═══════════════════════════════════════════════════════════════════════════════
# PANTALLA INICIO (HERO)
# ═══════════════════════════════════════════════════════════════════════════════
class HomeScreen(QWidget):
    go_analisis = pyqtSignal()
    go_catalogo = pyqtSignal()
    go_historial = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background:{C_BG};")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        lay.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border:none; background:transparent; }}
            QScrollBar:vertical {{ background:{C_BG}; width:8px; border-radius:4px; }}
            QScrollBar::handle:vertical {{ background:{C_BOR}; border-radius:4px; }}
            QScrollBar::handle:vertical:hover {{ background:{C_ACC}; }}
        """)

        inner = QWidget()
        inner.setStyleSheet(f"background:{C_BG};")
        vlay = QVBoxLayout(inner)
        vlay.setContentsMargins(60, 40, 60, 50)
        vlay.setSpacing(28)

        # ── Badge ────────────────────────────────────────────────────────────
        badge_row = QHBoxLayout()
        badge = QLabel("✦  SISTEMA DE DIAGNÓSTICO FITOSANITARIO CON IA")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"""
            color:{C_ACC};
            font-size:11px;
            font-weight:800;
            letter-spacing:2px;
            padding:10px 24px;
            background:{C_ACC_DK};
            border:1px solid #00e5a050;
            border-radius:22px;
        """)
        badge.setFixedHeight(40)
        badge_row.addStretch(); badge_row.addWidget(badge); badge_row.addStretch()
        vlay.addLayout(badge_row)

        # ── Título principal (una sola línea con "IA" resaltado) ────────────
        title_box = QVBoxLayout()
        title_box.setSpacing(4)

        t1 = QLabel("Detecta enfermedades en")
        t1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        t1.setStyleSheet(f"color:{C_TEXT}; font-size:40px; font-weight:900; letter-spacing:-1px;")
        title_box.addWidget(t1)

        # Línea con "tus cultivos con IA" — IA en verde
        line2 = QWidget()
        line2.setStyleSheet("background:transparent;")
        lh = QHBoxLayout(line2)
        lh.setContentsMargins(0,0,0,0); lh.setSpacing(0)
        lh.setAlignment(Qt.AlignmentFlag.AlignCenter)

        t2a = QLabel("tus cultivos con ")
        t2a.setStyleSheet(f"color:{C_TEXT}; font-size:40px; font-weight:900; letter-spacing:-1px;")
        t2b = QLabel("IA")
        t2b.setStyleSheet(f"color:{C_ACC}; font-size:40px; font-weight:900; letter-spacing:-1px;")
        lh.addWidget(t2a); lh.addWidget(t2b)
        title_box.addWidget(line2)

        vlay.addLayout(title_box)

        # ── Subtítulo ────────────────────────────────────────────────────────
        sub = QLabel("Sube una foto de una hoja y recibe un diagnóstico preciso en segundos.\n"
                     "88 enfermedades en 20 cultivos. Entrenado con fotos reales de campo.")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"color:{C_SUB2}; font-size:14px; line-height:1.7;")
        vlay.addWidget(sub)

        # ── Stats ────────────────────────────────────────────────────────────
        stats_data = [
            ("88",    "Enfermedades"),
            ("20",    "Cultivos"),
            ("93.7%", "Precisión"),
            ("<2s",   "Diagnóstico"),
            ("79K+",  "Imágenes"),
        ]
        srow = QHBoxLayout()
        srow.setSpacing(12)
        srow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for val, lbl in stats_data:
            chip = QFrame()
            chip.setStyleSheet(f"""
                background:{C_CARD};
                border-radius:24px;
                border:1px solid {C_BOR};
            """)
            cl = QHBoxLayout(chip)
            cl.setContentsMargins(20, 10, 20, 10)
            cl.setSpacing(8)
            v = QLabel(val)
            v.setStyleSheet(f"color:{C_ACC}; font-size:16px; font-weight:900;")
            t = QLabel(lbl)
            t.setStyleSheet(f"color:{C_SUB}; font-size:12px; font-weight:500;")
            cl.addWidget(v); cl.addWidget(t)
            srow.addWidget(chip)
        vlay.addLayout(srow)

        # ── Botones de acción ───────────────────────────────────────────────
        brow = QHBoxLayout()
        brow.setSpacing(14)
        brow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_a = QPushButton("🔬   Analizar imagen")
        btn_a.setFixedHeight(52); btn_a.setFixedWidth(220)
        btn_a.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_a.setStyleSheet(f"""
            QPushButton {{
                background:{C_ACC}; color:#000;
                border-radius:12px; font-size:14px;
                font-weight:800; border:none;
                letter-spacing:0.5px;
            }}
            QPushButton:hover {{ background:#00ffb3; }}
        """)
        add_shadow(btn_a, blur=25, color=(0, 229, 160, 100), offset=(0, 6))
        btn_a.clicked.connect(self.go_analisis)

        btn_c = QPushButton("📚   Ver catálogo")
        btn_c.setFixedHeight(52); btn_c.setFixedWidth(220)
        btn_c.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_c.setStyleSheet(f"""
            QPushButton {{
                background:transparent; color:{C_ACC};
                border-radius:12px; font-size:14px;
                font-weight:800; border:2px solid {C_ACC};
                letter-spacing:0.5px;
            }}
            QPushButton:hover {{ background:#00e5a015; }}
        """)
        btn_c.clicked.connect(self.go_catalogo)

        brow.addWidget(btn_a); brow.addWidget(btn_c)
        vlay.addLayout(brow)

        # ── Tips de foto ────────────────────────────────────────────────────
        tips_card = QFrame()
        tips_card.setStyleSheet(f"""
            background:{C_CARD};
            border-radius:16px;
            border:1px solid {C_BOR};
        """)
        tl = QVBoxLayout(tips_card)
        tl.setContentsMargins(28, 22, 28, 22)
        tl.setSpacing(16)

        th_row = QHBoxLayout()
        th = QLabel("📸   Cómo tomar la foto para mejor resultado")
        th.setStyleSheet(f"color:{C_TEXT}; font-size:15px; font-weight:800;")
        th_row.addWidget(th)
        th_row.addStretch()
        tl.addLayout(th_row)

        tips_ok = [
            "Una sola hoja en el centro de la imagen",
            "La enfermedad visible y enfocada claramente",
            "Buena iluminación natural, sin sombras fuertes",
            "Fondo lo más uniforme posible",
        ]
        tips_no = [
            "No múltiples hojas superpuestas",
            "No fotos borrosas o muy oscuras",
            "No manos sosteniendo la hoja",
            "No zoom excesivo ni muy lejano",
        ]

        tips_grid = QHBoxLayout()
        tips_grid.setSpacing(40)
        col1 = QVBoxLayout(); col1.setSpacing(10)
        col2 = QVBoxLayout(); col2.setSpacing(10)

        for t in tips_ok:
            r = QHBoxLayout()
            r.setSpacing(10)
            r.setAlignment(Qt.AlignmentFlag.AlignLeft)
            ic = QLabel("✅")
            ic.setStyleSheet("font-size:14px;")
            ic.setFixedWidth(24)
            tx = QLabel(t)
            tx.setStyleSheet(f"color:{C_SUB2}; font-size:12px;")
            r.addWidget(ic); r.addWidget(tx); r.addStretch()
            col1.addLayout(r)
        for t in tips_no:
            r = QHBoxLayout()
            r.setSpacing(10)
            r.setAlignment(Qt.AlignmentFlag.AlignLeft)
            ic = QLabel("❌")
            ic.setStyleSheet("font-size:14px;")
            ic.setFixedWidth(24)
            tx = QLabel(t)
            tx.setStyleSheet(f"color:{C_SUB2}; font-size:12px;")
            r.addWidget(ic); r.addWidget(tx); r.addStretch()
            col2.addLayout(r)

        tips_grid.addLayout(col1)
        tips_grid.addLayout(col2)
        tl.addLayout(tips_grid)

        vlay.addWidget(tips_card)
        vlay.addStretch()

        scroll.setWidget(inner)
        lay.addWidget(scroll)

# ═══════════════════════════════════════════════════════════════════════════════
# PANTALLA ANÁLISIS
# ═══════════════════════════════════════════════════════════════════════════════
class AnalisisScreen(QWidget):
    analisis_completado = pyqtSignal(dict)

    def __init__(self, model_ref, app_ref):
        super().__init__()
        self.model_ref  = model_ref
        self.app_ref    = app_ref
        self.cur_path   = None
        self.result_img = None
        self.last_analysis = None  # dict con resultado completo

        self.setStyleSheet(f"background:{C_BG};")
        self.setAcceptDrops(True)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(16)
        lay.addWidget(self._left_panel(),  stretch=4)
        lay.addWidget(self._right_panel(), stretch=5)

    # ── Drag & Drop ──────────────────────────────────────────────────────────
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith(('.jpg','.jpeg','.png','.bmp','.webp')):
                event.acceptProposedAction()
                self.img_frame.setStyleSheet(f"""
                    background:{C_BG2}; border-radius:12px;
                    border:2px solid {C_ACC};
                """)

    def dragLeaveEvent(self, event):
        if not self.cur_path:
            self.img_frame.setStyleSheet(f"""
                background:{C_BG2}; border-radius:12px;
                border:2px dashed {C_BOR};
            """)

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if path.lower().endswith(('.jpg','.jpeg','.png','.bmp','.webp')):
                self._load_image_from_path(path)

    # ── Panel izquierdo ──────────────────────────────────────────────────────
    def _left_panel(self):
        w = QWidget(); w.setStyleSheet("background:transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0,0,0,0); lay.setSpacing(16)

        # ── Card de imagen ───────────────────────────────────────────────────
        img_card = QFrame()
        img_card.setStyleSheet(f"""
            background:{C_CARD}; border-radius:16px;
            border:1px solid {C_BOR};
        """)
        ic = QVBoxLayout(img_card)
        ic.setContentsMargins(18, 18, 18, 18)
        ic.setSpacing(12)

        # Header imagen
        top = QHBoxLayout()
        icon = QLabel("📷")
        icon.setStyleSheet("font-size:18px;")
        lbl = QLabel("Imagen cargada")
        lbl.setStyleSheet(f"color:{C_TEXT}; font-size:13px; font-weight:700;")
        self.img_name = QLabel("Ninguna  ·  Arrastra o selecciona una imagen")
        self.img_name.setStyleSheet(f"color:{C_SUB}; font-size:11px;")
        top.addWidget(icon); top.addWidget(lbl); top.addStretch(); top.addWidget(self.img_name)
        ic.addLayout(top)

        # Zona de imagen
        self.img_frame = QFrame()
        self.img_frame.setMinimumHeight(280)
        self.img_frame.setStyleSheet(f"""
            background:{C_BG2}; border-radius:12px;
            border:2px dashed {C_BOR};
        """)
        ifl = QVBoxLayout(self.img_frame)
        ifl.setContentsMargins(12, 12, 12, 12)

        self.ph = QLabel("📷\n\nArrastra una imagen aquí\no haz clic en Cargar")
        self.ph.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ph.setStyleSheet(f"color:{C_SUB}; font-size:13px; border:none;")

        self.il = QLabel()
        self.il.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.il.setStyleSheet("border:none;")
        self.il.hide()

        ifl.addWidget(self.ph); ifl.addWidget(self.il)
        ic.addWidget(self.img_frame)

        # Validación
        self.valid_lbl = QLabel("")
        self.valid_lbl.setStyleSheet(f"color:{C_SUB}; font-size:11px;")
        self.valid_lbl.setWordWrap(True)
        ic.addWidget(self.valid_lbl)

        # Botones
        brow = QHBoxLayout(); brow.setSpacing(10)
        self.btn_l = make_button("📂  Cargar imagen", C_ACC, "#000", "#00ffb3", height=44)
        self.btn_l.clicked.connect(self.load_image)
        self.btn_a = make_button("🔬  Analizar", "#1565c0", "white", "#0d47a1", height=44)
        self.btn_a.setEnabled(False)
        self.btn_a.clicked.connect(self.run_inference)
        brow.addWidget(self.btn_l); brow.addWidget(self.btn_a)
        ic.addLayout(brow)

        # Progress
        self.prog = QProgressBar()
        self.prog.setFixedHeight(4); self.prog.setTextVisible(False)
        self.prog.setRange(0, 0)
        self.prog.setStyleSheet(f"""
            QProgressBar {{ background:{C_BOR}; border-radius:2px; border:none; }}
            QProgressBar::chunk {{ background:{C_ACC}; border-radius:2px; }}
        """)
        self.prog.hide()
        ic.addWidget(self.prog)

        lay.addWidget(img_card)

        # ── Card de diagnóstico ─────────────────────────────────────────────
        self.diag_card = QFrame()
        self.diag_card.setStyleSheet(f"""
            background:{C_CARD}; border-radius:16px;
            border:1px solid {C_BOR};
        """)
        self.diag_lay = QVBoxLayout(self.diag_card)
        self.diag_lay.setContentsMargins(18, 18, 18, 18)
        self.diag_lay.setSpacing(12)
        self._diag_placeholder()

        lay.addWidget(self.diag_card, stretch=1)
        return w

    # ── Panel derecho ────────────────────────────────────────────────────────
    def _right_panel(self):
        w = QWidget(); w.setStyleSheet("background:transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0,0,0,0); lay.setSpacing(16)

        # Información detallada
        det = QFrame()
        det.setStyleSheet(f"""
            background:{C_CARD}; border-radius:16px;
            border:1px solid {C_BOR};
        """)
        dl = QVBoxLayout(det)
        dl.setContentsMargins(22, 20, 22, 22)
        dl.setSpacing(14)

        title_lbl = QLabel("📋   Información Detallada")
        title_lbl.setStyleSheet(f"color:{C_TEXT}; font-size:15px; font-weight:800;")
        dl.addWidget(title_lbl)

        row = QHBoxLayout(); row.setSpacing(10)
        self.c_desc = self._icard("📖", "Descripción", "#EFF6FF", "#3b82f6", "—")
        self.c_trat = self._icard("💊", "Tratamiento", "#FEF2F2", "#ef4444", "—")
        self.c_prev = self._icard("🛡️", "Prevención",  "#ECFDF5", C_ACC, "—")
        row.addWidget(self.c_desc); row.addWidget(self.c_trat); row.addWidget(self.c_prev)
        dl.addLayout(row)
        lay.addWidget(det)

        # Otras posibilidades
        otras = QFrame()
        otras.setStyleSheet(f"""
            background:{C_CARD}; border-radius:16px;
            border:1px solid {C_BOR};
        """)
        ol = QVBoxLayout(otras)
        ol.setContentsMargins(22, 20, 22, 22)
        ol.setSpacing(14)

        otras_title = QLabel("🔍   Otras posibilidades")
        otras_title.setStyleSheet(f"color:{C_TEXT}; font-size:15px; font-weight:800;")
        ol.addWidget(otras_title)

        sc = QScrollArea()
        sc.setWidgetResizable(True)
        sc.setFixedHeight(120)
        sc.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        sc.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        sc.setStyleSheet(f"""
            QScrollArea {{ border:none; background:transparent; }}
            QScrollBar:horizontal {{ background:{C_BG}; height:6px; border-radius:3px; }}
            QScrollBar::handle:horizontal {{ background:{C_BOR}; border-radius:3px; }}
            QScrollBar::handle:horizontal:hover {{ background:{C_ACC}; }}
        """)
        self.otras_w = QWidget(); self.otras_w.setStyleSheet("background:transparent;")
        self.otras_l = QHBoxLayout(self.otras_w)
        self.otras_l.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.otras_l.setSpacing(10)
        ph = QLabel("Sin resultados aún. Analiza una imagen primero.")
        ph.setStyleSheet(f"color:{C_SUB}; font-size:12px;")
        self.otras_l.addWidget(ph)
        sc.setWidget(self.otras_w)
        ol.addWidget(sc)

        # Botones de exportación
        exp_row = QHBoxLayout(); exp_row.setSpacing(10)

        self.btn_save = make_button("💾  Guardar imagen", C_CARD2, C_ACC, "#1e2436",
                                    height=42, border=C_BOR)
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self.save_image)

        self.btn_excel = make_button("📊  Excel", C_CARD2, C_ACC, "#1e2436",
                                     height=42, border=C_BOR)
        self.btn_excel.setEnabled(False)
        self.btn_excel.clicked.connect(self.export_excel)

        self.btn_pdf = make_button("📄  PDF", C_CARD2, C_ACC, "#1e2436",
                                   height=42, border=C_BOR)
        self.btn_pdf.setEnabled(False)
        self.btn_pdf.clicked.connect(self.export_pdf)

        exp_row.addWidget(self.btn_save)
        exp_row.addWidget(self.btn_excel)
        exp_row.addWidget(self.btn_pdf)
        ol.addLayout(exp_row)

        lay.addWidget(otras, stretch=1)
        return w

    def _icard(self, icon, title, bg_accent, accent_color, content):
        card = QFrame()
        card.setStyleSheet(f"""
            background:{C_CARD2};
            border-radius:12px;
            border:1px solid {C_BOR};
        """)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(8)

        head = QHBoxLayout()
        ico = QLabel(icon)
        ico.setStyleSheet(f"font-size:18px; color:{accent_color}; background:transparent; border:none;")
        ico.setFixedWidth(26)
        t = QLabel(title)
        t.setStyleSheet(f"color:{accent_color}; font-size:12px; font-weight:800; letter-spacing:0.5px; background:transparent; border:none;")
        head.addWidget(ico); head.addWidget(t); head.addStretch()
        lay.addLayout(head)

        c = QLabel(content)
        c.setStyleSheet(f"color:{C_SUB2}; font-size:12px; background:transparent; border:none; line-height:1.5;")
        c.setWordWrap(True)
        c.setObjectName("content")
        lay.addWidget(c)
        lay.addStretch()
        return card

    def _upd_card(self, card, txt):
        l = card.findChild(QLabel, "content")
        if l: l.setText(txt)

    def _diag_placeholder(self):
        for i in reversed(range(self.diag_lay.count())):
            it = self.diag_lay.itemAt(i)
            wid = it.widget()
            if wid: wid.deleteLater()

        ph = QLabel("🔬\n\nEl diagnóstico aparecerá aquí\ndespués de analizar una imagen.")
        ph.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ph.setStyleSheet(f"color:{C_SUB}; font-size:13px; border:none; line-height:1.7;")
        self.diag_lay.addWidget(ph)

    # ── Cargar imagen ────────────────────────────────────────────────────────
    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar imagen", "",
            "Imágenes (*.jpg *.jpeg *.png *.bmp *.webp)"
        )
        if path:
            self._load_image_from_path(path)

    def _load_image_from_path(self, path):
        self.cur_path = path
        self.result_img = None
        self.last_analysis = None

        self.btn_a.setEnabled(True)
        self.btn_save.setEnabled(False)
        self.btn_excel.setEnabled(False)
        self.btn_pdf.setEnabled(False)

        # Validar imagen
        valid, msg, sev = validar_imagen(path)
        if not valid:
            QMessageBox.warning(self, "Imagen inválida", msg)
            return

        # Mostrar imagen
        self._show_pix(QPixmap(path))
        fname = os.path.basename(path)
        self.img_name.setText(f"✓  {fname[:35]}{'…' if len(fname)>35 else ''}")
        self.img_name.setStyleSheet(f"color:{C_ACC}; font-size:11px; font-weight:600;")

        self.img_frame.setStyleSheet(f"""
            background:{C_BG2}; border-radius:12px;
            border:2px solid {C_BOR};
        """)

        # Mostrar validación
        col = C_ACC if sev == "ok" else C_WARN
        icon = "✓" if sev == "ok" else "⚠"
        self.valid_lbl.setText(f"{icon}  {msg}")
        self.valid_lbl.setStyleSheet(f"color:{col}; font-size:11px; font-weight:500;")

        # Limpiar diagnóstico previo
        self._diag_placeholder()
        self._upd_card(self.c_desc, "—")
        self._upd_card(self.c_trat, "—")
        self._upd_card(self.c_prev, "—")

        for i in reversed(range(self.otras_l.count())):
            wid = self.otras_l.itemAt(i).widget()
            if wid: wid.deleteLater()
        ph = QLabel("Sin resultados aún. Analiza una imagen primero.")
        ph.setStyleSheet(f"color:{C_SUB}; font-size:12px;")
        self.otras_l.addWidget(ph)

    # ── Inferencia ───────────────────────────────────────────────────────────
    def run_inference(self):
        model = self.model_ref()
        if not model:
            QMessageBox.warning(self, "Modelo no cargado", "El modelo de IA aún no está listo.")
            return
        if not self.cur_path:
            return

        self.btn_a.setEnabled(False)
        self.btn_l.setEnabled(False)
        self.prog.show()

        if self.app_ref:
            self.app_ref.status.setText("🔬  Analizando imagen con YOLOv8...")

        self.thread = InferenceThread(model, self.cur_path)
        self.thread.finished.connect(self._on_result)
        self.thread.error.connect(self._on_error)
        self.thread.start()

    def _on_result(self, img_cv2, results, elapsed):
        self.prog.hide()
        self.btn_l.setEnabled(True)
        self.result_img = img_cv2

        # Mostrar imagen anotada
        rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
        h, w, c = rgb.shape
        qimg = QImage(rgb.data, w, h, w*c, QImage.Format.Format_RGB888)
        self._show_pix(QPixmap.fromImage(qimg))
        self.img_frame.setStyleSheet(f"""
            background:{C_BG2}; border-radius:12px;
            border:2px solid {C_ACC};
        """)

        probs = results.probs
        if probs is not None:
            top_idx  = int(probs.top1)
            top_conf = float(probs.top1conf)
            names    = results.names
            top_name = names[top_idx]
            top5n    = [names[i] for i in probs.top5]
            top5c    = probs.top5conf.cpu().numpy().tolist()

            self._show_diag(top_name, top_conf, top5n, top5c)

            # Guardar resultado
            self.last_analysis = {
                "clase":    top_name,
                "conf":     top_conf,
                "info":     INFO.get(top_name, {}),
                "top5n":    top5n,
                "top5c":    top5c,
                "imagen":   self.cur_path,
                "fecha":    datetime.datetime.now().isoformat(),
                "elapsed":  elapsed,
            }

            # Añadir al historial
            self._add_to_historial()

            # Emitir señal
            self.analisis_completado.emit(self.last_analysis)

            if self.app_ref:
                nombre = INFO.get(top_name, {}).get("n", top_name)
                self.app_ref.status.setText(
                    f"✓  {nombre} — {top_conf*100:.1f}% confianza  ·  {elapsed:.2f}s")

        self.btn_a.setEnabled(True)
        self.btn_save.setEnabled(True)
        self.btn_excel.setEnabled(True)
        self.btn_pdf.setEnabled(True)

    def _on_error(self, msg):
        self.prog.hide()
        self.btn_l.setEnabled(True)
        self.btn_a.setEnabled(True)
        QMessageBox.critical(self, "Error", f"No se pudo analizar la imagen:\n{msg}")

    def _add_to_historial(self):
        if not self.last_analysis: return
        # Copiar imagen a cache
        try:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            ext = os.path.splitext(self.cur_path)[1]
            cache_path = os.path.join(CACHE_DIR, f"img_{ts}{ext}")
            shutil.copy2(self.cur_path, cache_path)

            item = {
                "clase":   self.last_analysis["clase"],
                "conf":    self.last_analysis["conf"],
                "fecha":   self.last_analysis["fecha"],
                "imagen":  cache_path,
                "original": self.cur_path,
            }
            guardar_historial(item)
        except Exception:
            pass

    # ── Mostrar diagnóstico ──────────────────────────────────────────────────
    def _show_diag(self, cls_name, conf, top5n, top5c):
        info = INFO.get(cls_name, {})
        nombre = info.get("n", cls_name.replace("_", " ").title())
        emoji  = info.get("e", "🌿")
        grav   = info.get("g", "desconocida")
        desc   = info.get("d", "Sin información disponible.")
        trat   = info.get("t", "Consultar con agrónomo.")
        prev   = info.get("p", "Monitoreo regular.")
        gc     = GSEV.get(grav, C_SUB)
        gbg    = GSEV_BG.get(grav, C_CARD2)
        glabel = GSEV_LABEL.get(grav, "DIAGNÓSTICO")
        es_sano = grav == "ninguna"

        # Limpiar
        for i in reversed(range(self.diag_lay.count())):
            wid = self.diag_lay.itemAt(i).widget()
            if wid: wid.deleteLater()

        # Tarjeta alerta
        alert = QFrame()
        alert.setStyleSheet(f"""
            background:{gbg};
            border-radius:12px;
            border-left:4px solid {gc};
            border-top:1px solid {C_BOR};
            border-right:1px solid {C_BOR};
            border-bottom:1px solid {C_BOR};
        """)
        al = QVBoxLayout(alert)
        al.setContentsMargins(16, 14, 16, 14)
        al.setSpacing(6)

        # Etiqueta de estado
        status_row = QHBoxLayout()
        status_lbl = QLabel(glabel)
        status_lbl.setStyleSheet(f"""
            color:{gc}; font-size:10px; font-weight:900;
            letter-spacing:1.5px; background:transparent; border:none;
        """)
        status_row.addWidget(status_lbl)
        status_row.addStretch()
        al.addLayout(status_row)

        # Nombre
        name_lbl = QLabel(f"{emoji}   {nombre}")
        name_lbl.setStyleSheet(f"""
            color:{C_TEXT}; font-size:17px; font-weight:800;
            background:transparent; border:none;
        """)
        al.addWidget(name_lbl)

        # Clase técnica
        cls_lbl = QLabel(cls_name)
        cls_lbl.setStyleSheet(f"""
            color:{C_SUB}; font-size:11px; font-style:italic;
            background:transparent; border:none;
        """)
        al.addWidget(cls_lbl)

        # Confianza
        conf_row = QHBoxLayout()
        conf_row.setSpacing(8)
        conf_val = QLabel(f"{conf*100:.1f}%")
        conf_val.setStyleSheet(f"""
            color:{gc}; font-size:28px; font-weight:900;
            background:transparent; border:none;
        """)
        conf_txt = QLabel("de confianza")
        conf_txt.setStyleSheet(f"""
            color:{C_SUB}; font-size:12px;
            background:transparent; border:none;
        """)
        conf_row.addWidget(conf_val)
        conf_row.addWidget(conf_txt)
        conf_row.addStretch()

        grav_chip = QLabel(f"  {grav.upper()}  ")
        grav_chip.setStyleSheet(f"""
            color:{gc}; font-size:10px; font-weight:800;
            background:{C_BG2}; padding:4px 8px; border-radius:10px;
            border:1px solid {gc}40;
        """)
        conf_row.addWidget(grav_chip)
        al.addLayout(conf_row)

        # Barra
        bar_bg = QFrame()
        bar_bg.setFixedHeight(6)
        bar_bg.setStyleSheet(f"""
            background:{C_BOR}; border-radius:3px; border:none;
        """)
        bar_f = QFrame(bar_bg)
        bar_f.setFixedHeight(6)
        bar_f.setStyleSheet(f"""
            background:{gc}; border-radius:3px; border:none;
        """)
        bar_f.setFixedWidth(1)

        def animate_bar():
            w_total = bar_bg.width()
            target = max(1, int(w_total * conf))
            anim = QPropertyAnimation(bar_f, b"geometry")
            anim.setDuration(800)
            anim.setStartValue(QRect(0, 0, 1, 6))
            anim.setEndValue(QRect(0, 0, target, 6))
            anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            anim.start()
            self._anim_ref = anim

        QTimer.singleShot(150, animate_bar)
        al.addWidget(bar_bg)
        self.diag_lay.addWidget(alert)

        # Actualizar cards
        self._upd_card(self.c_desc, desc)
        self._upd_card(self.c_trat, trat)
        self._upd_card(self.c_prev, prev)

        # Otras posibilidades
        for i in reversed(range(self.otras_l.count())):
            wid = self.otras_l.itemAt(i).widget()
            if wid: wid.deleteLater()

        for nm, cf in zip(top5n[1:], top5c[1:]):
            inf2 = INFO.get(nm, {})
            g2 = inf2.get("g", "media")
            gc2 = GSEV.get(g2, C_SUB)

            mini = QFrame()
            mini.setFixedWidth(150)
            mini.setFixedHeight(82)
            mini.setStyleSheet(f"""
                background:{C_CARD2}; border-radius:10px;
                border:1px solid {C_BOR};
                border-top:2px solid {gc2};
            """)
            ml = QVBoxLayout(mini)
            ml.setContentsMargins(10, 8, 10, 10)
            ml.setSpacing(4)

            em_lbl = QLabel(inf2.get("e", "🌿"))
            em_lbl.setStyleSheet(f"font-size:14px; background:transparent; border:none;")

            n2 = inf2.get("n", nm.replace("_"," ").title())
            if len(n2) > 22: n2 = n2[:22] + "…"
            nm_lbl = QLabel(n2)
            nm_lbl.setStyleSheet(f"color:{C_TEXT}; font-size:11px; font-weight:600; background:transparent; border:none;")
            nm_lbl.setWordWrap(True)

            cf_lbl = QLabel(f"{cf*100:.1f}%")
            cf_lbl.setStyleSheet(f"color:{C_SUB}; font-size:14px; font-weight:800; background:transparent; border:none;")

            ml.addWidget(em_lbl)
            ml.addWidget(nm_lbl)
            ml.addStretch()
            ml.addWidget(cf_lbl)

            self.otras_l.addWidget(mini)
        self.otras_l.addStretch()

    # ── Exportar ─────────────────────────────────────────────────────────────
    def save_image(self):
        if self.result_img is None: return
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar imagen", "nexro_resultado.jpg",
            "JPEG (*.jpg);;PNG (*.png)"
        )
        if path:
            cv2.imwrite(path, self.result_img)
            QMessageBox.information(self, "Guardado", f"Imagen guardada en:\n{path}")

    def export_excel(self):
        if not self.last_analysis: return
        la = self.last_analysis
        default = f"nexro_diagnostico_{la['clase']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar reporte Excel", default, "Excel (*.xlsx)"
        )
        if not path: return
        try:
            exportar_reporte_excel(
                path, la["clase"], la["conf"], la["info"],
                la["top5n"], la["top5c"],
                imagen_path=la["imagen"], INFO=INFO
            )
            QMessageBox.information(self, "Excel generado",
                                    f"✓ Reporte exportado correctamente:\n{path}")
        except ImportError:
            QMessageBox.warning(self, "Falta librería",
                                "Instala openpyxl:\n\npip install openpyxl")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar:\n{e}")

    def export_pdf(self):
        if not self.last_analysis: return
        la = self.last_analysis
        default = f"nexro_diagnostico_{la['clase']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar reporte PDF", default, "PDF (*.pdf)"
        )
        if not path: return
        try:
            exportar_reporte_pdf(
                path, la["clase"], la["conf"], la["info"],
                la["top5n"], la["top5c"],
                imagen_path=la["imagen"], INFO=INFO
            )
            QMessageBox.information(self, "PDF generado",
                                    f"✓ Reporte exportado correctamente:\n{path}")
        except ImportError:
            QMessageBox.warning(self, "Falta librería",
                                "Instala reportlab:\n\npip install reportlab")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar:\n{e}")

    # ── Mostrar pixmap ───────────────────────────────────────────────────────
    def _show_pix(self, pix):
        self.ph.hide()
        self.il.show()
        av = self.img_frame.size() - QSize(30, 30)
        if av.width() < 50 or av.height() < 50:
            av = QSize(300, 240)
        self.il.setPixmap(pix.scaled(av, Qt.AspectRatioMode.KeepAspectRatio,
                                     Qt.TransformationMode.SmoothTransformation))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if self.il.isVisible() and self.il.pixmap() and not self.il.pixmap().isNull():
            if self.cur_path:
                if self.result_img is not None:
                    rgb = cv2.cvtColor(self.result_img, cv2.COLOR_BGR2RGB)
                    h, w, c = rgb.shape
                    qimg = QImage(rgb.data, w, h, w*c, QImage.Format.Format_RGB888)
                    self._show_pix(QPixmap.fromImage(qimg))
                else:
                    self._show_pix(QPixmap(self.cur_path))

# ═══════════════════════════════════════════════════════════════════════════════
# MODAL DE DETALLE DE ENFERMEDAD
# ═══════════════════════════════════════════════════════════════════════════════
class EnfermedadDialog(QDialog):
    def __init__(self, cls, info, parent=None):
        super().__init__(parent)
        self.setWindowTitle(info.get("n", cls))
        self.setMinimumSize(560, 440)
        self.setStyleSheet(f"background:{C_BG};")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Header
        grav = info.get("g", "media")
        gc   = GSEV.get(grav, C_SUB)
        gbg  = GSEV_BG.get(grav, C_CARD2)

        h = QFrame()
        h.setStyleSheet(f"""
            background:{gbg};
            border-bottom:3px solid {gc};
        """)
        hl = QVBoxLayout(h)
        hl.setContentsMargins(24, 20, 24, 20)
        hl.setSpacing(4)

        tag = QLabel(GSEV_LABEL.get(grav, "ENFERMEDAD"))
        tag.setStyleSheet(f"color:{gc}; font-size:10px; font-weight:900; letter-spacing:1.5px;")
        hl.addWidget(tag)

        em = QLabel(f"{info.get('e','🌿')}   {info.get('n', cls)}")
        em.setStyleSheet(f"color:{C_TEXT}; font-size:22px; font-weight:800;")
        hl.addWidget(em)

        cl_lbl = QLabel(cls)
        cl_lbl.setStyleSheet(f"color:{C_SUB}; font-size:11px; font-style:italic;")
        hl.addWidget(cl_lbl)

        lay.addWidget(h)

        # Body
        body = QScrollArea()
        body.setWidgetResizable(True)
        body.setStyleSheet(f"""
            QScrollArea {{ border:none; background:{C_BG}; }}
            QScrollBar:vertical {{ background:{C_BG}; width:8px; border-radius:4px; }}
            QScrollBar::handle:vertical {{ background:{C_BOR}; border-radius:4px; }}
        """)
        inner = QWidget(); inner.setStyleSheet(f"background:{C_BG};")
        il = QVBoxLayout(inner)
        il.setContentsMargins(24, 20, 24, 20)
        il.setSpacing(14)

        # Cultivo afectado
        cult = CLASE_A_CULTIVO.get(cls, "—")
        cult_row = QHBoxLayout()
        cult_row.setSpacing(6)
        cr_lbl = QLabel("Cultivo:")
        cr_lbl.setStyleSheet(f"color:{C_SUB}; font-size:12px;")
        cr_val = QLabel(cult)
        cr_val.setStyleSheet(f"color:{C_ACC}; font-size:12px; font-weight:700;")
        cult_row.addWidget(cr_lbl); cult_row.addWidget(cr_val); cult_row.addStretch()
        il.addLayout(cult_row)

        for icon, titulo, texto, col in [
            ("📖", "Descripción",            info.get("d","—"), "#3b82f6"),
            ("💊", "Tratamiento recomendado", info.get("t","—"), "#ef4444"),
            ("🛡️", "Medidas de prevención",   info.get("p","—"), C_ACC),
        ]:
            card = QFrame()
            card.setStyleSheet(f"""
                background:{C_CARD};
                border-radius:12px;
                border:1px solid {C_BOR};
                border-left:3px solid {col};
            """)
            cl_ = QVBoxLayout(card)
            cl_.setContentsMargins(16, 12, 16, 14)
            cl_.setSpacing(8)

            t_lbl = QLabel(f"{icon}   {titulo}")
            t_lbl.setStyleSheet(f"color:{col}; font-size:12px; font-weight:800; background:transparent; border:none;")
            cl_.addWidget(t_lbl)

            c_lbl = QLabel(texto)
            c_lbl.setStyleSheet(f"color:{C_SUB2}; font-size:12px; background:transparent; border:none; line-height:1.6;")
            c_lbl.setWordWrap(True)
            cl_.addWidget(c_lbl)

            il.addWidget(card)

        body.setWidget(inner)
        lay.addWidget(body, stretch=1)

        # Footer con botón cerrar
        foot = QFrame()
        foot.setStyleSheet(f"background:{C_CARD}; border-top:1px solid {C_BOR};")
        foot.setFixedHeight(56)
        fl = QHBoxLayout(foot)
        fl.setContentsMargins(24, 0, 24, 0)
        fl.addStretch()
        btn = make_button("Cerrar", C_ACC, "#000", "#00ffb3", height=36, width=100)
        btn.clicked.connect(self.close)
        fl.addWidget(btn)
        lay.addWidget(foot)


# ═══════════════════════════════════════════════════════════════════════════════
# PANTALLA CATÁLOGO (con buscador)
# ═══════════════════════════════════════════════════════════════════════════════
class CatalogoScreen(QWidget):
    def __init__(self, app_ref):
        super().__init__()
        self.app_ref = app_ref
        self.setStyleSheet(f"background:{C_BG};")
        self.filtro_texto = ""

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)

        # ── Header fijo ──────────────────────────────────────────────────────
        header = QWidget()
        header.setStyleSheet(f"background:{C_BG};")
        hl = QVBoxLayout(header)
        hl.setContentsMargins(40, 28, 40, 16)
        hl.setSpacing(12)

        badge = QLabel("━━   CULTIVOS SOPORTADOS")
        badge.setStyleSheet(f"color:{C_ACC}; font-size:11px; font-weight:800; letter-spacing:1.5px;")
        hl.addWidget(badge)

        t_row = QHBoxLayout()
        title = QLabel("20 cultivos · 88 enfermedades detectables")
        title.setStyleSheet(f"color:{C_TEXT}; font-size:26px; font-weight:900;")
        t_row.addWidget(title)
        t_row.addStretch()

        btn_xl = make_button("📥  Descargar Excel completo", C_CARD2, C_ACC,
                             "#1e2436", height=40, width=260, border=C_BOR)
        btn_xl.clicked.connect(self.export_excel)
        t_row.addWidget(btn_xl)
        hl.addLayout(t_row)

        # ── Buscador ─────────────────────────────────────────────────────────
        search_row = QHBoxLayout()
        search_row.setSpacing(10)

        search_frame = QFrame()
        search_frame.setStyleSheet(f"""
            background:{C_CARD}; border-radius:10px;
            border:1px solid {C_BOR};
        """)
        sfl = QHBoxLayout(search_frame)
        sfl.setContentsMargins(14, 8, 14, 8)

        icon_lbl = QLabel("🔍")
        icon_lbl.setStyleSheet("font-size:14px; background:transparent; border:none;")
        sfl.addWidget(icon_lbl)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar enfermedad, cultivo o síntoma...")
        self.search.setStyleSheet(f"""
            QLineEdit {{
                background:transparent;
                color:{C_TEXT};
                font-size:13px;
                border:none;
                padding:6px;
            }}
        """)
        self.search.textChanged.connect(self._on_search)
        sfl.addWidget(self.search)
        search_row.addWidget(search_frame, stretch=1)

        # Filtro por gravedad
        self.combo_grav = QComboBox()
        self.combo_grav.addItems(["Todas las gravedades", "✅ Sana", "⚠️ Media", "🚨 Alta", "🔴 Muy alta"])
        self.combo_grav.setFixedHeight(40)
        self.combo_grav.setFixedWidth(200)
        self.combo_grav.setCursor(Qt.CursorShape.PointingHandCursor)
        self.combo_grav.setStyleSheet(f"""
            QComboBox {{
                background:{C_CARD}; color:{C_TEXT};
                border:1px solid {C_BOR}; border-radius:10px;
                padding:0 14px; font-size:12px; font-weight:500;
            }}
            QComboBox:hover {{ border:1px solid {C_ACC}60; }}
            QComboBox::drop-down {{ border:none; width:30px; }}
            QComboBox::down-arrow {{ image:none; }}
            QComboBox QAbstractItemView {{
                background:{C_CARD2}; color:{C_TEXT};
                border:1px solid {C_BOR}; padding:4px;
                selection-background-color:{C_ACC_DK};
            }}
        """)
        self.combo_grav.currentIndexChanged.connect(self._on_search)
        search_row.addWidget(self.combo_grav)

        hl.addLayout(search_row)
        lay.addWidget(header)

        # ── Scroll de cards ──────────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border:none; background:{C_BG}; }}
            QScrollBar:vertical {{ background:{C_BG}; width:8px; border-radius:4px; }}
            QScrollBar::handle:vertical {{ background:{C_BOR}; border-radius:4px; }}
            QScrollBar::handle:vertical:hover {{ background:{C_ACC}; }}
        """)
        self.inner = QWidget()
        self.inner.setStyleSheet(f"background:{C_BG};")
        self.inner_lay = QVBoxLayout(self.inner)
        self.inner_lay.setContentsMargins(40, 4, 40, 40)
        self.inner_lay.setSpacing(14)

        self._build_grid()

        scroll.setWidget(self.inner)
        lay.addWidget(scroll)

    def _build_grid(self):
        # Limpiar
        for i in reversed(range(self.inner_lay.count())):
            it = self.inner_lay.itemAt(i)
            wid = it.widget()
            if wid: wid.deleteLater()

        filtro = self.filtro_texto.lower().strip()
        grav_idx = self.combo_grav.currentIndex()
        grav_map = {1:"ninguna", 2:"media", 3:"alta", 4:"muy alta"}
        grav_filter = grav_map.get(grav_idx)

        # Si hay filtro, mostrar enfermedades directamente (lista)
        if filtro or grav_filter:
            matches = []
            for cls, inf in INFO.items():
                nombre = inf.get("n","").lower()
                cultivo = CLASE_A_CULTIVO.get(cls,"").lower()
                desc = inf.get("d","").lower()
                cum_text = (filtro in cls.lower() or filtro in nombre or
                            filtro in cultivo or filtro in desc) if filtro else True
                cum_grav = (inf.get("g") == grav_filter) if grav_filter else True
                if cum_text and cum_grav:
                    matches.append((cls, inf))

            count_lbl = QLabel(f"{len(matches)} resultado(s) encontrado(s)")
            count_lbl.setStyleSheet(f"color:{C_SUB}; font-size:12px; font-weight:500;")
            self.inner_lay.addWidget(count_lbl)

            if not matches:
                ph = QFrame()
                ph.setStyleSheet(f"background:{C_CARD}; border-radius:12px; border:1px solid {C_BOR};")
                ph.setFixedHeight(180)
                phl = QVBoxLayout(ph)
                msg1 = QLabel("🔎")
                msg1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                msg1.setStyleSheet("font-size:36px; border:none; background:transparent;")
                msg2 = QLabel("No se encontraron resultados")
                msg2.setAlignment(Qt.AlignmentFlag.AlignCenter)
                msg2.setStyleSheet(f"color:{C_SUB}; font-size:13px; border:none; background:transparent;")
                phl.addWidget(msg1); phl.addWidget(msg2)
                self.inner_lay.addWidget(ph)
                self.inner_lay.addStretch()
                return

            # Grid de enfermedades
            grid = QGridLayout()
            grid.setSpacing(12)
            for i, (cls, inf) in enumerate(matches):
                card = self._enfermedad_card(cls, inf)
                grid.addWidget(card, i // 2, i % 2)
            self.inner_lay.addLayout(grid)
        else:
            # Grid normal de cultivos
            grid = QGridLayout()
            grid.setSpacing(14)
            row = col = 0
            for nombre, data in CULTIVOS.items():
                card = self._cultivo_card(nombre, data)
                grid.addWidget(card, row, col)
                col += 1
                if col == 4: col = 0; row += 1
            self.inner_lay.addLayout(grid)

        self.inner_lay.addStretch()

    def _on_search(self):
        self.filtro_texto = self.search.text()
        self._build_grid()

    def _cultivo_card(self, nombre, data):
        clss = data["cls"]
        enfs = [INFO[c] for c in clss if c in INFO]
        n_diseases = len([e for e in enfs if e.get("g") != "ninguna"])

        card = QFrame()
        card.setStyleSheet(f"""
            background:{C_CARD};
            border-radius:14px;
            border:1px solid {C_BOR};
        """)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setMinimumHeight(150)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(6)

        em = QLabel(data["e"])
        em.setStyleSheet("font-size:32px; border:none; background:transparent;")
        lay.addWidget(em)

        nm = QLabel(nombre)
        nm.setStyleSheet(f"color:{C_TEXT}; font-size:16px; font-weight:800; border:none; background:transparent;")
        lay.addWidget(nm)

        nc_row = QHBoxLayout(); nc_row.setSpacing(6)
        nc_chip = QLabel(f"{len(clss)}  condiciones")
        nc_chip.setStyleSheet(f"""
            color:{C_ACC}; font-size:11px; font-weight:700;
            background:{C_ACC_DK}; padding:3px 8px;
            border-radius:8px; border:none;
        """)
        nc_row.addWidget(nc_chip)
        nc_row.addStretch()
        lay.addLayout(nc_row)

        # Preview
        enf_names = [e["n"] for e in enfs if e.get("g") != "ninguna"]
        if enf_names:
            preview = ", ".join(enf_names[:2])
            if len(enf_names) > 2: preview += "..."
        else:
            preview = "Solo estado saludable"
        pv = QLabel(preview)
        pv.setStyleSheet(f"color:{C_SUB}; font-size:11px; border:none; background:transparent;")
        pv.setWordWrap(True)
        lay.addWidget(pv)
        lay.addStretch()

        # Ver más
        more = QLabel("Ver detalle →")
        more.setStyleSheet(f"color:{C_ACC}; font-size:11px; font-weight:700; border:none; background:transparent;")
        lay.addWidget(more)

        card.mousePressEvent = lambda e, n=nombre: self._show_cultivo_detail(n)
        return card

    def _enfermedad_card(self, cls, inf):
        grav = inf.get("g","media")
        gc = GSEV.get(grav, C_SUB)

        card = QFrame()
        card.setStyleSheet(f"""
            background:{C_CARD};
            border-radius:12px;
            border:1px solid {C_BOR};
            border-left:4px solid {gc};
        """)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setMinimumHeight(100)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 12, 16, 14)
        lay.setSpacing(6)

        # Header
        top = QHBoxLayout()
        em = QLabel(inf.get("e","🌿"))
        em.setStyleSheet("font-size:20px; border:none; background:transparent;")
        top.addWidget(em)

        nm_box = QVBoxLayout(); nm_box.setSpacing(2)
        nm = QLabel(inf.get("n", cls))
        nm.setStyleSheet(f"color:{C_TEXT}; font-size:13px; font-weight:700; border:none; background:transparent;")
        cult = CLASE_A_CULTIVO.get(cls, "")
        cl = QLabel(f"{cult}  ·  {grav.upper()}")
        cl.setStyleSheet(f"color:{gc}; font-size:10px; font-weight:600; border:none; background:transparent;")
        nm_box.addWidget(nm); nm_box.addWidget(cl)
        top.addLayout(nm_box)
        top.addStretch()
        lay.addLayout(top)

        # Descripción corta
        desc = inf.get("d", "")
        if len(desc) > 100: desc = desc[:100] + "..."
        d_lbl = QLabel(desc)
        d_lbl.setStyleSheet(f"color:{C_SUB}; font-size:11px; border:none; background:transparent; line-height:1.5;")
        d_lbl.setWordWrap(True)
        lay.addWidget(d_lbl)

        card.mousePressEvent = lambda e, c=cls, i=inf: self._show_enfermedad_detail(c, i)
        return card

    def _show_enfermedad_detail(self, cls, inf):
        dlg = EnfermedadDialog(cls, inf, self)
        dlg.exec()

    def _show_cultivo_detail(self, nombre):
        data = CULTIVOS[nombre]
        # Mostrar lista de enfermedades del cultivo
        dlg = QDialog(self)
        dlg.setWindowTitle(f"{data['e']}  {nombre}")
        dlg.setMinimumSize(560, 500)
        dlg.setStyleSheet(f"background:{C_BG};")

        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(0,0,0,0)
        lay.setSpacing(0)

        # Header
        h = QFrame()
        h.setStyleSheet(f"background:{C_ACC_DK}; border-bottom:2px solid {C_ACC};")
        hl = QVBoxLayout(h)
        hl.setContentsMargins(24, 18, 24, 18)
        hl.setSpacing(4)

        em = QLabel(f"{data['e']}   {nombre}")
        em.setStyleSheet(f"color:{C_TEXT}; font-size:24px; font-weight:900;")
        hl.addWidget(em)

        cnt = QLabel(f"{len(data['cls'])} condiciones detectables")
        cnt.setStyleSheet(f"color:{C_ACC}; font-size:12px; font-weight:700;")
        hl.addWidget(cnt)

        lay.addWidget(h)

        # Lista
        body = QScrollArea(); body.setWidgetResizable(True)
        body.setStyleSheet(f"QScrollArea {{ border:none; background:{C_BG}; }}")
        inner = QWidget(); inner.setStyleSheet(f"background:{C_BG};")
        il = QVBoxLayout(inner)
        il.setContentsMargins(20, 20, 20, 20)
        il.setSpacing(10)

        for c in data["cls"]:
            if c in INFO:
                card = self._enfermedad_card(c, INFO[c])
                il.addWidget(card)

        body.setWidget(inner)
        lay.addWidget(body, stretch=1)

        # Footer
        foot = QFrame()
        foot.setStyleSheet(f"background:{C_CARD}; border-top:1px solid {C_BOR};")
        foot.setFixedHeight(56)
        fl = QHBoxLayout(foot); fl.setContentsMargins(24, 0, 24, 0)
        fl.addStretch()
        btn = make_button("Cerrar", C_ACC, "#000", "#00ffb3", height=36, width=100)
        btn.clicked.connect(dlg.close)
        fl.addWidget(btn)
        lay.addWidget(foot)

        dlg.exec()

    def export_excel(self):
        try:
            import openpyxl
        except ImportError:
            QMessageBox.warning(self, "Falta librería", "Instala openpyxl:\n\npip install openpyxl")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar catálogo Excel",
            f"nexro_catalogo_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx",
            "Excel (*.xlsx)"
        )
        if not path: return
        try:
            exportar_catalogo_excel(path, INFO, CULTIVOS, CLASE_A_CULTIVO)
            QMessageBox.information(self, "Excel generado",
                                    f"✓ Catálogo exportado correctamente:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar:\n{e}")


# ═══════════════════════════════════════════════════════════════════════════════
# PANTALLA HISTORIAL
# ═══════════════════════════════════════════════════════════════════════════════
class HistorialScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background:{C_BG};")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)

        # Header
        header = QWidget(); header.setStyleSheet(f"background:{C_BG};")
        hl = QVBoxLayout(header)
        hl.setContentsMargins(40, 28, 40, 16)
        hl.setSpacing(8)

        badge = QLabel("━━   HISTORIAL DE ANÁLISIS")
        badge.setStyleSheet(f"color:{C_ACC}; font-size:11px; font-weight:800; letter-spacing:1.5px;")
        hl.addWidget(badge)

        t_row = QHBoxLayout()
        title = QLabel("Últimos diagnósticos realizados")
        title.setStyleSheet(f"color:{C_TEXT}; font-size:26px; font-weight:900;")
        t_row.addWidget(title)
        t_row.addStretch()

        btn_clear = make_button("🗑  Limpiar historial", C_CARD2, C_DANGER,
                                "#2a0a0a", height=38, width=200, border=C_BOR)
        btn_clear.clicked.connect(self._clear)
        t_row.addWidget(btn_clear)
        hl.addLayout(t_row)

        sub = QLabel("Los últimos 15 análisis se guardan automáticamente")
        sub.setStyleSheet(f"color:{C_SUB}; font-size:12px;")
        hl.addWidget(sub)

        lay.addWidget(header)

        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border:none; background:{C_BG}; }}
            QScrollBar:vertical {{ background:{C_BG}; width:8px; border-radius:4px; }}
            QScrollBar::handle:vertical {{ background:{C_BOR}; border-radius:4px; }}
        """)
        self.inner = QWidget(); self.inner.setStyleSheet(f"background:{C_BG};")
        self.inner_lay = QVBoxLayout(self.inner)
        self.inner_lay.setContentsMargins(40, 8, 40, 40)
        self.inner_lay.setSpacing(10)

        scroll.setWidget(self.inner)
        lay.addWidget(scroll)

        self.refresh()

    def refresh(self):
        for i in reversed(range(self.inner_lay.count())):
            wid = self.inner_lay.itemAt(i).widget()
            if wid: wid.deleteLater()

        hist = cargar_historial()
        if not hist:
            ph = QFrame()
            ph.setStyleSheet(f"background:{C_CARD}; border-radius:12px; border:1px solid {C_BOR};")
            ph.setMinimumHeight(220)
            phl = QVBoxLayout(ph)
            phl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ic = QLabel("🗂"); ic.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ic.setStyleSheet("font-size:48px; border:none; background:transparent;")
            t1 = QLabel("Aún no hay análisis"); t1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            t1.setStyleSheet(f"color:{C_TEXT}; font-size:15px; font-weight:700; border:none; background:transparent;")
            t2 = QLabel("Los análisis que realices aparecerán aquí")
            t2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            t2.setStyleSheet(f"color:{C_SUB}; font-size:12px; border:none; background:transparent;")
            phl.addWidget(ic); phl.addWidget(t1); phl.addWidget(t2)
            self.inner_lay.addWidget(ph)
            self.inner_lay.addStretch()
            return

        for item in hist:
            self.inner_lay.addWidget(self._hist_card(item))
        self.inner_lay.addStretch()

    def _hist_card(self, item):
        cls = item.get("clase","")
        conf = item.get("conf", 0)
        fecha = item.get("fecha","")
        inf = INFO.get(cls, {})
        grav = inf.get("g","media")
        gc = GSEV.get(grav, C_SUB)

        try:
            f = datetime.datetime.fromisoformat(fecha)
            fecha_str = f.strftime("%d/%m/%Y  %H:%M")
        except:
            fecha_str = fecha

        card = QFrame()
        card.setStyleSheet(f"""
            background:{C_CARD};
            border-radius:12px;
            border:1px solid {C_BOR};
            border-left:4px solid {gc};
        """)
        card.setFixedHeight(86)
        lay = QHBoxLayout(card)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(14)

        # Thumbnail
        thumb = QLabel()
        thumb.setFixedSize(60, 60)
        thumb.setStyleSheet(f"background:{C_BG2}; border-radius:8px; border:1px solid {C_BOR};")
        thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_path = item.get("imagen","")
        if os.path.exists(img_path):
            pix = QPixmap(img_path).scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                          Qt.TransformationMode.SmoothTransformation)
            thumb.setPixmap(pix)
        else:
            thumb.setText(inf.get("e","🌿"))
            thumb.setStyleSheet(f"background:{C_BG2}; border-radius:8px; border:1px solid {C_BOR}; font-size:24px;")
        lay.addWidget(thumb)

        # Info
        info_box = QVBoxLayout(); info_box.setSpacing(2)
        nm = QLabel(f"{inf.get('e','🌿')}  {inf.get('n', cls)}")
        nm.setStyleSheet(f"color:{C_TEXT}; font-size:13px; font-weight:700; background:transparent; border:none;")
        det = QLabel(f"{fecha_str}  ·  {CLASE_A_CULTIVO.get(cls,'—')}")
        det.setStyleSheet(f"color:{C_SUB}; font-size:11px; background:transparent; border:none;")
        info_box.addWidget(nm); info_box.addWidget(det)
        lay.addLayout(info_box)
        lay.addStretch()

        # Confianza
        conf_lbl = QLabel(f"{conf*100:.1f}%")
        conf_lbl.setStyleSheet(f"color:{gc}; font-size:18px; font-weight:900; background:transparent; border:none;")
        lay.addWidget(conf_lbl)

        grav_chip = QLabel(f"  {grav.upper()}  ")
        grav_chip.setStyleSheet(f"""
            color:{gc}; font-size:9px; font-weight:800;
            background:{C_BG2}; padding:3px 6px; border-radius:6px;
            border:1px solid {gc}40;
        """)
        lay.addWidget(grav_chip)

        return card

    def _clear(self):
        r = QMessageBox.question(self, "Limpiar historial",
                                 "¿Seguro que deseas borrar todo el historial?",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if r == QMessageBox.StandardButton.Yes:
            limpiar_historial()
            self.refresh()

# ═══════════════════════════════════════════════════════════════════════════════
# DIÁLOGO ACERCA DE
# ═══════════════════════════════════════════════════════════════════════════════
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de Nexro Plant AI")
        self.setFixedSize(480, 520)
        self.setStyleSheet(f"background:{C_BG};")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        lay.setSpacing(0)

        # Header con gradient
        h = QFrame()
        h.setFixedHeight(160)
        h.setStyleSheet(f"""
            background:qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {C_ACC_DK}, stop:1 {C_BG2});
            border-bottom:2px solid {C_ACC};
        """)
        hl = QVBoxLayout(h)
        hl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        em = QLabel("🌿")
        em.setAlignment(Qt.AlignmentFlag.AlignCenter)
        em.setStyleSheet("font-size:48px; background:transparent;")
        hl.addWidget(em)

        name = QLabel("Nexro Plant AI")
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name.setStyleSheet(f"color:{C_TEXT}; font-size:22px; font-weight:900; background:transparent;")
        hl.addWidget(name)

        ver = QLabel(f"Versión {APP_VERSION}")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ver.setStyleSheet(f"color:{C_ACC}; font-size:12px; font-weight:700; background:transparent;")
        hl.addWidget(ver)

        lay.addWidget(h)

        # Body
        body = QWidget(); body.setStyleSheet(f"background:{C_BG};")
        bl = QVBoxLayout(body)
        bl.setContentsMargins(28, 24, 28, 20)
        bl.setSpacing(14)

        desc = QLabel("Sistema de diagnóstico inteligente de enfermedades en cultivos mediante visión por computador y deep learning.")
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color:{C_SUB2}; font-size:12px; line-height:1.6;")
        bl.addWidget(desc)

        # Specs
        specs = QFrame()
        specs.setStyleSheet(f"background:{C_CARD}; border-radius:10px; border:1px solid {C_BOR};")
        sl = QVBoxLayout(specs); sl.setContentsMargins(16, 12, 16, 14); sl.setSpacing(6)

        for k, v in [
            ("Modelo",     "YOLOv8 (clasificación)"),
            ("Clases",     "88 enfermedades"),
            ("Cultivos",   "20 cultivos soportados"),
            ("Precisión",  "93.7% (validación)"),
            ("Dataset",    "79,087 imágenes reales de campo"),
            ("Framework",  "PyQt6 · Ultralytics · OpenCV"),
        ]:
            r = QHBoxLayout()
            kl = QLabel(k); kl.setStyleSheet(f"color:{C_SUB}; font-size:11px; background:transparent; border:none;")
            vl = QLabel(v); vl.setStyleSheet(f"color:{C_TEXT}; font-size:11px; font-weight:600; background:transparent; border:none;")
            r.addWidget(kl); r.addStretch(); r.addWidget(vl)
            sl.addLayout(r)

        bl.addWidget(specs)

        # Contacto
        contact = QLabel(
            "Nexro Systems © 2026\n"
            "nexrosystems@gmail.com  ·  +57 321 521 7396"
        )
        contact.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contact.setStyleSheet(f"color:{C_SUB}; font-size:11px; line-height:1.6;")
        bl.addWidget(contact)

        btn = make_button("Cerrar", C_ACC, "#000", "#00ffb3", height=40, width=120)
        btn.clicked.connect(self.close)
        btn_row = QHBoxLayout(); btn_row.addStretch(); btn_row.addWidget(btn); btn_row.addStretch()
        bl.addLayout(btn_row)

        lay.addWidget(body)


# ═══════════════════════════════════════════════════════════════════════════════
# VENTANA PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
class NexroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = None
        self.setWindowTitle(f"Nexro Plant AI  |  Diagnóstico Inteligente de Cultivos  ·  v{APP_VERSION}")
        self.setMinimumSize(1280, 780)
        self.resize(1400, 880)

        p = self.palette()
        p.setColor(QPalette.ColorRole.Window, QColor(C_BG))
        self.setPalette(p)

        self._build_ui()
        self._setup_shortcuts()

    # ── Build UI ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        root = QWidget()
        root.setStyleSheet(f"background:{C_BG};")
        self.setCentralWidget(root)
        main = QVBoxLayout(root)
        main.setContentsMargins(0,0,0,0)
        main.setSpacing(0)

        main.addWidget(self._build_header())

        self.stack = QStackedWidget()

        self.home_screen      = HomeScreen()
        self.analisis_screen  = AnalisisScreen(lambda: self.model, self)
        self.catalogo_screen  = CatalogoScreen(self)
        self.historial_screen = HistorialScreen()

        self.stack.addWidget(self.home_screen)       # 0
        self.stack.addWidget(self.analisis_screen)   # 1
        self.stack.addWidget(self.catalogo_screen)   # 2
        self.stack.addWidget(self.historial_screen)  # 3

        self.home_screen.go_analisis.connect(lambda: self._nav(1))
        self.home_screen.go_catalogo.connect(lambda: self._nav(2))
        self.analisis_screen.analisis_completado.connect(
            lambda item: self.historial_screen.refresh()
        )

        main.addWidget(self.stack, stretch=1)
        main.addWidget(self._build_footer())

    def _build_header(self):
        h = QFrame()
        h.setFixedHeight(64)
        h.setStyleSheet(f"""
            background:{C_CARD};
            border-bottom:1px solid {C_BOR};
        """)
        lay = QHBoxLayout(h)
        lay.setContentsMargins(28, 0, 28, 0)
        lay.setSpacing(0)

        # Logo
        logo_row = QHBoxLayout()
        logo_row.setSpacing(10)
        dot = QLabel("🌿")
        dot.setStyleSheet("font-size:24px;")
        logo = QVBoxLayout()
        logo.setSpacing(0)
        title = QLabel("Nexro Plant AI")
        title.setStyleSheet(f"color:{C_TEXT}; font-size:17px; font-weight:900; letter-spacing:-0.3px;")
        subt = QLabel("Diagnóstico Inteligente")
        subt.setStyleSheet(f"color:{C_SUB}; font-size:10px;")
        logo.addWidget(title); logo.addWidget(subt)
        logo_row.addWidget(dot); logo_row.addLayout(logo)
        lay.addLayout(logo_row)

        lay.addSpacing(40)

        # Nav
        self.nav_btns = []
        nav_items = [
            ("🏠",  "Inicio",     0),
            ("🔬",  "Analizar",   1),
            ("📚",  "Catálogo",   2),
            ("🗂",  "Historial",  3),
        ]
        for icon, label, idx in nav_items:
            btn = QPushButton(f"{icon}   {label}")
            btn.setFixedHeight(38)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(self._nav_style(idx == 0))
            btn.clicked.connect(lambda _, i=idx: self._nav(i))
            self.nav_btns.append(btn)
            lay.addWidget(btn)
            lay.addSpacing(4)

        lay.addStretch()

        # Badge modelo
        self.badge = QLabel("⏳ Cargando modelo...")
        self.badge.setStyleSheet(f"""
            color:{C_SUB}; font-size:11px; font-weight:600;
            padding:6px 14px;
            background:{C_CARD2}; border-radius:14px;
            border:1px solid {C_BOR};
        """)
        lay.addWidget(self.badge)

        lay.addSpacing(10)

        # Menú ⋮
        menu_btn = QPushButton("⋮")
        menu_btn.setFixedSize(34, 34)
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_btn.setStyleSheet(f"""
            QPushButton {{
                background:{C_CARD2}; color:{C_SUB};
                border-radius:10px; font-size:18px;
                font-weight:900; border:1px solid {C_BOR};
            }}
            QPushButton:hover {{ color:{C_ACC}; border:1px solid {C_ACC}40; }}
        """)
        menu_btn.clicked.connect(self._show_menu)
        lay.addWidget(menu_btn)

        return h

    def _nav_style(self, active):
        if active:
            return f"""
                QPushButton {{
                    background:{C_ACC_DK}; color:{C_ACC};
                    border-radius:10px; font-size:13px; font-weight:700;
                    border:1px solid {C_ACC}50; padding:0 18px;
                }}
            """
        return f"""
            QPushButton {{
                background:transparent; color:{C_SUB};
                border-radius:10px; font-size:13px; font-weight:500;
                border:none; padding:0 18px;
            }}
            QPushButton:hover {{
                color:{C_TEXT}; background:{C_CARD2};
            }}
        """

    def _build_footer(self):
        f = QFrame()
        f.setFixedHeight(32)
        f.setStyleSheet(f"""
            background:{C_CARD};
            border-top:1px solid {C_BOR};
        """)
        lay = QHBoxLayout(f)
        lay.setContentsMargins(24, 0, 24, 0)

        self.status = QLabel("Listo  ·  Nexro Systems  ·  v" + APP_VERSION)
        self.status.setStyleSheet(f"color:{C_SUB}; font-size:11px;")

        hint = QLabel("⌨  Ctrl+O abrir  ·  Ctrl+S guardar  ·  Ctrl+E Excel  ·  Ctrl+P PDF")
        hint.setStyleSheet(f"color:{C_SUB}; font-size:10px;")

        ver = QLabel("YOLOv8  ·  88 clases  ·  93.7%")
        ver.setStyleSheet(f"color:{C_ACC}; font-size:10px; font-weight:700;")

        lay.addWidget(self.status)
        lay.addStretch()
        lay.addWidget(hint)
        lay.addSpacing(20)
        lay.addWidget(ver)
        return f

    def _nav(self, idx):
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_btns):
            btn.setStyleSheet(self._nav_style(i == idx))
        if idx == 3:
            self.historial_screen.refresh()

    # ── Menú ─────────────────────────────────────────────────────────────────
    def _show_menu(self):
        m = QMenu(self)
        m.setStyleSheet(f"""
            QMenu {{
                background:{C_CARD2}; color:{C_TEXT};
                border:1px solid {C_BOR}; border-radius:8px;
                padding:6px;
            }}
            QMenu::item {{
                padding:8px 20px 8px 12px; border-radius:6px;
            }}
            QMenu::item:selected {{
                background:{C_ACC_DK}; color:{C_ACC};
            }}
        """)

        a_open = QAction("📂  Cargar imagen      Ctrl+O", self)
        a_open.triggered.connect(lambda: (self._nav(1), self.analisis_screen.load_image()))
        m.addAction(a_open)

        a_excel = QAction("📊  Exportar Excel      Ctrl+E", self)
        a_excel.triggered.connect(self._export_excel_shortcut)
        m.addAction(a_excel)

        a_pdf = QAction("📄  Exportar PDF        Ctrl+P", self)
        a_pdf.triggered.connect(self._export_pdf_shortcut)
        m.addAction(a_pdf)

        m.addSeparator()

        a_about = QAction("ℹ  Acerca de", self)
        a_about.triggered.connect(self._show_about)
        m.addAction(a_about)

        a_quit = QAction("✕  Salir                        Ctrl+Q", self)
        a_quit.triggered.connect(self.close)
        m.addAction(a_quit)

        pos = self.sender().mapToGlobal(QPoint(0, self.sender().height()+4))
        m.exec(pos)

    def _show_about(self):
        d = AboutDialog(self)
        d.exec()

    def _export_excel_shortcut(self):
        if self.analisis_screen.last_analysis:
            self._nav(1)
            self.analisis_screen.export_excel()
        else:
            QMessageBox.information(self, "Sin análisis",
                                    "Primero realiza un análisis para exportar.")

    def _export_pdf_shortcut(self):
        if self.analisis_screen.last_analysis:
            self._nav(1)
            self.analisis_screen.export_pdf()
        else:
            QMessageBox.information(self, "Sin análisis",
                                    "Primero realiza un análisis para exportar.")

    # ── Atajos ───────────────────────────────────────────────────────────────
    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+O"), self, activated=lambda: (self._nav(1), self.analisis_screen.load_image()))
        QShortcut(QKeySequence("Ctrl+S"), self, activated=lambda: self.analisis_screen.save_image() if self.analisis_screen.result_img is not None else None)
        QShortcut(QKeySequence("Ctrl+E"), self, activated=self._export_excel_shortcut)
        QShortcut(QKeySequence("Ctrl+P"), self, activated=self._export_pdf_shortcut)
        QShortcut(QKeySequence("Ctrl+Q"), self, activated=self.close)
        QShortcut(QKeySequence("F1"),     self, activated=self._show_about)
        QShortcut(QKeySequence("Ctrl+1"), self, activated=lambda: self._nav(0))
        QShortcut(QKeySequence("Ctrl+2"), self, activated=lambda: self._nav(1))
        QShortcut(QKeySequence("Ctrl+3"), self, activated=lambda: self._nav(2))
        QShortcut(QKeySequence("Ctrl+4"), self, activated=lambda: self._nav(3))

    # ── Carga de modelo ──────────────────────────────────────────────────────
    def load_model(self):
        try:
            self.model = YOLO(MODEL_PATH)
            self.badge.setText("✓   Modelo v3   ·   88 clases   ·   Listo")
            self.badge.setStyleSheet(f"""
                color:{C_ACC}; font-size:11px; font-weight:700;
                padding:6px 14px;
                background:{C_ACC_DK}; border-radius:14px;
                border:1px solid {C_ACC}40;
            """)
            self.status.setText("✓  Modelo cargado correctamente  ·  Nexro Systems")
        except Exception as e:
            self.badge.setText("✕  Error al cargar modelo")
            self.badge.setStyleSheet(f"""
                color:{C_DANGER}; font-size:11px; font-weight:700;
                padding:6px 14px;
                background:#2a0a0a; border-radius:14px;
                border:1px solid {C_DANGER}40;
            """)
            self.status.setText(f"Error: {e}")
            QMessageBox.critical(self, "Error de modelo",
                                 f"No se pudo cargar best.pt:\n{e}\n\n"
                                 f"Asegúrate de tener el archivo en:\n{MODEL_PATH}")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # ── Registrar ID único ANTES de crear QApplication ──────────────────────
    # Esto le dice a Windows que esta app es "su propia app" y debe usar su ícono
    try:
        import ctypes
        myappid = 'nexrosystems.plantai.app.3.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    app.setApplicationName("Nexro Plant AI")
    app.setOrganizationName("Nexro Systems")

    # ── Cargar ícono (funciona en desarrollo y en .exe compilado) ───────────
    def _resource_path(rel):
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, rel)
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), rel)

    icon_path = _resource_path("nexro.ico")
    app_icon = None
    if os.path.exists(icon_path):
        from PyQt6.QtGui import QIcon
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)

    # Splash
    splash = SplashScreen()
    if app_icon:
        splash.setWindowIcon(app_icon)
    splash.show()
    app.processEvents()

    window = NexroApp()
    if app_icon:
        window.setWindowIcon(app_icon)

    def finish_splash():
        window.load_model()
        window.show()
        splash.finish(window)

    QTimer.singleShot(400, finish_splash)
    sys.exit(app.exec())