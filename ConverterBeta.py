import wx
import requests
from currencygetter import CurrencyGetter

class GUI(wx.Frame,object):
    
    def __init__(self, *args, **kw):
        super(GUI, self).__init__(*args, **kw)
        self.currencyvalue=currencyvalue=[]
        self.userinput=userinput=''
        self.converted=converted=0
        self.currencyname=currencyname=''
        self.conversionPresenter=wx.TextCtrl()
        self.conversionPresenter2=wx.TextCtrl()
        self.valueToConvert=wx.TextCtrl()
        self.InitUI()
        self.Logic= CurrencyGetter()
        self.Logic.UpdateCurrency()

    def InitUI(self):
        pnl = wx.Panel(self)
        wx.OK
        testa=CurrencyGetter().getCurrencyNameList()
        lastUpdate=CurrencyGetter().time2[0]

        wx.ComboBox(pnl, pos=(135, 48), choices=["EUR"], style=wx.CB_READONLY, size=(290, 25))
        cb2 = wx.ComboBox(pnl, pos=(135, 75), choices=testa, style=wx.CB_READONLY, size=(290, 25))

        wx.StaticText(pnl, label='Convert from/to', pos=(15, 50))
        wx.StaticText(pnl, label='Convert to/from', pos=(15, 80))
        wx.StaticText(pnl, label='Update from ECB: ', pos=(15, 0))
        wx.StaticText(pnl, label=lastUpdate, pos=(130, 0))
        wx.StaticText(pnl, label='Amount', pos=(15, 110))

        self.valueToConvert = wx.TextCtrl(pnl, pos=(135, 110), size=(290, 25))
        self.conversionPresenter = wx.TextCtrl(pnl, pos=(135, 140), size=(290, 25), style=wx.TE_READONLY, )
        self.conversionPresenter2 = wx.TextCtrl(pnl, pos=(135, 170), size=(290, 25), style=wx.TE_READONLY, )

        cb5 = wx.Button(pnl, label="Convert", pos=(135, 200))
        cb6 = wx.Button(pnl, label="Clear", pos=(225, 200))

        self.SetSize((450, 280))
        self.SetMaxSize((450, 300))
        self.SetMinSize((450, 300))

        self.SetTitle('Currency Converter')
        self.Centre()
        self.style = wx.TAB_TRAVERSAL
        self.Show(True)

        # εδώ συνδέουμε τα διάφορα κουτιά(combobox,text,button) εφόσον ενεργοποιηθούν(πχ, να πληκτρολογηθεί κάτι από τον χρήστη, είτε να πατηθεί) με διάφορες συναρτήσεις που επιθυμούμε
        cb2.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self.valueToConvert.Bind(wx.EVT_TEXT, self.OnSelect2)
        cb5.Bind(wx.EVT_BUTTON, self.OnSelect3)
        cb6.Bind(wx.EVT_BUTTON, self.OnSelect4)
        # εδώ βλέπουμε της συναρτήσεις που καλούνται από την σύνδεση γραφικού περιβάλλοντος με των κώδικα

    def OnSelect(self, e):
        i = e.GetString()
        CurrencyValue = self.Logic.analogiesDict()[i]
        self.currencyname = i
        self.currencyvalue = float(CurrencyValue)

    def OnSelect2(self, e):

        self.userinput = float(e.GetString())

    def OnSelect3(self, e):
        converterCUrrencyTuple=self.Logic.convertTheCurrency(self.userinput,self.currencyvalue)
        self.conversionPresenter.SetValue(str(self.userinput) + " EUR = " + str(converterCUrrencyTuple[0]) + " " + self.currencyname + " \n")
        self.conversionPresenter2.SetValue(str( self.userinput) + " " + self.currencyname + ' = ' + str(round(converterCUrrencyTuple[1], 4)) + " " + "EUR")

    def OnSelect4(self, e):
        self.conversionPresenter.Clear()
        self.conversionPresenter2.Clear()
        self.valueToConvert.Clear()

def main():
    
    ex = wx.App()
    GUI(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
