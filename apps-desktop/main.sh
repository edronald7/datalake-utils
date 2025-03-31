# validar si está instalado python y las librerias (pyqt5, pandas, pyarrow, pyyaml, openpyxl)
if ! command -v python3 &> /dev/null
then
    echo "Python no está instalado. Instalando Python..."
    # preguntar si desea instalar python
    read -p "¿Desea instalar Python? (s/n): " install_python
    if [ "$install_python" = "s" ]; then
        # instalar python
        sudo apt-get update
        sudo apt-get install python3 python3-pip -y
        # instalar librerias
        pip3 install pyqt5 pandas pyarrow pyyaml openpyxl
        echo "Python y las librerías necesarias se han instalado."
    else
        echo "Python no se instalará. Saliendo..."
        exit 1
    fi

fi

# comprobar nuevamente si está instalado python
if ! command -v python3 &> /dev/null
then
    echo "Python no se pudo instalar. Saliendo..."
    exit 1
fi

# verficar si archivo main.py existe
if [ ! -f "main.py" ]; then
    echo "El archivo main.py no existe. Saliendo..."
    exit 1
fi

# Ejecutar el script de Python
python3 main.py
if [ $? -ne 0 ]; then
    echo "Error al ejecutar el script de Python. Saliendo..."
    exit 1
fi