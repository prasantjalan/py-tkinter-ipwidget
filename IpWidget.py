
from Tkinter import Frame, Entry, Text, Label
from Tkconstants import *
import re
import tkMessageBox
# required for test
from Tkinter import Tk, LabelFrame

class IpByte():
    """ This represents a byte of the IPv4 Address"""

    def __init__(self, master, debug=False):
        """This initializes the widget.
        Debug mdoe can be used to see how Entry validation takes place"""
        self.master = master
        self.debug = debug
        vcmd = (self.master.register(self.__onValidate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry = Entry(self.master, justify=CENTER, validate="all", validatecommand=vcmd, width=4)
        self.default_bg = self.entry.cget('bg')
        if self.debug == True:
            self.text = Text(self.master, height=10, width=40)

    def __onValidate(self, d, i, P, s, S, v, V, W):
        """This validates the user input, as the user types each character"""
        if self.debug == True:
            self.text.delete("1.0", "end")
            self.text.insert("end","__onValidate:\n")
            self.text.insert("end","d='%s'\n" % d)
            self.text.insert("end","i='%s'\n" % i)
            self.text.insert("end","P='%s'\n" % P)
            self.text.insert("end","s='%s'\n" % s)
            self.text.insert("end","S='%s'\n" % S)
            self.text.insert("end","v='%s'\n" % v)
            self.text.insert("end","V='%s'\n" % V)
            self.text.insert("end","W='%s'\n" % W)

        # on key input
        if d == "1":
            if S.isdigit() == False:
                return False
            if len(P) > 3:
                return False
        # on focusout
        if (d == "-1" and s and V == "focusout" ):
            if int(s) >= 256:
                self.entry.configure(bg='red')
                tkMessageBox.showerror("IP Error", "Invalid value of the IP.\nValue should be between 0-225")
                #self.entry.delete(0, END)
                return False
        self.entry.configure(bg=self.default_bg)
        return True

    def configure(self, **kwargs):
        self.entry.configure(**kwargs)
        if self.debug == True:
            self.text.configure(**kwargs)

    def get(self):
        """Read out the value of the ip byte entered by the user. Returns integer value"""
        val = self.entry.get()
        if not val:
            return None
        if (int(val) >= 256):
            return None
        return val

    def set(self, ip):
        """Sets the ip byte to ip"""
        if ip == None:
            self.entry.delete(0, END)
            self.entry.configure(bg=self.default_bg)
            return
        if ip.isdigit() == False:
            self.entry.configure(bg='red')
            return
        if int(ip) >= 999:
            self.entry.configure(bg='red')
            return
        if int(ip) >= 256:
            self.entry.configure(bg='red')
            self.entry.configure(text=ip)
            return
        self.entry.configure(bg=self.default_bg)
        self.entry.delete(0, END)
        self.entry.insert(0, ip)

    def grid(self, *args, **kwargs):
        self.entry.grid(*args, **kwargs)
        if self.debug == True:
            self.text.grid(row=1, column=0)


class IpWidget(Frame):
    """IpWidget can accept IPv4 Address and also verify the input"""

    def __init__(self, master, iptext="Not Defined"):
        """ Initializes IpWidget and also accepts a Label for the widget"""
        Frame.__init__(self, master)
        self.master = master
        self.iptext = iptext
        self.grid(row=0, column=0)

        self.IpWidgetName = Label(self, text=iptext, justify=RIGHT)
        self.IpWidgetName.grid(row=0, column=0, sticky=E)

        self.ipbyte = []
        for i in range(4): # 4 bytes in an IPv4 Address
            self.ipbyte.append(IpByte(self))
            self.ipbyte[i].grid(row=0, column=i+1)

    def ipState(self, st=NORMAL):
        """ The state of the byte widget can be changed if required (st => normal, disabled, etc)"""
        for i in range(4):
            self.ipbyte[i].configure(state=st)

    def getIp(self):
        """ Read out the value entered by the user.
            Returns None if any value is missing or if wrong value is entered.
            Returns dotted dtring (e.g.: 192.168.13.234) if valid Ip Address is entered"""
        val = []
        for i in range(4):
            temp = self.ipbyte[i].get()
            if temp is None:
                return None
            else:
                val.append(temp)
        return val[0] + "." + val[1] + "." + val[2] + "." + val[3]

    def setIp(self, ip):
        """Accepts a dotted string (e.g.: 192.168.1.10)
        This function does not check if the ip byte is greater than 255"""
        if ip == None:
            for i in range(4):
                self.ipbyte[i].set(None)
        matchedObj = re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",ip)
        if matchedObj:
            ib = ip.split('.')
            for i in range(4):
                try:
                    test = ib[i]
                    self.ipbyte[i].set(ib[i])
                except:
                    self.ipbyte[i].set(None)
        else:
            print("IpWidget: did not match ip pattern")

    def configure(self, *args, **kwargs):
        for i in range(4):
            self.ipbyte[i].configure(*args, **kwargs)


if __name__ == "__main__":
    help(IpByte)
    root = Tk()
    root.title("Ip Widget Example")
    ip1 = IpWidget(root, "Ip Address 1 (Valid Address   192.168.100.1):   ")
    ip1.setIp("192.168.100.1")
    ip1.grid(row=0, column=0, pady=10)

    ip2 = IpWidget(root, "Ip Address 2 (Invalid Address 192.278.100.567): ")
    ip2.setIp("192.278.100.567")
    ip2.grid(row=1, column=0, pady=10)

    ipByteFrame = LabelFrame(root, text="IpByte Debug Example : (Only for Entry Widget Demo) ")
    ipByteFrame.grid(row=2, column=0, pady=10)
    ipbyte = IpByte(ipByteFrame, debug=True)
    ipbyte.grid(row=0, column=0, pady=10)

    root.mainloop()
