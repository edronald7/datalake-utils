import sys
from PyQt5 import QtWidgets, uic

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('main.ui', self)  # Carga la interfaz desde el archivo .ui
        self.initUI()  # Inicializa los componentes adicionales

    def initUI(self):
        # Aquí puedes conectar señales y realizar otras configuraciones
        self.pushButton.clicked.connect(self.on_button_click)  # Ejemplo de conexión de un botón

    def on_button_click(self):
        # Función que se ejecuta cuando se presiona el botón
        print("Botón presionado")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
