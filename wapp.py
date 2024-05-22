import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont

API_KEY = '2400b29b85e27bf53d592e32bb7ce142'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Aplicación de Clima en Tiempo Real')

        # Crear un layout vertical
        layout = QVBoxLayout()

        # Título
        title = QLabel('Aplicación de Clima en Tiempo Real')
        title.setFont(QFont('Helvetica', 16, QFont.Bold))
        layout.addWidget(title)

        # Entrada de ciudad
        self.city_label = QLabel('Ingrese la ciudad:')
        self.city_label.setFont(QFont('Helvetica', 12))
        layout.addWidget(self.city_label)

        self.city_entry = QLineEdit(self)
        self.city_entry.setFont(QFont('Helvetica', 12))
        layout.addWidget(self.city_entry)

        # Botón para obtener el clima
        self.button = QPushButton('Obtener Clima', self)
        self.button.setFont(QFont('Helvetica', 12))
        self.button.clicked.connect(self.get_weather)
        layout.addWidget(self.button)

        # Resultado
        self.result_label = QLabel('', self)
        self.result_label.setFont(QFont('Helvetica', 14, QFont.Bold))
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def get_weather(self):
        city = self.city_entry.text()
        try:
            url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if data['cod'] != 200:
                raise Exception(data['message'])

            weather = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description']
            }

            self.display_weather(weather)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al obtener datos: {e}')

    def display_weather(self, weather):
        self.result_label.setText(f"Ciudad: {weather['city']}\n"
                                  f"Temperatura: {weather['temperature']}°C\n"
                                  f"Humedad: {weather['humidity']}%\n"
                                  f"Descripción: {weather['description']}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherApp()
    ex.show()
    sys.exit(app.exec_())
