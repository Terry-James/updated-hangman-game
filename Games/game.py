from graphics import *
from time import *
from player import *

#git practice change
windowX = int(1000)
windowY = int(1000)
used_letters = []

class HiddenWord:
    def __init__(self):
        self.hidden_word = ""
    
    def get_hidden_word(self):
        return self.hidden_word
    
    def set_hidden_word(self, hidden_word):
        self.hidden_word = hidden_word

def main():
    mainWindow = createWindow()
    closeWindow(mainWindow)

def rebuildDisplay(secret_word): # Function to rebuild the hidden word to display the correct _ with correct characters
    new_word = ""
    for word in secret_word:
        if word != "_":
            new_word += word + " "
        else:
            new_word += "_ "
    return new_word.strip()

def wordTiles(window, current_word, state, player_input, hidden_word): # Function for getting the word to show up a individual _ representing each character
    temp_word = ""
    if state == "new state":
        for i in range(len(current_word) - 1):
            temp_word += "_ "
            hidden_word.set_hidden_word(temp_word)
    else:
        if len(player_input) == 1: #Done Tested
            for i in range(len(current_word) - 1):
                if player_input.lower() == current_word[i].lower():
                    update_word = hidden_word.get_hidden_word().split()
                    update_word[i] = player_input.lower()
                    temp_word = rebuildDisplay(update_word)
                    hidden_word.set_hidden_word(temp_word)
        else:
            if player_input.lower().strip() == current_word.lower().strip():
                temp_word = current_word
                hidden_word.set_hidden_word(temp_word)
            else:
                print("Enter single characters or whole words inside wordtiles")

    return hidden_word.get_hidden_word().strip()

def displayWordTiles(window, hidden_word): #Function for displaying wordTile
    draw_word = Text(Point(windowX/2 - 50, windowY/2 + 5), hidden_word)
    try:
        draw_word.undraw()
        draw_word.draw(window)
    except:
        draw_word.draw(window)
    return draw_word

def checkInput(current_word, player_input): #Function for check if the character or word entered by the play is correct or not
    check_result = False

    if len(player_input) == 1:
        if player_input.strip() in current_word:
            check_result = True
    else:
        if player_input.lower().strip() == current_word.lower().strip():
            check_result = True
        else:
            #TODO add function to split multiple character entry and check if each letter is in the word.
            print("Enter single characters or whole words")

    return check_result

def usedLetters(window, player_input): #Function to check if letter has already been used
    used_before = False
    if len(player_input) == 1:
        if player_input not in used_letters:
            used_letters.append(player_input)
        else:
            used_before = True
    
    return used_before

def gameWin(current_word, hidden_word): #Function to check if word has been completed
    winner = False
    current = ""
    print(current_word)
    if current_word.lower().strip() == hidden_word.lower().strip():
        winner = True
    else:
        for i in range(len(current_word)):
            if current_word[i] != " ":
                current += current_word[i]
       
        if current.lower().strip() == hidden_word.lower().strip():
            winner = True
    
    return winner

def fixCurrentWord(current_word): #Function to get the format for the current word to match what the hidden format will look like
    word = ""
    for current_letter in current_word:
        word += current_letter + " "
    return word

def gameloop(background, window): # Function for main game loop
    hidden_word = HiddenWord()
    player = Player()
    game_words = getWords("Hangman.txt") # Returns an array of words
    current_tries = 0
    word_index = 0
    stage_names = ["Stage2", "Stage3", "Stage4", "Stage5", "Stage6", "Stage7"]

    while len(game_words) > word_index:
        print("outer while game loop")
        print(word_index)
        win = False
        current_word = game_words[word_index]
        current_hidden = wordTiles(window, current_word, "new state", "", hidden_word)
        fixed_word = fixCurrentWord(current_word)
        draw_word = displayWordTiles(window, current_hidden)
        entry_box = playerInputBox(window, len(current_word))

        while current_tries <= 7 and win == False:
            print("inside while for current tries")
            win = gameWin(fixed_word, hidden_word.get_hidden_word())
            if win == True:
                print("Game Won Next Word.")
                draw_word.undraw()
                used_letters.clear()
                current_tries = 0
                backgrounds("new game", window, background)
                break
            mouse = window.getMouse() # wait for mouse click so player can enter answer
            xcoord = mouse.getX()
            ycoord = mouse.getY()
            if ((625 <= xcoord <= 684) and (540 <= ycoord <= 559)):
                player_input = entry_box.getText()
                used_result = usedLetters(window, player_input)# check if letter in entry has already been used
                if used_result == True: # start the loop over if true since the letter entered has already been used
                    entry_box.setText("")
                    continue
                check_result = checkInput(current_word, player_input)
                if check_result == True:
                    entry_box.setText("")
                    current_hidden = wordTiles(window, current_word, "", player_input, hidden_word)
                    draw_word.undraw()
                    draw_word = displayWordTiles(window, current_hidden) 
                else:
                    entry_box.setText("")
                    backgrounds(stage_names[current_tries], window, background)
                    current_tries += 1
        word_index += 1

def createWindow(): #Create main window
    window = GraphWin("Game Window", windowX, windowY)
    window.setBackground("yellow")
    background = backgrounds("default", window, "")

    if window.getMouse():
        background = backgrounds("new game", window, background)
        gameloop(background, window)

    return window

def backgrounds(stage, window, old_background): #Funtion to set all stage background images
    background = ""

    if stage == 'default':
        background = Image(Point(windowX/2, windowY/2), "Stage0.gif")
        background.draw(window)
    elif stage == 'new game':
        old_background.undraw()
        background = Image(Point(windowX/2, windowY/2 - 300), "Stage1.gif")
        background.draw(window)
        createAlphabet(window)
    else:
        old_background.undraw()
        background = Image(Point(windowX/2, windowY/2 - 300), (stage + ".gif"))
        background.draw(window)

    return background  

def closeWindow(window): #Function to close window on final click
    window.getMouse()
    window.close()

def playerInputBox(window, word_length): #Function for creating input box for player
    input_label = Text(Point(windowX/2 - 50, windowY/2 + 50), "Enter letter or word: ")
    input_label.draw(window)
    input_box = Entry(Point(windowX/2 + 75, windowY/2 + 50), word_length)
    input_box.draw(window)
    submit_button = Rectangle(Point(625,540), Point(684, 559))
    submit_button.draw(window)
    submit_label = Text(Point(655, 550), "Submit")
    submit_label.draw(window)

    return input_box

def createAlphabet(window): #Function to set the starting alphabet
    alpha = ['A','B','C','D','E','F','G','H','I','J','K',
            'L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','','']
    for i in range (len(alpha) - 1):
        singleLetter = Text(Point((windowX/2 - 200) + (i*15), windowY/2 + 100), alpha[i])
        singleLetter.draw(window)

def getWords(filedata): #Function to get the words from a file that will be used in the game
    words = []
    List_of_Words = open (filedata, 'r')
    allWords = List_of_Words.readlines()
    List_of_Words.close()

    # make sure each word is lowercase
    for i in range (len (allWords)):
        choosenWord = allWords[i].lower()
        words.append(choosenWord)

    return words
main()