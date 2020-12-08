from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from USBSerial import USBdevice
from kivy.uix.label import Label
import time

class GreenhouseWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(GreenhouseWidget, self).__init__(**kwargs)
        self.USBdevice = USBdevice()

    def connect_usb(self):
        self.USBdevice.connect_usb()
        self.populate_params()

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

    class P(BoxLayout):
        pass

    def show_popup(self, title, msg):
        show = self.P()
        popup_window = Popup(title = title,
                             content = Label(text = msg, font_size = 40),
                             size_hint = (.7, .7))
        popup_window.open()

    def update_parameter(self, parameter):
        try:
            if(parameter in ["minirriginterval", "startlight", "stoplight", "irrigtime"]):
                value = float(self.ids[parameter + "_text_input"].text)
            else:
                value = int(self.ids[parameter + "_text_input"].text)
        except ValueError:
            self.handle_wrong_input()
            return
        cmd = f"{self.switch_parameters[parameter]}{value}"
        while True:
            self.send_cmd(f"<{cmd}>")
            msg = self.rec_msg()
            time.sleep(1)
            print("Trying to update parameter!")
            if cmd in msg:
                break
        self.populate_params()
        self.ids[parameter + "_button"].text += " (ok)"

    def get_readings(self):
        msg = None
        while True:
            self.send_cmd("<sr>")
            msg = self.rec_msg()
            print("Waiting readings!")
            time.sleep(1)
            if msg is not None:
                try:
                    msg_list = msg.splitlines()[-5:]
                    if "Current soil moisture" in msg_list[1]:
                        break
                except:
                    print("Problem in subsetting readings list.")
        return msg_list

    def show_readings(self):
        readings = "\n".join(self.get_readings())
        self.show_popup(title = "Current readings", msg = readings)
        #self.send_cmd("<of>")
        
    def get_params(self):
        msg = None
        while True:
            if msg is not None:
                # Check if the first parameter is in msg
                keys = list(self.switch_parameters.keys())
                if keys[0] in msg and keys[-1] in msg:
                    break
            self.send_cmd("<pp>")
            msg = self.rec_msg()
            print("Waiting msg!")
            time.sleep(1)
        return msg.splitlines()

    def parse_params(self, msg_list):
        params = [line for line in msg_list if ":" in line]
        params = {param.split(":")[0]:param.split(":")[1] for param in params}
        return params

    def populate_params(self):
        msg = self.get_params()
        params_dict = self.parse_params(msg)
        for param in params_dict.keys():
            self.ids[param + "_text_input"].text = params_dict[param]

    def flush(self):
        self.USBdevice.flush()

    def send_cmd(self, cmd):
        self.USBdevice.write(cmd)
    
    def rec_msg(self):
        msg = self.USBdevice.read()
        return msg

    def handle_wrong_input(self):
        pass
    
    def commit_changes(self):
        self.send_cmd("<sa>")
        #self.send_cmd("<on>")

class GreenhouseApp(App):
    def build(self):
        return GreenhouseWidget()

    def on_start(self):
        self.root.connect_usb()

if __name__ == '__main__':
    GreenhouseApp().run()