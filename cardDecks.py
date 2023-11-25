import json

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


if __name__ == "__main__":

    card1 = Card('a','A')
    card2 = Card('b','B')
    card3 = Card('c','C')
    card4 = Card('d','D')
    card5 = Card('e','E')
    cardA = Card('a','A')
    cardB = Card('b','B')
    cardlist= [card1, card2, card3, card4, card5]

    deck1 = Deck('Deck1', cardlist)

    # print(deck1.cards.index("a"))

    deck1.deleteCard(card1)
    deck1.deleteCard(card3)

    # # print(card1)
    # # print(deck1.cards)
    # deck1.printCards()
    # print('------')
    # f = {'f':'F'}
    # deck1.add(f)
    # deck1.create_add('f','F')
    # print(deck1.cards[-1])
    # print('-----')
    # g = Card('g','G')
    # deck1.add(g)
    # print(deck1.cards[-1])
    # print(deck1.cards)

    # deck2 = Deck('Deck2')

    # print(deck2)

    deck3 = Deck('Deck3', 'Hello')
    # deck3.printCards()

    # print('-----')

    deck4 = Deck("Deck4", [card1,'aaaa',0, None, card2, card3])
    # deck4.printCards()

    # print(card1.convJson())
    # print(deck1.convJson())
    # print('--------')
    # print(json.dumps(deck1.convJson(), indent=4))

    # with open("./decks.json","r") as f:
    #     data = json.load(f)

    # decks = []
    # for deck in data:
    #     cards = Deck.createCards(data[deck]["cards"])
    #     decks.append(Deck(data[deck]["name"], cards))

    # print(decks[0].cards[0].back)
    
