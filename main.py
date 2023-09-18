from math import ceil
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
    tax = TextInput(hint_text = "tax", size_hint = (.5, None), height = 50)
    tip = TextInput(hint_text = "tip", size_hint = (.5, None), height = 50)
    def addLine(self, x):
        for i in range(0, (2 * x)):
            TI = TextInput(hint_text = self.textl if i%2 == 0 else self.textr, size_hint = (.5, None), height = 50)
            self.add_widget(TI, index = len(self.lineList))
            self.lineList.append(TI)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.addLine(5)
        self.add_widget(self.tax)
        self.add_widget(self.tip)
    def fill4test(self):
        alph = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "z","ab", "bb", "cb", "db", "eb", "bf", "gb", "hb", "ib", "jb", "kb", "lb", "mb", "nb", "ob", "pb", "qb", "rb", "sb", "tb", "ub", "vb", "wb", "xb", "zb"]
        i = 0
        for textBox in self.lineList:
            if textBox.hint_text == "Name":
                textBox.text = alph[i]
            else:
                textBox.text = str(i)
            i += 1
        self.tax.text = str(i)
        self.tip.text = str(i)
        
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
