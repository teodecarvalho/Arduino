from kivy.utils import platform
if platform != "android":
    from glob import glob
    import serial
else:
    from usb4a import usb
    from usbserial4a import serial4a

class USBdevice():
    def get_usb_devices(self):
        try:
            self.usb_device = usb.get_usb_device_list()[0]
        except NameError:
            print("Device not found!")

    def connect_usb(self):
        if platform == "android":
            self.get_usb_devices()
            port = self.usb_device.getDeviceName()
            self.serial_port = serial4a.get_serial_port(
                port, 9600, 8, 'N', 1)
        else:
            port = [port for port in glob('/dev/tty.*') if "usbserial" in port][0] # Only works on Mac
            self.serial_port = serial.Serial(port, 9600, timeout=3)