import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QListWidget
)

class GameClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD: Игры")
        self.setGeometry(100, 100, 350, 400)

        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.name_label = QLabel("Название игры:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.price_label = QLabel("Цена:")
        self.price_input = QLineEdit()
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)

        self.quantity_label = QLabel("Количество:")
        self.quantity_input = QLineEdit()
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_game)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить")
        self.update_button.clicked.connect(self.update_game)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_game)
        layout.addWidget(self.delete_button)

        self.refresh_button = QPushButton("Обновить список")
        self.refresh_button.clicked.connect(self.load_games)
        layout.addWidget(self.refresh_button)

        self.list_widget.itemClicked.connect(self.load_selected_game)

        self.load_games()

    def load_selected_game(self, item):
        name, price, quantity = item.text().split(" | ")
        self.name_input.setText(name)
        self.price_input.setText(price)
        self.quantity_input.setText(quantity)

    def load_games(self):
        try:
            response = requests.get("http://localhost:5000/get_games")
            self.list_widget.clear()
            for game in response.json():
                self.list_widget.addItem(f"{game['name']} | {game['price']} | {game['quantity']}")
        except:
            QMessageBox.critical(self, "Ошибка", "Ошибка загрузки списка игр")

    def add_game(self):
        self._send_game("http://localhost:5000/add_game", method="post", success_msg="Игра добавлена")

    def update_game(self):
        self._send_game("http://localhost:5000/update_game", method="put", success_msg="Игра обновлена")

    def _send_game(self, url, method, success_msg):
        name = self.name_input.text()
        price = self.price_input.text()
        quantity = self.quantity_input.text()

        if not name or not price or not quantity:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            data = {"name": name, "price": float(price), "quantity": int(quantity)}
            if method == "post":
                r = requests.post(url, json=data)
            else:
                r = requests.put(url, json=data)
            msg = r.json().get("message") or r.json().get("error")
            if r.status_code == 200:
                QMessageBox.information(self, "Успех", success_msg)
                self.load_games()
            else:
                QMessageBox.warning(self, "Ошибка", msg)
        except:
            QMessageBox.critical(self, "Ошибка", "Не удалось отправить данные!")

    def delete_game(self):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название игры!")
            return

        try:
            r = requests.delete("http://localhost:5000/delete_game", params={"name": name})
            msg = r.json().get("message") or r.json().get("error")
            if r.status_code == 200:
                QMessageBox.information(self, "Успех", msg)
                self.load_games()
            else:
                QMessageBox.warning(self, "Ошибка", msg)
        except:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к серверу!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameClient()
    window.show()
    sys.exit(app.exec())