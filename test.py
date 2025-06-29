from PyQt5 import QtWidgets, QtGui, QtCore
from myGUI import Ui_Form  # Match this with your actual class name in myGUI.py

class ZoomableWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zoomable Scrollable UI")
        self.resize(1200, 800)

        self.ui_container = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.ui_container)
        self.ui_container.setFixedSize(2500, 1200)

        scene = QtWidgets.QGraphicsScene(self)
        self.proxy = scene.addWidget(self.ui_container)

        self.view = QtWidgets.QGraphicsView(scene, self)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.view.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.view.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setCentralWidget(self.view)

        self.scale_factor = 1.0
        self.apply_zoom()

        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl++"), self, self.zoom_in)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+-"), self, self.zoom_out)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+0"), self, self.reset_zoom)

        self.ui.etcBtn.clicked.connect(self.etcBtnClicked)
        self.ui.adcBtn.clicked.connect(self.adcBtnClicked)

        self.view.viewport().installEventFilter(self)

    def etcBtnClicked(self):
        print("ETC button clicked!")

    def adcBtnClicked(self):
        print("Adc btn clicked")

    def apply_zoom(self):
        self.view.resetTransform()
        self.view.scale(self.scale_factor, self.scale_factor)

    def zoom_in(self):
        self.change_zoom(1.1)

    def zoom_out(self):
        self.change_zoom(1 / 1.1)

    def reset_zoom(self):
        self.scale_factor = 1.0
        self.apply_zoom()

    def change_zoom(self, factor):
        new_scale = self.scale_factor * factor
        new_scale = max(0.2, min(4.0, new_scale))
        if abs(new_scale - self.scale_factor) > 1e-6:
            self.scale_factor = new_scale
            self.apply_zoom()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Wheel and QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            return True
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ZoomableWindow()
    window.show()
    sys.exit(app.exec_())
