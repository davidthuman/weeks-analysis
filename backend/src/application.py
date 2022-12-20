import sys
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QWidget, QMainWindow, QPushButton, QDialog, QVBoxLayout, QMessageBox, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QLine, pyqtSlot

# Creating a class with the name 'App' that is an extention of the class QWidget


class App(QWidget):

    # create window for application
    def __init__(self):
        super().__init__()
        self.title = 'Classification of Actions'
        self.left = 10
        self.top = 50
        self.width = 640
        self.height = 480
        self.initUI()

    # Will initialize the UI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_button("Level One", 'level_one')
        self.create_button("Level Two", 'level_two')
        self.show()

        # The class needs to be extended from 'QMainWindow', the message appears at the bottom left corner of the screen.
        # self.statusBar().showMessage('Message in statusbar.')

    # Needs to extend QMainWindow
    def create_menubar(self):
        # Creating a menu bar at the top of the window
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        # Adding drop down button to those menus
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

    def create_button(self, text, action):
        # Creates a button object, the first argument is the text displayed on the button
        self.button = QPushButton(text, self)
        # When a user hovers over the button, the '.setToolTip' allows text to be displayed
        self.button.setToolTip('Example Button')
        # Will move the button's location to the x, y position
        
        # Connect the button to the function 'on_click'
        match action:
            case 'level_one':
                self.button.move(200, 150)
                self.button.clicked.connect(self.click_level_one)
            case 'level_two':
                self.button.move(400, 150)
                self.button.clicked.connect(self.click_level_two)

    def create_textbox_button(self):
        # Create a label, which is text on the screen
        label = QLabel("Type anything!", self)
        label.move(50, 50)

        # Create a text box
        self.textbox = QLineEdit(self)
        self.textbox.move(50, 100)
        self.textbox.resize(280, 40)

        # Creates a button object, the first argument is the text displayed on the button
        self.button = QPushButton('Show text', self)
        # When a user hovers over the button, the '.setToolTip' allows text to be displayed
        self.button.setToolTip('Example Button')
        # Will move the button's location to the x, y position
        self.button.move(100, 150)

        # Connect the button to the function 'on_click'
        self.button.clicked.connect(self.on_click)

    # Creating a message box.  Second to last argument is a list of button opinions, the last argument is which button is on foucs
    def pop_up(self):
        buttonReply = QMessageBox.question(
            self, "Title of Message", "Message ... ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked')
        else:
            print('No clicked')


    def createTable(self):
        # Create the table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Sleep"))
        self.tableWidget.move(200, 200)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_table_click)

    # Definition for when the button is clicked
    @pyqtSlot()
    def click_level_one(self):
        value = "Level One"
        QMessageBox.question(self, "Message Title", "You typed: " +
                             value, QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot()
    def click_level_two(self):
        value = "Level Two"

    @pyqtSlot()
    def on_table_click(self):
        print("\n")
        for currentQTableWidgetItme in self.tableWidget.selectedItems():
            print(currentQTableWidgetItme.row(),
                  currentQTableWidgetItme.column(), currentQTableWidgetItme.text())


class Dialog(QDialog):

    def slot_method(self):
        print('slot method called')

    def __init__(self):
        super(Dialog, self).__init__()

        button = QPushButton('Click Me')
        button.clicked.connect(self.slot_method)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(button)

        self.setLayout(mainLayout)
        self.setWindowTitle("Title")


#
def main_app():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


def main_dialog():
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())


main_app()
