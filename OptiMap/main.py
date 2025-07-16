import sys
from PyQt5.QtWidgets import QApplication
from interfaz import OptiMapWindow

def main():
    app = QApplication(sys.argv)
    ventana = OptiMapWindow()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
