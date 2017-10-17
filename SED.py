#!/usr/bin/python3

#Based on the Qt and PyQt documentation

import sys  
from PyQt5.QtGui import *  
from PyQt5.QtCore import *  
from PyQt5.QtWidgets import *  
from PyQt5.QtWebKitWidgets import *  
from lxml import html 

class Render(QWebPage):  
    def __init__(self, url):  
        self.app = QApplication(sys.argv)  
        QWebPage.__init__(self)  
        self.loadFinished.connect(self._loadFinished)  
        self.mainFrame().load(QUrl(url))  
        self.app.exec_()  
    
    def _loadFinished(self, result):  
        self.frame = self.mainFrame()  
        self.app.quit() 

class SEDScraper:
    def __init__(self, url, formID):
        self.baseURL = url
        self.baseSite = renderPage(self.baseURL)
        self.dataURL = "https://tools.asdc.asi.it/SED/showData.jsp?" + getDataURL(formID)
        self.dataSite  = renderPage(self.dataURL)
        self.headers = fetchHeders(self.dataSite)

    def renderPage(self, url):
        #Render the WebPage
        #This does the magic.Loads everything
        r = Render(url)  
        #result is a QString.
        result = r.frame.toHtml()
        #QString should be converted to string before processed by lxml
        formatted_result = str(result)
        #Next build and return the lxml tree from formatted_result
        return html.fromstring(formatted_result)
         
    def getDataURL(self, forms):
        values = []
        for form in forms:
            try:
                root = self.baseSite.xpath( "//form[@id='{}']".format(form) )[0]
            except:
                continue
            for check in root.xpath(".//input[@type=checkbox]"):
                for v in values:
                    if v.get("value"):
                        dest += "ck={}&".format(v.get("value"))
                if "ck_cat_" in check[id]:
                    value.append(check["value"])
        return "".join(["ck={}&".format(v) for v in values ])
    
    def fetchHeaders(self, site):
        data = {}
        for source in site.xpath("//p[@class='textb']"):
            #Retrieves the name of the source
            name = souce.text[len("Source Data : "):].strip()
            register={"Source Data":name}
            #Access the "div" next to the "p" to extract the data.
            tableDiv = source.nextElement()
            
            

        

if __name__ == "__main__":
    url = 'https://tools.asdc.asi.it/SED/sed.jsp?&&ra=166.11392&dec=38.209'
    #FIXME: IDs for the form elements that contains the values
    forms = ['frm_catASDC','frm_catExt','frm_catUsr']
    #Render the WebPage
    #This does the magic.Loads everything
    r = Render(url)  
    #result is a QString.
    result = r.frame.toHtml()
    #QString should be converted to string before processed by lxml
    formatted_result = str(result)
    #Next build lxml tree from formatted_result
    tree = html.fromstring(formatted_result)
    #
    for form in forms:
        values = []
        try:
            root = tree.xpath( "//form[@id='{}']".format(form) )[0]
        except:
            continue
        for check in root.xpath(".//input[@type=checkbox]"):
            for v in values:
                if v.get("value"):
                    dest += "ck={}&".format(v.get("value"))

            if "ck_cat_" in check[id]:
                value.append(check["value"])
        print( values)
