
import requests

class CurrencyGetter(object):
    
    def __init__(self,currency=[],rate=[],time2=[],analogies={}):

        self.currency = currency
        self.rate=rate
        self.time2=time2
        self.analogies=analogies


    def UpdateCurrency(self):

        r = requests.get('http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml', stream=True)
        from xml.etree import ElementTree as ET

        tree = ET.parse(r.raw)
        root = tree.getroot()
        namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
        for cube in root.findall('.//ex:Cube[@currency]', namespaces=namespaces):
            self.currency.append(cube.attrib['currency']), self.rate.append(cube.attrib['rate'])
            for cube in root.findall('.//ex:Cube[@time]', namespaces=namespaces):
                self.time2.append(cube.attrib['time'])

        analogies = dict(zip(self.currency, self.rate))
        self.analogies=analogies
        return (self.analogies,self.currency,self.rate,self.time2)   

    def getCurrencyNameList(self):
        return self.currency

    def getRateList(self):
        return self.rate

    def getTimeList(self):
        return self.time2

    def analogiesDict(self):
        return self.analogies

    def convertTheCurrency(self,userinput,currencyvalue):
        converted = userinput * currencyvalue
        converted2 = userinput / currencyvalue
        return (converted,converted2)
        
x = CurrencyGetter()
x.UpdateCurrency()
