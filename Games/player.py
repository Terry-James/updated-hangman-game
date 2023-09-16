class Player:
    def __init__(self):
        self.words_correct = 0
        self.words_incorrect = 0

    def get_words_correct(self):
        return self.words_correct

    def set_words_correct(self, words_correct):
        self.words_correct = words_correct

    def get_words_incorrect(self):
        return self.words_incorrect

    def set_words_incorrect(self, words_incorrect):
        self.words_incorrect = words_incorrect

    def update_correct_word(self):
        self.words_correct += 1
    
    def update_incorrect_word(self):
        self.words_incorrect += 1