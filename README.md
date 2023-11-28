# CS499DD
Project for CS499

## Flashcards

This app is used to make digital flashcards. Flashcards are added to decks
and decks can be studied.

In order to run Fkashcards, you must have Python 3.7 or later installed on your computer.

Run Flashcards:

1. Open a terminal
2. Go to the folder/directory where the file is stored
3. * If on Windows, type `python .\Flashcards.py` and hit Enter.
    * On Linux or Mac, type `python3 ./Flashcards.py` and hit Enter.

# App Explanation

### Cards

A *card* refers to a single flashcard. On the card, there is a front side
and a back side. While studying, the front of the card will show up first,
and the back of the card will be shown when the card is flipped.

### Decks

A *deck* refers to a collection of *cards*. Cards must belong to a deck.
When studying, the user will study a single deck. The cards that will show up
are only the cards that belong to the deck being studied.

## Home

The *Home* tab is the main page. On this tab, there will be a list of Decks
created by the user. When a deck is clicked on, the *Home* tab will change to
display the cards from the deck. Cards are ordered randomly every time the app
runs.

The user can flip the card by clicking on the card or by clicking the "Flip"
button. The cards can be cycled through by clicking on either of the arrow
buttons. A "Back" button will be in the upper left corner. Clicking on this
will switch the page back to the list of decks.

## Add Cards

The "Add Cards" tab is where you can add new cards to a deck or create a new
deck. On this tab, there are two forms. The first form is to add a new card to
a deck. The second form is to create a new deck.

The first form has three fields. These are "Deck," "Front," and "Back." The
"Deck" field is a dropdown menu that specifies which deck the card will be
added to. The "Front" and "Back" fields are Entries where you will type what
you want to show on that side of the card. Clicking "Submit" will add the card
to the specified deck.

The second form is a single field. This field is for the name of the new deck
to be created. You type the name in the field and hit the "Submit" button
to create the deck. All Decks must have unique names.

## Browse

The *Browse* tab is where you can view all the cards in a deck, listed in 
alphabetical order. At the very top of the page is a drop down menu showing
the name of the deck currently being displayed. Clicking on the dropdown menu 
and then clicking on a new deck will change the cards being displayed. To the
right of the dropdown menu are 2 buttons. The "Edit" button will bring up a
form where you can change the name of the current deck. All decks will still
need to have unique names. The "X" button is used to delete the current deck.
You cannot have less than 1 deck.

Under the dropdown menu is a list of cards. These are the cards in the deck 
in alphabetical order. Ten cards will be displayed on a page, and pages can be
cycled through using the arrow buttons. 2 buttons will appear to the right of
each card. The "Edit" button allows you to change the front and/or back of the
card. The "X" button will delete the card.

## Save

The *Save* tab is a normal button. Clicking on this will save the cards to a 
JSON file, and a notification will show up confirming the cards were saved.

When exiting the app, you will be asked whether you want to save before 
quiting. Even if you just saved, this message will still appear. It is just
for avoiding forgetting to save the cards.

Data will be saved on a JSON file in the same directory/folder as the script
to run the app. The file is "decks.json" and is required to be in the same
folder as the script. If the file is not in the directory, a new file will 
be created with a single empty deck. The file consists of objects representing
each deck. Within these objects is a list of the cards in the deck. These
are also represented as objects.
