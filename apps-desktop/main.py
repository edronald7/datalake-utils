import sys
import pandas as pd
from PyQt5 import QtWidgets, uic

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('main.ui', self)  # Carga la interfaz desde el archivo .ui
        self.initUI()  # Inicializa los componentes adicionales

    def initUI(self):
        # Aquí puedes conectar señales y realizar otras configuraciones
        self.actionOpenCSVFile.triggered.connect(self.open_csv_file)  # Ejemplo de conexión de un botón
        

    def open_csv_file(self):
        self.set_status("Select file...")
        path_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt) and CSV (*.csv)')[0]
        if path_file:
            self.dataframe = pd.read_csv(path_file, sep=',')
            self.set_status_total_records()
            self.show_data()

    def show_data(self):
        # Clean tableWidget
        self.tableWidget.clear()

        limit_rows = self.spinLimit.value()
        print("limit rows:", limit_rows)

        self.tableWidget.setColumnCount(self.dataframe.shape[1])
        #self.tableWidget.setRowCount(self.dataframe.shape[0])
        self.tableWidget.setRowCount(limit_rows)
        self.tableWidget.setHorizontalHeaderLabels(self.dataframe.columns)

        self.progressBar.setValue(0)
        for i in range(self.dataframe.shape[0]):
            if i >= limit_rows:
                break
            for j in range(self.dataframe.shape[1]):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(self.dataframe.iloc[i, j])))
            
            #self.progressBar.setValue(i+1)
    
    def set_status_total_records(self):
        if not hasattr(self, 'dataframe'):
            return
        # Si no esta vacia la variable dataframe:
        if self.dataframe.empty:
            self.set_status("No records")
        else:
            # Numero con ##,###,###,###
            self.set_status("Total records: {:,}".format(self.dataframe.shape[0]))

    def set_status(self, message):
        self.labelStatus.setText(message)
        

    def on_button_click(self):
        # Función que se ejecuta cuando se presiona el botón
        print("Botón presionado")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
