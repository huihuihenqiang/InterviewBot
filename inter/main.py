from PyQt5.QtWidgets import QApplication
from chatbot.ui import ChatBotApp

def main():
    app = QApplication([])
    window = ChatBotApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()










