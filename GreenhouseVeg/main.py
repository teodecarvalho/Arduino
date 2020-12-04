from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class GreenhouseWidget(BoxLayout):
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
        self.send_cmd(f"<{self.switch_parameters[parameter]}{value}>")

    def send_cmd(self, cmd):
        print(cmd)

    def handle_wrong_input(self):
        pass

class GreenhouseApp(App):
    def build(self):
        return GreenhouseWidget()

if __name__ == '__main__':
    GreenhouseApp().run()