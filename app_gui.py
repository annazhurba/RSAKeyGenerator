import PySimpleGUI as sg
from generate_functions import generate_key_pair

def process_layout(layout):
    window = sg.Window('Qualified Electronic Signature Emulator', layout, size=(600, 400), resizable=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Quit':
            break
        elif event == 'Generate':
            pin = values['-INPUT-']
            generate_key_pair(pin)


def show_welcome_page():
    layout = [  [sg.VPush()],
                [sg.Text('Welcome to the RSA Signature Generator!')],
                [sg.Text('Enter your PIN to encrypt the private key: '), sg.InputText(key='-INPUT-')],
                [sg.Button('Generate'), sg.Button('Quit')],
                [sg.VPush(), sg.Sizegrip()]
              ]
    process_layout(layout)
