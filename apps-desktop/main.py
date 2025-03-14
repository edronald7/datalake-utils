import sys
import yaml
import pandas as pd
from PyQt5 import QtWidgets, uic

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('main.ui', self)  # Carga la interfaz desde el archivo .ui
        self.config = self.load_config()
        self.set_constants()

        self.init_gui()  # Inicializa los componentes visuales

    def load_config(self):
        conf_file = 'main.yaml'
        with open(conf_file, 'r') as file:
            config = yaml.safe_load(file)
        return config
    def set_constants(self):
        self.file_auto_infer_types = self.config['app']['files']['txt-auto-infer-types']
        self.file_encodings = [enc.strip() for enc in self.config['app']['files']['txt-encodings'].split(',')]
        self.file_delimiter = self.config['app']['files']['txt-delimiter']

    def init_gui(self):
        self.setWindowTitle("Datalake Utils")
        self.set_status("No records")
        self.path_file = None
        self.dataframe = pd.DataFrame()
        self.dataindex = 0
        self.datarows = 0
        
        # Aquí puedes conectar señales y realizar otras configuraciones

        self.actionOpenParquetFile.triggered.connect(self.open_file_parquet)
        self.actionOpenCSVGZFile.triggered.connect(self.open_file_csv_gzip)
        self.actionOpenCSVFile.triggered.connect(self.open_file_csv)
        self.actionOpenTXTFile.triggered.connect(self.open_file_txt)

        self.actionCloseAndClean.triggered.connect(self.clear_data)

        self.actionExit.triggered.connect(self.close_window)

        self.btnShow.clicked.connect(self.on_re_show)
        self.btnPagPrevious.clicked.connect(self.on_page_previous)
        self.btnPagNext.clicked.connect(self.on_page_next)


    def close_window(self):
        # Cerrar ventana si confirma con si
        reply = QtWidgets.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.close()
        
    def open_file_parquet(self):
        self.set_status("Select file...")
        path_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'Parquet Files (*.parquet)')[0]
        if path_file:
            self.dataframe = pd.read_parquet(path_file)
            self.set_status_total_records()
            self.show_data()

    def open_file_csv_gzip(self):
        self.set_status("Select file...")
        path_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'CSV Gzip Files (*.csv.gz)')[0]
        if path_file:
            index_encoding = 0
            while index_encoding < len(self.file_encodings):
                try:
                    if self.file_auto_infer_types:
                        self.dataframe = pd.read_csv(path_file, encoding=self.file_encodings[index_encoding], compression='gzip')
                    else:
                        self.dataframe = pd.read_csv(path_file, encoding=self.file_encodings[index_encoding], dtype='str', compression='gzip')
                    break
                except:
                    index_encoding += 1

            self.set_status_total_records()
            self.show_data()

    def open_file_csv(self):
        self.set_status("Select file...")
        path_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files CSV (*.csv)')[0]
        if path_file:
            index_encoding = 0
            while index_encoding < len(self.file_encodings):
                try:
                    if self.file_auto_infer_types:
                        self.dataframe = pd.read_csv(path_file, encoding=self.file_encodings[index_encoding])
                    else:
                        self.dataframe = pd.read_csv(path_file, encoding=self.file_encodings[index_encoding], dtype='str')
                    break
                except:
                    index_encoding += 1

            self.set_status_total_records()
            self.show_data()

    def open_file_txt(self):
        print("Delimitador:", self.file_delimiter)
        self.set_status("Select file...")
        path_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;Text File (*.TXT)')[0]
        if path_file:
            index_encoding = 0
            while index_encoding < len(self.file_encodings):
                try:
                    if self.file_auto_infer_types:
                        self.dataframe = pd.read_csv(path_file, sep=self.file_delimiter, encoding=self.file_encodings[index_encoding])
                    else:
                        self.dataframe = pd.read_csv(path_file, sep=self.file_delimiter, encoding=self.file_encodings[index_encoding], dtype='str')
                    break
                except Exception as ex:
                    print("Error:", ex)
                    index_encoding += 1
            self.set_status_total_records()
            self.show_data()

    def clear_data(self):
        self.dataframe = pd.DataFrame()
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.set_status("No records")

    def show_data(self):
        # Clean tableWidget
        self.tableWidget.clear()

        limit_rows = self.spinLimit.value()

        self.tableWidget.setColumnCount(self.dataframe.shape[1])
        #self.tableWidget.setRowCount(self.dataframe.shape[0])
        self.tableWidget.setRowCount(limit_rows)
        self.tableWidget.setHorizontalHeaderLabels(self.dataframe.columns)

        self.progressBar.setValue(0)

        limit_grid = self.dataindex + limit_rows
        index_grid = 0

        while self.dataindex < self.datarows and self.dataindex < limit_grid:
            for j in range(self.dataframe.shape[1]):
                self.tableWidget.setItem(index_grid, j, QtWidgets.QTableWidgetItem(str(self.dataframe.iloc[self.dataindex, j])))
            
            self.dataindex += 1
            index_grid += 1
            self.progressBar.setValue(int((self.dataindex/self.datarows)*100))
            QtWidgets.QApplication.processEvents()
        
        self.set_count_showing()

    def fill_table(self):
        limit_rows = self.spinLimit.value()
        limit_index = self.dataindex + limit_rows
        while self.dataindex < self.datarows and self.dataindex < limit_index:
            for j in range(self.dataframe.shape[1]):
                self.tableWidget.setItem(self.dataindex, j, QtWidgets.QTableWidgetItem(str(self.dataframe.iloc[self.dataindex, j])))
            
            self.dataindex += 1
            self.progressBar.setValue(int((self.dataindex/self.datarows)*100))
            QtWidgets.QApplication.processEvents()

    def on_page_previous(self):
        limit_rows = self.spinLimit.value()
        if self.datarows and self.dataindex > 0 and self.dataindex-limit_rows*2 >= 0:
            self.dataindex -= limit_rows*2
            self.show_data()
        elif self.datarows and self.dataindex > 0 and self.dataindex-(limit_rows+1) >= 0:
            self.dataindex = 0
            self.show_data()

    def on_page_next(self):
        limit_rows = self.spinLimit.value()
        if self.datarows and self.dataindex >= 0 and self.dataindex < self.datarows:
            self.show_data()

    def on_re_show(self):
        self.dataindex = 0
        self.show_data()

    def set_count_showing(self):
        # Showing # to ## of ### entries
        limit_rows = self.spinLimit.value()
        count_from = self.dataindex - limit_rows
        if count_from < 0:
            count_from = 0
        count_from += 1
        self.labelShowing.setText("Showing {:,} to {:,} of {:,} entries".format(count_from, self.dataindex, self.datarows))

    def set_status_total_records(self):
        if not hasattr(self, 'dataframe'):
            return
        # Si no esta vacia la variable dataframe:
        if self.dataframe.empty:
            self.set_status("No records")
        else:
            # Numero con ##,###,###,###
            self.set_status("Total records: {:,}".format(self.dataframe.shape[0]))
            self.datarows = self.dataframe.shape[0]
            self.dataindex = 0

    def set_status(self, message):
        self.labelStatus.setText(message)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
