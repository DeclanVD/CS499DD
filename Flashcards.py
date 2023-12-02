import tkinter as tk
from tkinter import font
from tkinter.messagebox import askyesno, showerror, showinfo
import json
import random
import math
import os

# Classes For Cards and Decks #########################################
class Deck():
    def __init__(self, title, cards=None):
        self.title = title
        self.cards = []

        if cards == None or cards == []:
            pass
        elif type(cards) == list:
            remove = []
            for card in cards:
                if type(card) != Card:
                    # print(card)
                    remove.append(card)
            for item in remove:
                cards.remove(item)
            self.cards.extend(cards)
        elif type(cards) == Card:
            self.cards.append(cards)

    def __str__(self):
        return self.title

    def __len__(self):
        return len(self.cards)
    
    def printCards(self):
        for card in self.cards:
            print(card)

    def createAdd(self, front, back):
        card = Card(front, back)
        self.cards.append(card)

    def add(self,card):
        if type(card) == Card:
            self.cards.append(card)
        else:
            print(f"Item {card} is not of class 'Card'")
    
    def convJson(self):
        obj = {}
        obj["name"] = self.title
        obj["cards"] = []
        for card in self.cards:
            obj["cards"].append(card.convJson())
        return obj
    
    def createCards(cardList):
        if type(cardList) != list:
            raise TypeError("Deck.createCards requires Cards to be in a list")
        cards = []
        for card in cardList:
            try:
                newCard = Card(card['front'],card['back'])
                cards.append(newCard)
            except (KeyError, TypeError):
                continue
        return cards
        
    def deleteCard(self, card):
        try:
            index = self.cards.index(card)
        except ValueError:
            raise ValueError(f"{card} does not exist in deck")
        
        self.cards.pop(index)
       

class Card():
    def __init__(self, front, back):
        self.front = front
        self.back = back
    
    def __str__(self):
        return f"{self.front} | {self.back}"
    
    def convJson(self):
        obj = {}
        obj["front"] = self.front
        obj["back"] = self.back
        return obj

# Global Functions #######################################
def saveDecks():
    global decks
    content = {}
    for deck in decks:
        content[deck.title]= deck.convJson()
        
    string = json.dumps(content, indent=4)
    with open("./decks.json","w") as f:
        f.write(string)
    showinfo("Flashcards","All changes have been saved")

def saveOnClose():
    answer = askyesno("Save Changes?", "Do you want to save before closing?")
    if answer is True:
        saveDecks()
    window.destroy()
    
# Read/Create file for storing card and deck information #####################

file = os.path.isfile("./decks.json")
if file is False:
    with open("./decks.json", "w") as f:
        f.write('{"Deck1": {"name":"Deck1", "cards":[]}}')


with open("./decks.json","r") as f:
    data = json.load(f)

decks = []
for deck in data:
    cards = Deck.createCards(data[deck]["cards"])
    decks.append(Deck(data[deck]["name"], cards))

# tkinter Class setup =====================================================
# App (main application)==============================================
class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="gray14")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=7)
        self.rowconfigure(0, weight=1)

        self.xpad = 30
        self.ypad = 15

        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Calibri")

        frm_buttons = tk.Frame(self, height=100, width=100,bg='gray')
        frm_buttons.rowconfigure((0,1,2,3), weight=1)
        frm_buttons.rowconfigure(4, weight=4)
        frm_buttons.columnconfigure(0, weight=1)

        btn_home = tk.Button(frm_buttons, text="Home", font=("Calibri",14), height=1, cursor="hand2", command=self.switchHome)
        btn_home.grid(row=0,column=0, padx=10, pady= 10, sticky="nsew")

        btn_addFrame = tk.Button(frm_buttons,text="Add",font=("Calibri",14), height=1, width=1, cursor="hand2", command=self.switchAdd_Frame)
        btn_addFrame.grid(row=1,column=0, padx=10, pady= 10, sticky="nsew")
        
        btn_browse = tk.Button(frm_buttons, text="Browse",font=("Calibri",14), height=1, cursor="hand2", command=self.switchBrowse)
        btn_browse.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        btn_save = tk.Button(frm_buttons, text="Save",font=("Calibri",14), height=1, cursor="hand2", command=saveDecks)
        btn_save.grid(row=3,column=0,padx=10, pady=10, sticky="nsew")
        frm_buttons.grid(row=0, column=0, sticky="nsew")

        self.home = Home(self)
        self.home.grid(row=0, column=1, padx=self.xpad, pady=self.ypad, sticky="nsew")
        self.add_frame = Add_Frame(self)
        self.add_frame.grid(row=0, column=1, padx=self.xpad, pady=self.ypad, sticky="nsew")
        self.add_frame.grid_forget()
        self.browse = Browse(self)
        self.browse.grid(row=0, column=1, padx=self.xpad, pady=self.ypad, sticky="nsew")
        self.browse.grid_forget()

        self.activePage = self.home
        self.frames = [self.home, self.add_frame, self.browse]


    def switchPage(self, page):
        self.activePage.forget()
        self.activePage = self.frames[page]
        self.activePage.tkraise()
        self.activePage.grid(row=0, column=1, padx=self.xpad, pady=self.ypad, sticky="nsew")

    def switchHome(self):
        self.switchPage(0)
    def switchAdd_Frame(self):
        self.switchPage(1)
    def switchBrowse(self):
        self.switchPage(2)


# Home and Related =====================================================
# CardFrame ================================================
class CardFrame(tk.Frame):
    def __init__(self, parent, card):
        tk.Frame.__init__(self, parent, height=30, width=80, bg="gray24")
        self.columnconfigure((0,1,2), weight=1)
        self.columnconfigure(1,weight=5)
        self.rowconfigure((0,1,2), weight=1)
        self.rowconfigure(1, weight=3)
        # front = 0; back = 1
        self.state = 0
        self.front= card.front
        self.back= card.back

        self.lbl_Front = tk.Label(self, text=self.front, font=("Calibri",(20)), wraplength=280, bg="white", cursor="hand2", width=1)
        self.lbl_Front.bind("<Button-1>", self.flip)
        self.lbl_Front.grid(row=1,column=1,sticky="nsew")

        self.lbl_Back = tk.Label(self, text=self.back, font=("Calibri", (20)), wraplength=280, bg="white", cursor="hand2", width=1, height=1)
        self.lbl_Back.bind("<Button-1>", self.flip)
        self.lbl_Back.grid(row=1,column=1,sticky="nsew")
        self.lbl_Back.grid_forget()

        self.cardSides = [self.lbl_Front, self.lbl_Back]
    
    def flip(self, event):
        self.cardSides[self.state].grid_forget()
        self.state = (self.state + 1)%2
        self.cardSides[self.state].tkraise()
        self.cardSides[self.state].grid(row=1,column=1,sticky="nsew")

# DeckFrame ================================================
class DeckFrame(tk.Frame):
    def __init__(self, parent, deck):
        tk.Frame.__init__(self, parent, height=50, width=100, bg="gray24")
        self.columnconfigure(0,weight=1)
        self.rowconfigure((0,1), weight=1)
        self.rowconfigure(0, weight=9)

        self.deck = deck
        self.title = deck.title
        self.cards = list(deck.cards)
        random.shuffle(self.cards)

        self.pos = 0
        try:
            self.frm_Card = CardFrame(self, self.cards[self.pos])
        except:
            self.frm_Card = CardFrame(self,Card("",""))
        self.frm_Card.grid(row=0, column=0, sticky="nsew")
           
        self.frm_control = tk.Frame(self, height=45, width=200, bg='gray24')
        self.frm_control.columnconfigure((0,2), weight=1)
        self.frm_control.columnconfigure(1,weight=5)
        self.frm_control.rowconfigure(0, weight=1)

        self.btn_left = tk.Button(self.frm_control, text="\u2190", cursor="hand2", command=self.moveLeft)
        self.btn_left.grid(row=0, column=0, sticky="nsew")
        self.btn_right = tk.Button(self.frm_control, text="\u2192", cursor="hand2", command=self.moveRight)
        self.btn_right.grid(row=0, column=2, sticky="nsew")
        self.btn_flip = tk.Button(self.frm_control, text="Flip", cursor="hand2")
        self.btn_flip.grid(row=0, column=1, sticky="nsew")
        self.btn_flip.bind("<Button-1>",self.frm_Card.flip)

        self.frm_control.grid(row=1,column=0, sticky="nsew")

    def changeCard(self, move):
        if len(self.cards) == 0:
            app.home.back()
            return
        self.frm_Card.grid_forget()
        self.frm_Card.destroy()
        self.pos = (self.pos + move)%len(self.cards)
        self.frm_Card = CardFrame(self, self.cards[self.pos])
        self.frm_Card.tkraise()
        self.btn_flip.unbind("<Button-1>")
        self.btn_flip.bind("<Button-1>", self.frm_Card.flip)
        self.frm_Card.grid(row=0,column=0, sticky="nsew")

    def moveLeft(self):
        self.changeCard(-1)
    def moveRight(self):
        self.changeCard(1)

    def updateCards(self):
        self.cards = list(self.deck.cards)
        random.shuffle(self.cards)
        if len(self.cards)>0:
            self.moveLeft()
            self.moveRight()

# Home ===================================================================
class Home(tk.Frame):
    def __init__(self, parent):
    # Configuring ===================================
        tk.Frame.__init__(self, parent, height=300, width=600, bg='gray24')
        global decks
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0,2), weight=1)
        self.columnconfigure(1,weight=5)

        self.grid_propagate(False)
        self.deckMenu = tk.Frame(self, height=50, width=100, bg="navy")
        self.deckMenu.columnconfigure(0,weight=1)
        

    # Frames Set Up===========================================

        self.frames_ref = {}

        for f in range(len(decks)):
            frm_deck = DeckFrame(self, decks[f])
            frm_deck.grid(row=0, column=1, sticky="nsew")
            frm_deck.grid_forget()

            self.frames_ref[decks[f].title] = frm_deck

        self.btn_back = tk.Button(self, text="Back", font=("Calibri", (12)), cursor="hand2", command=self.back)
        self.btn_back.grid(row=0, column=0, padx=10, pady=10,sticky="nw")
        self.btn_back.grid_forget()

    # Radio Selection Buttons=====================

        self.selection = tk.StringVar()
        self.radios = []

        for d in range(len(decks)):
            radio = tk.Radiobutton(self.deckMenu, text=f'{decks[d].title}', variable= self.selection, value=decks[d].title, indicatoron=0, cursor="hand2", command=self.select)
            self.radios.append(radio)
            radio.grid(row=d,column=0,padx=10,pady=10,sticky="nsew")

        self.deckMenu.grid(row=0, column=1, sticky="nsew")


    # Functions ======================================
    def select(self):
        sel = self.selection.get()
        if len(self.frames_ref[sel].deck) == 0:
            showerror("No Cards", "This deck does not have any cards.\nAdd cards in order to view.")
            return
        self.deckMenu.forget()
        self.btn_back.tkraise()
        self.btn_back.grid(row=0, column=0, padx=10, pady=10,sticky="nw")

        self.frames_ref[sel].tkraise()
        self.frames_ref[sel].grid(row=0, column=1, sticky="nsew")
    
    def back(self):
        sel = self.selection.get()
        self.frames_ref[sel].grid_forget()
        self.btn_back.grid_forget()
        self.deckMenu.tkraise()
        self.deckMenu.grid(row=0, column=1, sticky="nsew")

    def addDeck(self, deck):
        frm_deck = DeckFrame(self, deck)
        frm_deck.grid(row=0, column=1, sticky="nsew")
        frm_deck.grid_forget()
        self.frames_ref[frm_deck.title]=frm_deck

        d = len(self.radios)
        radio = tk.Radiobutton(self.deckMenu, text=f'{decks[d].title}', variable= self.selection, value=f'{decks[d].title}',indicatoron=0,cursor="hand2", command=self.select)
        self.radios.append(radio)
        radio.grid(row=d,column=0,padx=10,pady=10,sticky="nsew")
    
    def delDeck(self, deck):
        popped = self.frames_ref.pop(deck.title)

        try:
            index = decks.index(deck)
        except ValueError:
            raise ValueError(f"{deck.title} does not exist")
        self.radios[index].destroy()
        self.radios.pop(index)
        
    def updateTitle(self):
        radios = self.radios
        index = list(self.frames_ref.keys()).index(self.selection.get())
        newFrameRef = {}
        for i in range(len(radios)):
            widget = radios[i]
            widget.config(text=f'{decks[i].title}',value=f'{decks[i].title}')
            oldRef = list(self.frames_ref.keys())[i]
            newFrameRef[decks[i].title] = self.frames_ref[oldRef]
        self.frames_ref = newFrameRef
        self.selection.set(list(self.frames_ref.keys())[index])


# Add Cards ==================================================
# Add Frame ==================================================
class Add_Frame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=300, width=600, bg='gray24')
        self.columnconfigure((0,1,2),weight=1)
        self.columnconfigure((1), weight=3)
        self.rowconfigure((0,1), weight=1)

        self.form_card = Form(self)
        self.form_card.grid(row=0, column=1, padx=30,pady=30, sticky="nsew")
        self.form_deck = DeckForm(self)
        self.form_deck.grid(row=1,column=1, padx=30, pady=30,sticky="nsew")

# Form ===================================================================
class Form(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=300, width=600, bg="gray")
        global decks
        self.columnconfigure((0,1), weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure((0,1,2,3,4), weight=1)

        self.decks_ref = {}
        for deck in decks:
            self.decks_ref[deck.title] = deck
        self.deckDest = tk.StringVar()
        self.deckDest.set(list(self.decks_ref.keys())[0])

        self.lbl_form = tk.Label(self, text="Add New Card", font="15")
        self.lbl_form.grid(row=0,column=0,columnspan=2,sticky="nsew")
        self.btn = tk.Button(self, text="Add Card", cursor="hand2", command=self.submit)
        self.lbl_drop = tk.Label(self, text="Deck:")
        self.lbl_drop.grid(row=1,column=0, sticky="nsew")
        self.drop = tk.OptionMenu(self, self.deckDest, *self.decks_ref)
        self.drop.grid(row=1,column=1,sticky="nsew")

        self.lbl_front = tk.Label(self, text="Front:")
        self.ent_front = tk.Entry(self, font=("Calibri", (14)))
        self.lbl_front.grid(row=2,column=0,sticky="nsew")
        self.ent_front.grid(row=2,column=1,sticky="nsew")
        self.lbl_back = tk.Label(self, text="Back:")
        self.ent_back = tk.Entry(self, font=("Calibri", (14)))
        self.ent_back.bind("<Return>", self.submit)
        self.lbl_back.grid(row=3,column=0,sticky="nsew")
        self.ent_back.grid(row=3,column=1,sticky="nsew")
        self.btn.grid(row=4,column=0, columnspan=2, sticky="nsew")
    
    def show(self):
        title = self.deckDest.get()
        print(self.decks_ref[title].cards[0])
        print(self.ent_front.get(), self.ent_back.get())

    def submit(self, event=None):
        title = self.deckDest.get()
        dest = self.decks_ref[title]
        new_front = self.ent_front.get()
        new_back = self.ent_back.get()

        dest.createAdd(new_front,new_back)
       
        deck_frm = app.home.frames_ref[title]

        deck_frm.updateCards()
        browse = app.browse
        if dest == browse.currentDeck:
            browse.setup()

        self.ent_front.delete(0,tk.END)
        self.ent_back.delete(0,tk.END)
        self.ent_front.focus_set()
    
    def updateOptions(self):
        current = self.deckDest.get()

        self.decks_ref = {}
        for deck in decks:
            self.decks_ref[deck.title] = deck

        menu = self.drop["menu"]
        menu.delete(0,'end')
        for deckTitle in self.decks_ref:
            menu.add_command(label=deckTitle, command=tk._setit(self.deckDest, deckTitle))
        if current in self.decks_ref:
            self.deckDest.set(current)
        else:
            self.deckDest.set(list(self.decks_ref.keys())[0])

# DeckForm ====================================================
class DeckForm(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=300, width=600, bg="gray")
        global decks
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure((0,1,2), weight=1)
        self.rowconfigure(1,weight=3)


        self.lbl = tk.Label(self,text="Add New Deck", font=15)
        self.lbl.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.lbl_name = tk.Label(self, text="Name:")
        self.ent_name = tk.Entry(self, font=("Calibri", (14)))
        self.ent_name.bind("<Return>", self.submit)
        self.lbl_name.grid(row=1,column=0,sticky='nsew')
        self.ent_name.grid(row=1,column=1,sticky="nsew")

        self.btn_submit = tk.Button(self, text="Add", cursor="hand2", command=self.submit)
        self.btn_submit.grid(row=2,column=0, columnspan=2, sticky="nsew")

    def submit(self, event=None):
        global app 
        new_title = self.ent_name.get()
        card_form = app.add_frame.form_card
        if new_title in card_form.decks_ref:
            showerror(title="Error", message=f'{new_title} already exists')
            return
        new_deck = Deck(new_title)
        decks.append(new_deck)
        app.home.addDeck(new_deck)

        card_form.decks_ref[new_deck.title] = new_deck
        card_form.updateOptions()
        app.browse.updateOptions()

        self.ent_name.delete(0,tk.END)


# Browse ==================================================
class Browse(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=300, width=600, bg='gray')
        global decks
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0, weight=1)

        self.frm_edit = None
        self.frm_browse = tk.Frame(self,  height=300, width=600, bg='gray')
       
        self.frm_browse.columnconfigure(0, weight=1)
        self.frm_browse.rowconfigure(0, weight=1)
        self.frm_browse.rowconfigure(1, weight=9)
        self.frm_browse.rowconfigure(2, weight=1)

        self.decks_ref = {}
        for deck in decks:
            self.decks_ref[deck.title] = deck
        self.deckDest = tk.StringVar()
        self.deckDest.set(list(self.decks_ref.keys())[0])
        self.currentDeck = self.decks_ref[self.deckDest.get()]

        self.frm_options = tk.Frame(self.frm_browse)
        self.frm_options.rowconfigure(0, weight=1)
        self.frm_options.columnconfigure((0,1,2,3), weight=2)
        self.frm_options.columnconfigure(0, weight=20)
        self.drop = tk.OptionMenu(self.frm_options, self.deckDest, *self.decks_ref)
        self.drop.config(width=1, font=("Calibri", (12)))
        self.drop.grid(row=0,column=0,sticky="nsew")

        self.lbl_length = tk.Label(self.frm_options, text=f"{len(self.currentDeck)} cards", width=1, border=2, relief=tk.RAISED)
        self.lbl_length.grid(row=0, column=1, sticky="nsew")

        self.btn_edit_deck = tk.Button(self.frm_options, text="Edit", cursor="hand2", width=1, command=self.editDeck)
        self.btn_edit_deck.grid(row=0, column=2, sticky="nsew")

        self.btn_del_deck = tk.Button(self.frm_options, text="\u274c", cursor="hand2", width=1, command=self.delDeck)
        self.btn_del_deck.grid(row=0, column=3, sticky="nsew")

        self.frm_options.grid(row=0, column=0, sticky="nsew")


        self.pagesList = []
        self.pagePos = 0
        self.pageMax = 10

        self.frm_control = tk.Frame(self.frm_browse, width=1, bg="gray24")
        self.btn_left = tk.Button(self.frm_control, text='\u2190', cursor="hand2", height=2, width=4, command=self.switchPageLeft)
   
        self.btn_left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.btn_right = tk.Button(self.frm_control, text="\u2192", cursor="hand2", height=2, width=4, command=self.switchPageRight)
        self.btn_right.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.frm_control.grid(row=2, column=0, sticky="nsew")

        self.view = tk.Frame(self.frm_browse, bg='darkgray')
        self.view.rowconfigure(0, weight=1)
        self.view.columnconfigure(0, weight=1)
        # self.view.grid_propagate(False)
        self.setup()
        self.deckDest.trace_add('write', self.setupCallback)
        self.view.grid(row=1, column=0, sticky="nsew")

        self.frm_browse.grid(row=0, column=0, sticky="nsew")
# Functions =====================================================
    def setup(self):
        for label in self.view.winfo_children():
            label.destroy()

        pageMax = self.pageMax
        self.pagePos = 0
        deck = self.decks_ref[self.deckDest.get()]
        self.currentDeck = deck
        countC = len(deck.cards)
        countP = math.ceil(countC/pageMax)
        sortedCards = list(deck.cards)
        sortedCards.sort(key=lambda card:card.front)
        self.lbl_length.config(text=f"{len(self.currentDeck)} cards")

        self.pagesList = []
        for p in range(countP):
            self.pagesList.append(tk.Frame(self.view, height=200, width= 600, bg="gray24"))
            self.pagesList[p].rowconfigure(list(range(pageMax)), weight=1)
            self.pagesList[p].columnconfigure(0, weight=1)

        for c in range(countC):
            lbl = ViewItem(self.pagesList[c//pageMax], sortedCards[c])
            lbl.grid(row=c%pageMax, column=0, sticky="nsew")
        if len(self.pagesList) > 0:
            self.pagesList[0].grid(row=0, column=0, sticky='nsew')

    def setupCallback(self, var, index, mode):
        self.setup()

    def switchPage(self, n):
        countP = len(self.pagesList)
        self.pagesList[self.pagePos].forget()
        self.pagePos = (self.pagePos + n) % countP
        self.pagesList[self.pagePos].tkraise()
        self.pagesList[self.pagePos].grid(row=0, column=0, sticky='nsew')

    def switchPageLeft(self):
        self.switchPage(-1)
    def switchPageRight(self):
        self.switchPage(1)

    def updateOptions(self):
        self.decks_ref = {}
        for deck in decks:
            self.decks_ref[deck.title] = deck

        menu = self.drop["menu"]
        menu.delete(0,'end')
        for deckTitle in self.decks_ref:
            menu.add_command(label=deckTitle, command=tk._setit(self.deckDest, deckTitle))
        self.deckDest.set(list(self.decks_ref.keys())[0])
        


    def editDeck(self):
        browse = app.browse
        deck = browse.currentDeck
        browse.frm_edit = EditFrameDeck(browse, self.currentDeck)
        browse.frm_edit.grid(row=0,column=0, sticky="nsew")        


    def delDeck(self):
        global decks
        if len(decks) < 2:
            showerror("Delete Deck","You cannot have 0 decks, add another deck before deleting this one.")
            return
        answer = askyesno(title="Delete Deck?", message="Are you sure you want to delete this deck? (This action cannot be undone)")
        if answer == False:
            return
        deck = self.currentDeck
        try:
            index = decks.index(deck)
        except ValueError:
            raise ValueError(f'Deck "{deck}" does not exist')
        app.home.delDeck(deck)
        decks.pop(index)


        self.updateOptions()
        app.add_frame.form_card.updateOptions()



class ViewItem(tk.Frame):
    def __init__(self, parent, card):
        tk.Frame.__init__(self, parent, height=50, width=100, borderwidth=1, relief="solid", bg="gray64")
        self.card = card
        self.rowconfigure(0,weight=1)
        self.columnconfigure((0,1,2),weight=3)
        self.columnconfigure(0, weight=20)
        self.item = tk.Label(self, text=str(card), font=("Calibri", 12), bg="gray64", width=1, height=1)
        self.item.grid(row=0, column=0, sticky="nsew")

        self.btn_edit = tk.Button(self, text="Edit", cursor="hand2", borderwidth=1, relief="solid", font=("Calibri", 12, "bold"), command=self.editCard)
        self.btn_edit.grid(row=0, column=1, sticky="nsew")

        self.btn_delete = tk.Button(self, text="\u274c", cursor="hand2", borderwidth=1,relief="solid", command=self.deleteCard)
        self.btn_delete.grid(row=0, column=2, sticky="nsew")

    def editCard(self):
        browse = app.browse
        deck= browse.currentDeck
        browse.frm_edit = EditFrame(browse, self.card)
        browse.frm_edit.grid(row=0,column=0, sticky="nsew")        


    def deleteCard(self):
        answer = askyesno(title="Delete Card?", message="Are you sure you want to delete this card? (This action cannot be undone)")
        if answer == False:
            return
        
        deck = app.browse.currentDeck
        deck.deleteCard(self.card)
        app.browse.setup()
        deck_frm = app.home.frames_ref[deck.title]
        deck_frm.updateCards()


class EditFrame(tk.Frame):
    def __init__(self, parent, card):
        tk.Frame.__init__(self, parent, height=300, width=600, bg='gray')
        global decks
        self.card = card
        self.columnconfigure((0,1,2), weight=1)
        self.rowconfigure((0,1,2,3), weight=1)

        self.lbl_front = tk.Label(self, text="Front: ")
        self.lbl_front.grid(row=1, column=0, sticky="nsew")

        self.ent_front = tk.Entry(self)
        self.ent_front.insert(0, card.front)
        self.ent_front.grid(row=1, column=1, columnspan=2, sticky="nsew")

        self.lbl_back = tk.Label(self, text="Back: ")
        self.lbl_back.grid(row=2, column=0, sticky="nsew")

        self.ent_back = tk.Entry(self)
        self.ent_back.insert(0, card.back)
        self.ent_back.grid(row=2, column=1, columnspan=2, sticky="nsew")

        self.btn_cancel = tk.Button(self, text="Cancel", cursor="hand2", width=1, command=self.exitScreen)
        self.btn_cancel.grid(row=3, column=0, sticky="nsew")

        self.btn_submit = tk.Button(self, text="Submit Changes", cursor="hand2", width=1, command=self.editSubmit)
        self.btn_submit.grid(row=3, column=2, sticky="nsew")

    def exitScreen(self):
        browse = app.browse
        editScreen = browse.frm_edit
        browseScreen = browse.frm_browse

        editScreen.grid_forget()
        browseScreen.tkraise()
        browseScreen.grid(row=0, column=0, sticky="nsew")

    def editSubmit(self):
        currentPage = app.browse.pagePos
        
        self.card.front = self.ent_front.get()
        self.card.back = self.ent_back.get()
        app.browse.setup()
        app.browse.switchPage(currentPage)
        
        deck = app.browse.currentDeck
        deck_frm = app.home.frames_ref[deck.title]
        deck_frm.updateCards()
        
        self.exitScreen()

class EditFrameDeck(tk.Frame):
    def __init__(self, parent, deck):
        tk.Frame.__init__(self, parent, height=300, width=600, bg="gray")
        global decks
        self.rowconfigure((0,1,2), weight=1)
        self.columnconfigure((0,1,2), weight=1)
        
        self.deck = deck

        self.lbl_title = tk.Label(self, text="Title: ")
        self.lbl_title.grid(row=1, column=0, sticky="nsew")

        self.ent_title = tk.Entry(self)
        self.ent_title.insert(0, self.deck.title)
        self.ent_title.grid(row=1, column=1, columnspan=2, sticky="nsew")

        self.btn_cancel = tk.Button(self, text="Cancel", cursor="hand2",  width=1, command=self.exitScreen)
        self.btn_cancel.grid(row=2, column=0, sticky="nsew")

        self.btn_submit = tk.Button(self, text="Submit Changes", cursor="hand2", width=1, command=self.editSubmit)
        self.btn_submit.grid(row=2, column=2, sticky="nsew")

    def exitScreen(self):
        browse = app.browse
        editScreen = browse.frm_edit
        browseScreen = browse.frm_browse

        editScreen.grid_forget()
        browseScreen.tkraise()
        browseScreen.grid(row=0, column=0, sticky="nsew")

    def editSubmit(self):
        new_title = self.ent_title.get()
        if new_title in app.browse.decks_ref:
            showerror(title="Error", message=f'{new_title} already exists')
            return
        self.deck.title = self.ent_title.get()
        app.browse.updateOptions()
        app.browse.deckDest.set(self.deck.title)
        app.browse.setup()

        app.add_frame.form_card.updateOptions()

        app.home.updateTitle()

        self.exitScreen()


#==========================================================
# Run App
#==========================================================


window = tk.Tk()

window.title("Flashcards")

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
app = App(window)
app.grid(row=0, column=0, sticky="nsew")

window.protocol("WM_DELETE_WINDOW", saveOnClose)


window.mainloop()
