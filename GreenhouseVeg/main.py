from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from USBSerial import USBdevice

class GreenhouseWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(GreenhouseWidget, self).__init__(**kwargs)
        self.USBdevice = USBdevice()

    def connect_usb(self):
        self.USBdevice.connect_usb()

    switch_parameters = {
        "drysoil":"s1",
        "wetsoil":"s2",
        "minirriginterval":"s3",
        "startlight":"s4",
        "stoplight":"s5",
        "lowtemp":"s6",
        "hightemp": "s7",
        "minsoilmoist":"s8",
        "irrigtime":"s9"
    }

    def update_parameter(self, parameter):
        try:
            if(parameter in ["minirriginterval", "startlight", "stoplight", "irrigtime"]):
                value = float(self.ids[parameter + "_text_input"].text)
            else:
                value = int(self.ids[parameter + "_text_input"].text)
        except ValueError:
            self.handle_wrong_input()
            return
        self.ids[parameter + "_button"].text += " (ok)"
        #self.send_cmd(f"<{self.switch_parameters[parameter]}{value}>")
        self.send_cmd("<of>")

    def send_cmd(self, cmd):
        self.USBdevice.serial_port.write(cmd.encode())
    
    def rec_msg(self):
        self.USBdevice.serial_port.read()
    
    def handle_wrong_input(self):
        pass
    
    def commit_changes(self):
        self.send_cmd("<on>")

class GreenhouseApp(App):
    def build(self):
        return GreenhouseWidget()

if __name__ == '__main__':
    GreenhouseApp().run()