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
from kivy.uix.popup import Popup

class Inputs(GridLayout):
    lineList = []
    placement = 0
    tax = TextInput(hint_text = "tax", size_hint = (.5, None), height = 50)
    tip = TextInput(hint_text = "tip", size_hint = (.5, None), height = 50)
    def addLine(self, x):
        for i in range(0, (x)):
            TIname = TextInput(hint_text = "Name", size_hint = (.5, None), height = 50)
            TImoney = TextInput(hint_text = "$0.00", size_hint = (.5, None), height = 50)
            self.add_widget(TIname, index = self.placement)
            self.placement -= 1
            self.add_widget(TImoney, index = self.placement)
            self.placement -= 1
            TItuple = (TIname, TImoney)
            self.lineList.append(TItuple)
    def clearLines(self):
        for pair in self.lineList:
            pair[0].text=""
            pair[1].text=""
            self.tax.text=""
            self.tip.text=""
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
        self.clearLines()
        image = cv2.imread('testReceipts/ginos.jpeg')
        customfig = "--user-patterns configs/tesseract/user-patterns --user-words configs/tesseract/user-words --psm 4"
        text = pytesseract.image_to_string(image, config = customfig)
        print(text)
        entries = []
        taxEntry = None
        tipEntry = None
        haveTip = False
        haveTax = False
        for line in text.split("\n") :
            Match = re.search("\d+\.\d{2}", line)
            if Match != None:
                price = line[Match.start():Match.end()]
                item = line[0:Match.start()].strip()
                if price == "0.00":
                    continue
                match item.capitalize():
                    case "Total" | "Subtotal":
                        print("Total/Subtotal = ", price)
                    case "Tip $" | "Gratuity":
                        tipEntry = price
                        haveTip = True
                        if haveTax:
                            break
                    case "Tax $":
                        taxEntry = price
                        haveTax = True
                        if haveTip:
                            break
                    case _:
                        entries.append((item, price))
                        print("default case")
        if entries == []:
            noneFound = Popup(title = "no items found", content = Label(text = "Please provide better image or enter fields manually"), size_hint = (.5, .5))
            noneFound.open()
            return
        self.addLine((len(entries) - len(self.lineList)))
        count = 0
        for itemFromReceipt in entries:
            if taxEntry != None:
                self.tax.text = str(taxEntry)
            if tipEntry != None:
                self.tip.text = str(tipEntry)
            TIpair = self.lineList[count]
            TIpair[0].text = itemFromReceipt[0]
            TIpair[1].text = itemFromReceipt[1]
            count += 1





        
class FullScreen(BoxLayout):
    people = {}
    def logic(self):
        itemList = [(Inputs.lineList[i][0].text,Inputs.lineList[i][1].text) for i in range(0, len(Inputs.lineList))]
        taxTip = float(Inputs.tax.text) + float(Inputs.tip.text)
        people = self.people
        people.clear()
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
        onScreen = Results()
        try:
            self.ids.scroller.add_widget(onScreen)
        except Exception:
            self.ids.scroller.clear_widgets()
            self.ids.scroller.add_widget(onScreen)

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
    Window.clearcolor = '#fc8c03'

splitBillApp().run()
