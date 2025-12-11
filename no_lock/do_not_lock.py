import sys
import ctypes


class os_no_lock:
    
    def __init__(self):
        self.platform = sys.platform
        
    
    def run_mac(self):
        
        IOPMAssertionCreateWithName = ctypes.cdll.LoadLibrary(
            '/System/Library/Frameworks/IOKit.framework/IOKit'
        ).IOPMAssertionCreateWithName
        
        
    def run_linux(self):
        import dbus #pip install dbus-python
        
        bus = dbus.SessionBus()
        proxy = bus.get_object("org.freedesktop.ScreenSaver", "/ScreenSaver")
        iface = dbus.Interface(proxy, "org.freedesktop.ScreenSaver")
        cookie = iface.Inhibit("MyApp", "Prevent screensaver while running")

        # Later, when done:
        iface.UnInhibit(cookie)

    
    def run(self):
        if self.platform == 'darwin': #macos
            self.run_mac()
            
        elif sys.platform == 'linux':
            self.run_linux()
            
        else:
            print("Not compatible with windows")

