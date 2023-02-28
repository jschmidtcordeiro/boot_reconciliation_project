import PySimpleGUI as sg 

# View of MVC pattern
class UserView():
    def __init__(self, controller):
        self.__controller = controller
        self.__container = []
        self.__window = sg.Window("Depot Reconciliation List", self.__container ,font=("Helvetica", 14))

    @property
    def window(self):
        return self.__window

    def main_screen(self):
        
        self.__container = [
            [sg.Text('Search for file .txt')],
            [sg.T("")], [sg.Text("Choose a folder: ")],
            [[sg.Input(), sg.FileBrowse()]],
            [sg.Button("Submit")],
            [sg.Text('', key='result')],
        ]
        self.__window = sg.Window("Depot Reconciliation List", self.__container ,font=("Helvetica", 14))

    def show_results(self, result): 
        self.__window.Element('result').Update(result)

    def read_events(self):
        return self.__window.read()

    def end(self):
        self.__window.close()