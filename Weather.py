import sys
import requests
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("WeatherIcon.png"))
        self.text=""
        self.Menu()

    def full_style(self):
        return """
        QMainWindow{
        background-color: hsl(9, 0%, 90%);
        }
        QLineEdit{
        font-size: 35px;
        }
        QLabel#text1{
        font-size:50px;
        font-family: Calibri;
        }
        QLabel#errormsg{
        font-size:40px;
        font-family: Calibri;
        }
        QPushButton{
        font-size: 30px;
        font-family: Calibri;
        background-color: hsl(58, 100%, 67%);
        border: 3px solid;
        padding: 5px 55px;
        }
        QPushButton:hover{
        background-color: hsl(58, 100%, 87%);
        }
        """

    def full_style1(self, id):
        if 200<=id<=521:
            color="233, 33%, 70%"
        elif 701 <= id < 741:
            color= "192, 32%, 91%"
        elif id == 751 or id == 761:
            color = "59, 55%, 69%"
        elif 771<=id<=781:
            color = "176, 66%, 82%"
        elif id == 762:
            color= "9, 66%, 71%"
        elif id==800:
            color="192, 100%, 80%"
        else:
            color= "192, 100%, 65%"

        return f""" 
        QMainWindow{{
        background-color: hsl({color});
        }}
        QLabel#temp{{
        font-size:40px;
        font-family: Calibri;
        }}
        QLabel#emoji{{
        font-size:60px;
        font-family: Segoe UI Emoji;
        }}
        QLabel#description{{
        font-size:35px;
        font-family: Calibri;
        }}
        QPushButton{{
        font-size: 30px;
        font-family: Calibri;
        background-color: hsl(58, 100%, 67%);
        border: 3px solid;
        padding: 5px 55px;
        }}
        QPushButton:hover{{
        background-color: hsl(58, 100%, 87%);
        }}
        """

    def get_emoji(self, id):
        if 200 <= id <= 232:
            return "⛈️"
        elif 300 <= id <= 321:
            return "⛆"
        elif 500 <= id <= 531:
            return "🌧️"
        elif 600 <= id <= 631:
            return "❄️"
        elif 701 <= id < 741:
            return "🌫️"
        elif id == 751 or id == 761:
            return "🏜️"
        elif id == 771:
            return "💨"
        elif id == 781:
            return "🌪️"
        elif id == 762:
            return "🌋"
        elif id == 800:
            return "☀️"
        else:
            return "☁️"

    def Menu(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        text1 = QLabel("Enter City Name: ", self)
        self.textbox = QLineEdit(self)
        button = QPushButton("Get weather", self)
        text1.setObjectName("text1")
        self.textbox.setObjectName("textbox")
        button.setObjectName("button")

        vbox = QVBoxLayout()
        vbox.addWidget(text1)
        vbox.addWidget(QLabel(self))
        vbox.addWidget(self.textbox)
        vbox.addWidget(QLabel(self))
        vbox.addWidget(button, alignment=Qt.AlignCenter)
        vbox.addWidget(QLabel(self))

        button.clicked.connect(self.weather)
        self.textbox.returnPressed.connect(self.weather)

        central_widget.setLayout(vbox)
        self.setStyleSheet(self.full_style())

    def weather(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Weather_info
        api_key = "efcd698c77b6c38ed2a66374d2b66ea3"
        city = self.textbox.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError:
            code = response.status_code
            match code:
                case 400:
                    self.display_error("Bad Request\nCheck Your Input")
                    return
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                    return
                case 402:
                    self.display_error("Forbidden\nAccess Denied")
                    return
                case 404:
                    self.display_error("Not found\nCity not Found")
                    return
                case 500:
                    self.display_error("Server Error\nTry Again Later")
                    return
                case 501:
                    self.display_error("Bad Gateway\nInvalid response from server")
                    return
                case 502:
                    self.display_error("Sevice Unavailable\nServer Down")
                    return
                case 504:
                    self.display_error("Gateway Timeout\nNo response from the server")
                    return
                case _:
                    self.display_error(f"HTTP Error\n {requests.exceptions.HTTPError}")
                    return
        except requests.exceptions.ConnectionError:
            self.display_error("Check your internet connection")
            return
        except requests.exceptions.Timeout:
            self.display_error("Requests Timed out")
            return
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects")
            return
        except requests.exceptions.RequestException as err:
            self.display_error(f"An Error occured: {err}")
            return

        tem = (data['main']['temp'] - 273.15)
        desc = data['weather'][0]['description']
        id = data['weather'][0]['id']
        emo = self.get_emoji(id)

        temp = QLabel(f"{tem:.2f}°C", self)
        emoji = QLabel(emo,self)
        description = QLabel(desc, self)
        getback = QPushButton("Go Back", self)
        temp.setObjectName("temp")
        emoji.setObjectName("emoji")
        description.setObjectName("description")
        getback.setObjectName("getback")

        vbox = QVBoxLayout()
        vbox.addWidget(temp, alignment=Qt.AlignCenter)
        vbox.addWidget(emoji, alignment=Qt.AlignCenter)
        vbox.addWidget(description, alignment=Qt.AlignCenter)
        vbox.addWidget(getback, alignment=Qt.AlignCenter)

        getback.clicked.connect(self.Menu)

        central_widget.setLayout(vbox)
        self.setStyleSheet(self.full_style1(id))

    def display_error(self, message):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        error = QLabel(message, self)
        back = QPushButton("Go Back", self)
        error.setObjectName("errormsg")
        back.clicked.connect(self.Menu)
        vbox = QVBoxLayout()
        vbox.addWidget(error, alignment=Qt.AlignCenter)
        vbox.addWidget(back, alignment=Qt.AlignCenter)

        central_widget.setLayout(vbox)
        self.setStyleSheet(self.full_style())

def main():
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())

main()