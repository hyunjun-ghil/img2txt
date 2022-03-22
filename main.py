import sys, os, time, datetime


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore, uic

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract


# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

main_class = uic.loadUiType(resource_path("img2txt.ui"))[0]
image = resource_path("1.png")

# 영어 인식
# print(pytesseract.image_to_string(Image.open('english.png')))
class MainWindow(QMainWindow, main_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("img2txt")
        self.loadPicBtn.clicked.connect(self.loadImageFromFile)
        self.convertBtn.clicked.connect(self.convertImg2Txt)

    def loadImageFromFile(self):
        fname = QFileDialog.getOpenFileName(self, "Open Image", "", "All File(*);; Image File(*.png *.jpg")

        if fname[0]:
            self.qPixmapFileVar = QPixmap(fname[0])
            self.qPixmapFileVar.load(fname[0])
            self.qPixmapFileVar.save("SavedImage.jpg")

            self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(600)
            self.smaller_pixmap = self.qPixmapFileVar.scaled(281, 381, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
            self.lbl_picture.setPixmap(self.smaller_pixmap)

        else:
            QMessageBox.about(self, "Warning", "파일을 선택하지 않았습니다.")

    def convertImg2Txt(self):
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract'
        print(pytesseract.image_to_string(Image.open("SavedImage.jpg"), lang='kor+eng'))

        file = open("result.txt", "w", encoding="utf-8")
        result =(pytesseract.image_to_string(Image.open("SavedImage.jpg"), lang='kor+eng'))
        file.write(result)
        file.close()

        QMessageBox.information(self, "result", "저장되었습니다.")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()