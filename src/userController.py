from src.userView import UserView
import PySimpleGUI as sg 
from src.PDFFilter import PDFFilter

class UserController:
    def __init__(self):
        self.__userScreen = UserView(self)
        self.__Users = {} # List of user objects

    def start(self):
        self.__userScreen.main_screen()
        
        # Event loop
        running = True
        while running:
            event, values = self.__userScreen.read_events()

            if event == sg.WIN_CLOSED:
                running = False
            if event == 'Submit':
                result = values["Browse"]
                pdf = PDFFilter(result)
                pdf.main()


            self.__userScreen.window.Element('result').update(result)

        self.__userScreen.end()
    
    def result(self, message):
        self.__userScreen.show_results(message)