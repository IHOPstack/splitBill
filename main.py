from math import ceil
import cv2
import pytesseract
import re
from kivy.core.window import Window
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget

class Inputs(GridLayout):
    textl = "Name"
    textr = "$0.00"
    lineList = []
    placement = 0
    tax = TextInput(hint_text = "tax", size_hint = (.5, None), height = 50)
    tip = TextInput(hint_text = "tip", size_hint = (.5, None), height = 50)
    def addLine(self, x):
        for i in range(0, (x)):
            TIname = TextInput(hint_text = self.textl, size_hint = (.5, None), height = 50)
            TImoney = TextInput(hint_text = self.textr, size_hint = (.5, None), height = 50)
            self.add_widget(TIname, index = self.placement)
            self.placement -= 1
            self.add_widget(TImoney, index = self.placement)
            self.placement -= 1
            TItuple = (TIname, TImoney)
            self.lineList.append(TItuple)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.addLine(5)
        self.add_widget(self.tax)
        self.add_widget(self.tip)
    def fill4test(self):
        alph = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "z","ab", "bb", "cb", "db", "eb", "bf", "gb", "hb", "ib", "jb", "kb", "lb", "mb", "nb", "ob", "pb", "qb", "rb", "sb", "tb", "ub", "vb", "wb", "xb", "zb"]
        i = 0
        for tuple in self.lineList:
            tuple[0].text = alph[i]
            tuple[1].text = str(i)
            i += 1
        self.tax.text = str(i)
        self.tip.text = str(i)
    def PhotoInput(self):
        image = cv2.imread('receipt2.jpeg')
        text = pytesseract.image_to_string(image)
        moneyList = re.findall("\d+\.\d{2}", text)
        entries = {}
        taxEntry = None
        tipEntry = None
        for price in moneyList:
            for line in text.split("\n"):
                if price in line:
                    ind = line.index(price)
                    item = line[0:ind]
                    if item.strip() == "TOTAL":
                        break
                    if "TAX" in item:
                        taxEntry = price
                        break
                    if "TIP" in item:
                        tipEntry = price
                        break                   
                    entries[item] = price
        self.addLine((len(entries) - 5))
        count = 0
        for key in entries:
            if taxEntry != None:
                self.tax.text = str(taxEntry)
            if tipEntry != None:
                self.tip.text = str(tipEntry)
            tuple = self.lineList[count]
            tuple[0].text = key
            tuple[1].text = entries[key]
            count += 1        
        



        
class FullScreen(BoxLayout):
    people = {}
    def logic(self):
        itemList = [(Inputs.lineList[i].text,Inputs.lineList[i+1].text) for i in range(0, len(Inputs.lineList), 2)]
        taxTip = float(Inputs.tax.text) + float(Inputs.tip.text)
        people = self.people
        subtotal = 0
        for pair in itemList:
            try:
                person = pair[0]
                price = float(pair[-1])
            except ValueError:
                price = float(pair[0])
                person = pair[-1]
            people[person] =  people.get(person, 0) + price
            subtotal += price
        for person in people:
            price = people[person]
            billPercent = price/subtotal
            taxTipShare = billPercent * taxTip
            people[person] = ceil((taxTipShare + price) * 100) / 100
        self.ids.scroller.add_widget(Results())

class Results(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = 1, None
        self.bind(minimum_height = self.setter("height"))
        people = FullScreen.people
        total = 0
        for key in people:
            cost = people[key]
            name = str(key)
            self.add_widget(Label(text = f"{name} owes ${cost}", size_hint = (1, None), height = 50))
            total += cost
        self.add_widget(Label(text = f"Total amound paid is ${total}", size_hint = (1, None), height = 50))




class splitBillApp(App):
    Window.size = (350, 700)

splitBillApp().run()
