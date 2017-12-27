import wx
import requests

# Global Variables

currencyvalue = 0
userinput = 0
converted = 0
currencyname = ''
currency = []
rate = []
analogies = {}
time2 = []
debug = []


def UpdateCurrency():
    # ...
    # Χρησιμοποιώντας την βιβλιοθήκη requests κατεβάζουμε από την επίσημη ιστοσελίδα της,
    # Ευρωπαϊκής κεντρικής τράπεζας ένα xml αρχείο το οποίο περιέχει τις ποιο πρόσφατες τιμές,
    # συναλλαγματoς σε σχέση με το Ευro.
    r = requests.get('http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml', stream=True)
    from xml.etree import ElementTree as ET

    # Διαβάζουμε το xml αρχείο και καταλήγουμε στα nodes που μας ενδιαφέρουν (Currency,Value) και τα βάζουμε σε μια λίστα ξεχωριστά
    tree = ET.parse(r.raw)
    root = tree.getroot()
    namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    for cube in root.findall('.//ex:Cube[@currency]', namespaces=namespaces):
        currency.append(cube.attrib['currency']), rate.append(cube.attrib['rate'])
        for cube in root.findall('.//ex:Cube[@time]', namespaces=namespaces):
            time2.append(cube.attrib['time'])

    analogies = dict(zip(currency, rate))
    
    return analogies   


class GUI(wx.Frame):
    def __init__(self, *args, **kw):
        super(GUI, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        pnl = wx.Panel(self)
        wx.OK
        currency2 = ['EUR']

        # εδώ δημιουργούνται τα παράθυρα και ότι έχει να κάνει με την εμφάνιση του προγράμματος

        wx.ComboBox(pnl, pos=(135, 48), choices=currency2, style=wx.CB_READONLY, size=(290, 25))
        cb2 = wx.ComboBox(pnl, pos=(135, 75), choices=currency, style=wx.CB_READONLY, size=(290, 25))

        wx.StaticText(pnl, label='Convert from/to', pos=(15, 50))
        wx.StaticText(pnl, label='Convert to/from', pos=(15, 80))

        global debug
        global debug2
        debug = wx.TextCtrl(pnl, pos=(135, 140), size=(290, 25), style=wx.TE_READONLY, )
        debug2 = wx.TextCtrl(pnl, pos=(135, 170), size=(290, 25), style=wx.TE_READONLY, )
        
        

        wx.StaticText(pnl, label='Update from ECB: ', pos=(15, 0))
        wx.StaticText(pnl, label=str(time2[0]), pos=(130, 0))
        cb4 = wx.TextCtrl(pnl, pos=(135, 110), size=(290, 25))
        cb5 = wx.Button(pnl, label="Convert", pos=(135, 200))
        cb6 = wx.Button(pnl, label="Clear", pos=(225, 200))

        wx.StaticText(pnl, label='Amount', pos=(15, 110))

        self.SetSize((450, 280))
        self.SetMaxSize((450, 300))
        self.SetMinSize((450, 300))

        self.SetTitle('Currency Converter')
        self.Centre()
        self.style = wx.TAB_TRAVERSAL
        self.Show(True)
        # wx.FutureCall(100, self.ShowMessage)

        # εδώ συνδέουμε τα διάφορα κουτιά(combobox,text,button) εφόσον ενεργοποιηθούν(πχ, να πληκτρολογηθεί κάτι από τον χρήστη, είτε να πατηθεί) με διάφορες συναρτήσεις που επιθυμούμε
        cb2.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        cb4.Bind(wx.EVT_TEXT, self.OnSelect2)
        cb5.Bind(wx.EVT_BUTTON, self.OnSelect3)
        cb6.Bind(wx.EVT_BUTTON, self.OnSelect4)


        # εδώ βλέπουμε της συναρτήσεις που καλούνται από την σύνδεση γραφικού περιβάλλοντος με των κώδικα

    def OnSelect(self, e):
        i = e.GetString()
        CurrencyValue = analogies[i]
        global currencyvalue, currencyname
        currencyname = i
        currencyvalue = float(CurrencyValue)

    def OnSelect2(self, e):
        i = e.GetString()
        global userinput
        userinput = float(i)

        # μετατροπή και εμφάνιση συναλλάγματος

    def OnSelect3(self, e):
        global userinput, currencyvalue, converted, currencyname, debug
        converted = userinput * currencyvalue
        converted2 = userinput / currencyvalue
        debug.SetValue(str(userinput) + " EUR = " + str(converted) + " " + currencyname + " \n")
        debug2.SetValue(str( userinput) + " " + currencyname + ' = ' + str(round(converted2, 4)) + " " + "EUR")

    def OnSelect4(self, e):
        debug.Clear()
        debug2.Clear()
        cb4.Clear()

def main():
    
    ex = wx.App()
    GUI(None)
    ex.MainLoop()


if __name__ == '__main__':
    analogies = UpdateCurrency()
    main()
