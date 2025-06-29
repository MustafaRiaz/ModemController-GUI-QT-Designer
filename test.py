from PyQt5 import QtWidgets, QtCore, QtGui
from myGUI import Ui_Form          # ← change to Ui_Widget / Ui_MainWindow if needed


# ─────────────────────────────────────────────────────────────
# Custom ComboBox without dropdown arrow
# ─────────────────────────────────────────────────────────────
class CustomComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None, items=None):
        super().__init__(parent)
        self.setFont(QtGui.QFont("Segoe UI", 10))
        if items:
            self.addItems(items)

        # Remove arrow; keep text left‑aligned
        self.setStyleSheet("""
            QComboBox { border:none; background:transparent; padding-left:2px;
                        font-weight:bold; qproperty-alignment:AlignLeft|AlignVCenter; }
            QComboBox::drop-down { width:0px; border:none; }
            QComboBox::down-arrow { image:none; width:0px; height:0px; }
            QComboBox QAbstractItemView { font-size:10px; selection-background-color:#dcdcdc; }
        """)
        self.setEditable(False)


# ─────────────────────────────────────────────────────────────
# Main Window
# ─────────────────────────────────────────────────────────────
class ZoomableWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zoomable UI with ComboBoxes & Label Clicks")
        self.resize(1200, 800)

        # 1) Load QWidget‑based Designer UI
        self.ui_container = QtWidgets.QWidget()
        self.ui = Ui_Form()          # Update if your class differs
        self.ui.setupUi(self.ui_container)
        self.ui_container.setFixedSize(2500, 1200)   # original design size

        # 2) Add custom combo boxes into switchFrame* frames
        self.add_comboboxes_to_switch_frames()

        # 3) Graphics View + Scene for zoom / scroll
        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.addWidget(self.ui_container)

        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.view.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.view.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setCentralWidget(self.view)

        # 4) Zoom bookkeeping
        self.scale_factor = 1.0
        self.apply_zoom()

        # 5) Keyboard shortcuts
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl++"), self, self.zoom_in)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+-"), self, self.zoom_out)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+0"), self, self.reset_zoom)

        # 6) Ctrl + wheel zoom
        self.view.viewport().installEventFilter(self)

        # 7) Make QLabel clickable (example tooltip)
        self.add_label_click_detection()

    # ─────────────────────────────────────────────────────────
    # ComboBoxes inside switchFrame*
    # ─────────────────────────────────────────────────────────
    def add_comboboxes_to_switch_frames(self):
        for frame in self.ui_container.findChildren(QtWidgets.QFrame):
            if frame.objectName().startswith("switchFrame"):
                combo = CustomComboBox(frame, items=["rf1", "rf2", "rf3", "rf4"])
                combo.setGeometry(2, 2, frame.width() - 4, frame.height() - 4)

    # ─────────────────────────────────────────────────────────
    # Optional: Make QLabel clickable for demonstration
    # ─────────────────────────────────────────────────────────
    def add_label_click_detection(self):
        for label in self.ui_container.findChildren(QtWidgets.QLabel):
            label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)
            label.installEventFilter(self)

    # ─────────────────────────────────────────────────────────
    # Zoom helpers
    # ─────────────────────────────────────────────────────────
    def apply_zoom(self):
        self.view.resetTransform()
        self.view.scale(self.scale_factor, self.scale_factor)

    def zoom_in(self):
        self.change_zoom(1.1)

    def zoom_out(self):
        self.change_zoom(1 / 1.1)

    def reset_zoom(self):
        """Reset to 100 % and scroll to the top‑left corner."""
        self.scale_factor = 1.0
        self.apply_zoom()

        # Scroll so that (0,0) is visible (top‑left)
        self.view.ensureVisible(0, 0, 1, 1)

    def change_zoom(self, factor):
        new_scale = self.scale_factor * factor
        self.scale_factor = max(0.2, min(4.0, new_scale))
        self.apply_zoom()

    # Optional utility: scroll to any scene coordinate
    def scroll_to_coordinates(self, x, y):
        """Center the view on scene position (x, y)."""
        self.view.centerOn(x, y)

    # ─────────────────────────────────────────────────────────
    # Event filter: ctrl+wheel zoom, label clicks, etc.
    # ─────────────────────────────────────────────────────────
    def eventFilter(self, obj, event):
        # Ctrl + wheel zoom
        if (
            obj is self.view.viewport()
            and event.type() == QtCore.QEvent.Wheel
            and QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ControlModifier
        ):
            self.zoom_in() if event.angleDelta().y() > 0 else self.zoom_out()
            return True

        # Example: tooltip on QLabel click
        if isinstance(obj, QtWidgets.QLabel) and event.type() == QtCore.QEvent.MouseButtonPress:
            QtWidgets.QToolTip.showText(
                obj.mapToGlobal(QtCore.QPoint(0, obj.height())),
                "Label clicked! (example)",
                obj
            )
            return False

        return super().eventFilter(obj, event)


# ─────────────────────────────────────────────────────────────
# Run the application
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ZoomableWindow()
    window.show()
    sys.exit(app.exec_())
