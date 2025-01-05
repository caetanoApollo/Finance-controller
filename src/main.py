from PyQt5 import QtWidgets
from gui.interface import Interface
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    interface = Interface()
    interface.iniciar()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()