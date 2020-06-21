# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from pyowm import OWM, exceptions
from socket import gethostbyname, create_connection
from time import sleep
import sys

sys.path.append('..\\interface\\')
from window import Ui_MainWindow


class WeatherApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(WeatherApp, self).__init__()

        self.owm = OWM('6d00d1d4e704068d70191bad2673e0cc', language='en')

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('WeatherApp')
        self.setWindowIcon(QIcon('..\\assets\\logo.ico'))
        self.setFixedSize(self.width(), self.height())

        self.ui.pushButton.clicked.connect(self.showWeather)
        self.ui.actionExit.triggered.connect(lambda _: sys.exit())

    def showWeather(self):
        try:
            create_connection((gethostbyname('www.google.com'), 80), 2).close()

            self.ui.label.setText('Request processing...')
            self.repaint()

            sleep(.5)

            city = self.ui.lineEdit.text()
            weather = self.owm.weather_at_place(city).get_weather()
            forecast = self.owm.daily_forecast(city, limit=2) \
                .get_forecast().get_weathers()

            self.ui.label.setText('Temperature: {0} °C \
                                  \nWind: {1} m/s \
                                  \nWeather:\n{2} \
                                  \nTomorrow:\n{3} \
                                  \nDay after tomorrow:\n{4}'.format(
                weather.get_temperature('celsius')['temp'],
                weather.get_wind()['speed'],
                weather.get_detailed_status().capitalize(),
                forecast[0].get_detailed_status().capitalize(),
                forecast[1].get_detailed_status().capitalize())
            )
        except OSError:
            self.ui.label.setText('A network error\noccurred!')
        except exceptions.api_response_error.NotFoundError:
            self.ui.label.setText('You entered the\nwrong city name!')
        except exceptions.api_call_error.APICallError:
            self.ui.label.setText('An error occurred\nwhile processing\nthe request!')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = WeatherApp()
    application.show()

    sys.exit(app.exec_())
