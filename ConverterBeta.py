# -*- coding: utf-8 -*-	
#!/usr/bin/python/lib

  
import wx
import requests
import time 

# Global Variables

currencyvalue=0
userinput=0
converted=0
currencyname=''
currency=[]
rate=[]
analogies={}
time2=[]
debug=[]
			
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
		currency.append(cube.attrib['currency']),rate.append(cube.attrib['rate'])
		for cube in root.findall('.//ex:Cube[@time]', namespaces=namespaces):
        		time2.append(cube.attrib['time'])       
                  

        global analogies        
        analogies = dict(zip(currency,rate))
        
     
class GUI(wx.Frame):
       
       
        def __init__(self, *args, **kw):
            super(GUI, self).__init__(*args, **kw)
            self.InitUI()
           
        def InitUI(self):  
            
     
            pnl = wx.Panel(self)
            wx.OK
            currency2=['EUR']
            
		# εδώ δημιουργούνται τα παράθυρα και ότι έχει να κάνει με την εμφάνιση του προγράμματος		
			
            wx.ComboBox(pnl, pos=(135, 48), choices=currency2,
                style=wx.CB_READONLY,size =(290,25))

            cb2 =wx.ComboBox(pnl, pos=(135,75),choices=currency,
                style=wx.CB_READONLY,size =(290,25))            
     
            wx.StaticText(pnl, label='Convert from/to', pos=(15, 50))
            wx.StaticText(pnl, label='Convert to/from', pos=(15, 80))
            
            global debug
            debug = wx.TextCtrl(pnl,  pos=(135, 250),size =(290,50),style=wx.TE_READONLY,)
            debug.SetValue("             ----------Results--------")




            wx.StaticText(pnl, label='Last Update from ECB: ', pos=(10, 380))
            wx.StaticText(pnl, label=str(time2[0]), pos=(35, 395))
            cb4 = wx.TextCtrl(pnl,pos=(135,160),size =(290,25))
            cb5 = wx.Button(pnl, label="Convert",pos=(213,200))
            wx.StaticText(pnl, label='Amount', pos=(15, 160))
          
            self.SetSize((500, 500))
            self.SetTitle('Currency Converter')
            self.Centre()
            self.style= wx.TAB_TRAVERSAL
            self.Show(True)
            wx.FutureCall(100, self.ShowMessage)
			
# εδώ συνδέουμε τα διάφορα κουτιά(combobox,text,button) εφόσον ενεργοποιηθούν(πχ, να πληκτρολογηθεί κάτι από τον χρήστη, είτε να πατηθεί) με διάφορες συναρτήσεις που επιθυμούμε			
            cb2.Bind(wx.EVT_COMBOBOX, self.OnSelect)
            cb4.Bind(wx.EVT_TEXT, self.OnSelect2)
            cb5.Bind(wx.EVT_BUTTON, self.OnSelect3)
           
 # εδώ βλέπουμε της συναρτήσεις που καλούνται από την σύνδεση γραφικού περιβάλλοντος με των κώδικα		   
		   
        def OnSelect(self, e):
           
             i = e.GetString()
             abc = analogies[i]
             global currencyvalue,currencyname
             currencyname=i
             currencyvalue = float(abc)
           
        def OnSelect2(self,e):
           
             i = e.GetString()
             global userinput
             userinput = float(i)
     
	 # μετατροπή και εμφάνιση συναλλάγματος
        def OnSelect3(self,e):
             global userinput,currencyvalue,converted,currencyname,debug
             converted= userinput * currencyvalue
             converted2= userinput / currencyvalue
             debug.SetValue(str(userinput)+ " EUR = "+str(converted)+" "+currencyname+ " \n"+ str(userinput)+" "+currencyname + '= ' +str(round(converted2,4))+" "+"EUR")            



     #ενημέρωση του χρήστη για την ικανότητα αυτό-ενημερωσης μεσo ίντερνετ.
        def ShowMessage(self):
             wx.MessageBox('Auto-Updated Currency Converter \nFeel free to get our source-code from \nhttp://goo.gl/mL4qxy', 'Welcome',
               wx.OK | wx.ICON_INFORMATION)
       
def main():

        UpdateCurrency()
        ex = wx.App()
        GUI(None)
        ex.MainLoop()  
		
		
 
if __name__ == '__main__':
        main()

