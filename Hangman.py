import pyglet
import arcade
import random
from PyDictionary import PyDictionary
from tkinter import *

PyDictionary = PyDictionary("html.parser")

word_file = "C:\\Users\\palli\\PycharmProjects\\HangMan\\words.txt"
words = open(word_file).read().splitlines()

def isVowel(letter):
	if letter == 'A' or letter == 'E' or letter == 'I' or letter == 'O' or letter == 'U':
		return True

	return False


def find_nth(haystack, needle, n):
	start = haystack.find(needle)
	while n > 1:
		start = haystack.find(needle, start + len(needle))
		if start < 0:
			break
		n -= 1
	return start


def countVowels(word):
	count = 0
	for i in range(len(word)):
		if isVowel(word[i]):
			count += 1

	return count


class Game(arcade.Window):
	STATE = 0
	CURRENT_WORD = ''
	LETTERS_TO_DRAW = []
	KEYS_TO_DRAW = []
	MISTAKES = 0
	CLUE = ''
	NOT_LOST = False
	LETTERS_USED = []

	not_played_win_or_lose_sound = 0

	def __init__(self, width, height, title):
		# Call the parent class's init function
		super().__init__(width, height, title)

		arcade.set_background_color(arcade.color.BANANA_YELLOW)

	def on_draw(self):
		arcade.start_render()
		self.draw()

	def draw(self):
		if self.STATE == 0:
			self.NOT_LOST = True
			self.CURRENT_WORD = ''
			self.LETTERS_TO_DRAW = []
			self.KEYS_TO_DRAW = []
			self.MISTAKES = 0
			self.not_played_win_or_lose_sound = 0
			self.LETTERS_USED = []

			arcade.draw_text('Welcome To Hangman!', 40, 500, arcade.color.RED, 40)
			arcade.draw_text('A Game By Joseph Pallipadan', 50, 430, arcade.color.RED, 30)
			arcade.draw_text('Press Shift for 1 Player |', 30, 30, arcade.color.BLACK, 20)
			arcade.draw_text('Press Enter for 2 Players', 300, 30, arcade.color.BLACK, 20)

			# Face
			arcade.draw_circle_filled(300, 380, 30, arcade.color.BLACK)

			# Eyes
			arcade.draw_circle_filled(315, 390, 3, arcade.color.WHITE)
			arcade.draw_circle_filled(285, 390, 3, arcade.color.WHITE)

			# Mouth
			arcade.draw_line(290, 370, 310, 370, arcade.color.WHITE, 2)

			# Chest
			arcade.draw_rectangle_filled(298, 285, 80, 120, arcade.color.BLACK)

			# Hands
			arcade.draw_rectangle_filled(240, 275, 20, 140, arcade.color.BLACK)
			arcade.draw_rectangle_filled(355, 275, 20, 140, arcade.color.BLACK)

			# Legs
			arcade.draw_rectangle_filled(275, 150, 30, 140, arcade.color.BLACK)
			arcade.draw_rectangle_filled(320, 150, 30, 140, arcade.color.BLACK)

		if self.STATE != 0:
			arcade.draw_text('Press Esc To Go Back', 470, 580, arcade.color.BLACK, 10)
			if self.STATE == 1:
				arcade.draw_text('1 Player Mode', 5, 580, arcade.color.BLACK, 10)
			else:
				arcade.draw_text('2 Player Mode', 5, 580, arcade.color.BLACK, 10)

			if self.CURRENT_WORD != '' and len(self.LETTERS_TO_DRAW) != len(self.CURRENT_WORD) - countVowels(
					self.CURRENT_WORD) - self.CURRENT_WORD.count(' '):
				arcade.draw_line(160, 490, 300, 490, arcade.color.BLACK, border_width=3)
				arcade.draw_line(160, 430, 220, 490, arcade.color.BLACK, border_width=3)
				arcade.draw_line(300, 490, 300, 470, arcade.color.BLACK, border_width=3)
				arcade.draw_line(160, 490, 160, 110, arcade.color.BLACK, border_width=3)
				arcade.draw_line(80, 110, 240, 110, arcade.color.BLACK, border_width=5)

		if self.MISTAKES <= 7 and (self.NOT_LOST or len(self.CURRENT_WORD) == 0) and self.STATE != 0:

			if self.CURRENT_WORD == '':
				random_num = random.randrange(len(words))

				# while PyDictionary.synonym(words[random_num])[0] == "":
				# 	random_num = random.randrange(len(words))
				#
				# synonym_list = PyDictionary.synonym(self.CURRENT_WORD)
				# synonym = str(synonym_list[0])
				self.CURRENT_WORD = words[random_num]
				self.CLUE = self.CURRENT_WORD[:3]

			arcade.draw_text('Guess The Word Based On The Clue And The Filled Vowels!', 25, 550, arcade.color.RED, 15)
			arcade.draw_text('Press The Key For A Letter You Think Is In The Word', 50, 525, arcade.color.RED, 15)
			arcade.draw_text('If Hangman Completely Appears, You Lose!', 100, 500, arcade.color.RED, 15)
			arcade.draw_text('Clue : ' + str(self.CLUE), 10, 10, arcade.color.RED, 15)
			arcade.draw_line(548, 120, 548, 555, arcade.color.BLACK)
			arcade.draw_line(548, 555, 600, 555, arcade.color.BLACK)
			arcade.draw_line(548, 120, 600, 120, arcade.color.BLACK)
			arcade.draw_text('Letters \n Used: ', 555, 540, arcade.color.BLACK, 10)

			for i in range(len(self.CURRENT_WORD)):

				letter = self.CURRENT_WORD[i]

				if letter != ' ':
					arcade.draw_line(5 + 40 * i, 70, 35 + 40 * i, 70, arcade.color.BLACK)

				if isVowel(letter):
					arcade.draw_text(letter, 15 + 40 * i, 75, arcade.color.RED, 15)

			for i in range(len(self.LETTERS_TO_DRAW)):
				arcade.draw_text(self.LETTERS_TO_DRAW[i], 15 + 40 * (self.KEYS_TO_DRAW[i]), 75, arcade.color.RED, 15)

			for i in range(len(self.LETTERS_USED)):
				arcade.draw_text(self.LETTERS_USED[i], 565, 500 - 25 * i, arcade.color.BLACK, 15)

			if self.MISTAKES >= 1:
				arcade.draw_circle_filled(300, 440, 30, arcade.color.BLACK)

			if self.MISTAKES >= 2:
				arcade.draw_rectangle_filled(298, 345, 80, 120, arcade.color.BLACK)

			if self.MISTAKES >= 3:
				arcade.draw_rectangle_filled(355, 335, 20, 140, arcade.color.BLACK)

			if self.MISTAKES >= 4:
				arcade.draw_rectangle_filled(240, 335, 20, 140, arcade.color.BLACK)

			if self.MISTAKES >= 5:
				arcade.draw_rectangle_filled(320, 210, 30, 140, arcade.color.BLACK)

			if self.MISTAKES >= 6:
				arcade.draw_rectangle_filled(275, 210, 30, 140, arcade.color.BLACK)

			if self.MISTAKES >= 7:
				arcade.draw_circle_filled(315, 450, 3, arcade.color.WHITE)
				arcade.draw_circle_filled(285, 450, 3, arcade.color.WHITE)

				arcade.draw_line(290, 430, 310, 430, arcade.color.WHITE, 2)

			self.NOT_LOST = len(self.LETTERS_TO_DRAW) != len(self.CURRENT_WORD) - self.CURRENT_WORD.count(
				' ') - countVowels(self.CURRENT_WORD)

		elif self.MISTAKES > 7 and self.STATE != 0:

			arcade.draw_circle_filled(300, 440, 30, arcade.color.BLACK)
			arcade.draw_rectangle_filled(298, 345, 80, 120, arcade.color.BLACK)
			arcade.draw_rectangle_filled(355, 335, 20, 140, arcade.color.BLACK)
			arcade.draw_rectangle_filled(240, 335, 20, 140, arcade.color.BLACK)
			arcade.draw_rectangle_filled(320, 210, 30, 140, arcade.color.BLACK)
			arcade.draw_rectangle_filled(275, 210, 30, 140, arcade.color.BLACK)

			arcade.draw_line(280, 445, 290, 455, arcade.color.WHITE)
			arcade.draw_line(280, 455, 290, 445, arcade.color.WHITE)
			arcade.draw_line(310, 445, 320, 455, arcade.color.WHITE)
			arcade.draw_line(310, 455, 320, 445, arcade.color.WHITE)

			arcade.draw_line(290, 420, 300, 430, arcade.color.WHITE)
			arcade.draw_line(300, 430, 310, 420, arcade.color.WHITE)

			if self.STATE == 1:
				arcade.draw_text('You Have Lost!', 120, 520, arcade.color.RED, 40)
			if self.STATE == 2:
				arcade.draw_text('The Word Setter Has Won!', 40, 520, arcade.color.RED, 35)

			arcade.draw_text('The Word Was: ' + self.CURRENT_WORD, 10, 10, arcade.color.BLACK, 15)

			if self.not_played_win_or_lose_sound < 2:
				if self.not_played_win_or_lose_sound == 1:
					song = pyglet.media.load('C:\\Users\\palli\\PycharmProjects\\HangMan\\Lose_Sound.wav')
					song.play()

				self.not_played_win_or_lose_sound += 1

		elif self.STATE != 0:
			arcade.draw_text('You Have Won!', 110, 520, arcade.color.RED, 40)
			arcade.draw_text('Mistakes Made: ' + str(self.MISTAKES), 10, 10, arcade.color.BLACK, 15)
			arcade.draw_text('The Word Was: ' + self.CURRENT_WORD, 10, 30, arcade.color.BLACK, 15)

			arcade.draw_circle_filled(300, 440, 30, arcade.color.BLACK)
			arcade.draw_rectangle_filled(298, 345, 80, 120, arcade.color.BLACK)
			arcade.draw_rectangle_filled(355, 335, 20, 140, arcade.color.BLACK)
			arcade.draw_rectangle_filled(240, 335, 20, 140, arcade.color.BLACK)
			arcade.draw_rectangle_filled(320, 210, 30, 140, arcade.color.BLACK)
			arcade.draw_rectangle_filled(275, 210, 30, 140, arcade.color.BLACK)

			arcade.draw_line(278, 445, 283, 450, arcade.color.WHITE)
			arcade.draw_line(283, 450, 288, 445, arcade.color.WHITE)

			arcade.draw_line(313, 445, 318, 450, arcade.color.WHITE)
			arcade.draw_line(318, 450, 323, 445, arcade.color.WHITE)

			arcade.draw_line(291, 430, 301, 420, arcade.color.WHITE)
			arcade.draw_line(301, 420, 311, 430, arcade.color.WHITE)

			if self.not_played_win_or_lose_sound < 2:
				if self.not_played_win_or_lose_sound == 1:
					song = pyglet.media.load('C:\\Users\\palli\\PycharmProjects\\HangMan\\Win_Sound.mp3')
					song.play()
				self.not_played_win_or_lose_sound += 1

	def on_key_press(self, key, modifiers):
		if self.STATE == 0:

			if key == arcade.key.LSHIFT:
				self.STATE = 1
				self.on_draw()

			if key == arcade.key.ENTER:
				self.STATE = 2

				def set_2Player_Details():
					self.CLUE = e2.get()
					self.CURRENT_WORD = str(e1.get()).upper()
					self.NOT_LOST = True

				master = Tk()
				Label(master, text="Enter A Phrase Less Than 15 Characters Long And A Clue. Don't Let Your Friend See!").grid(
					row=0, column=0)
				Label(master, text="Word:").grid(row=2)
				Label(master, text="Clue:").grid(row=3)
				Label(master, text="Once You're Done, Click OK and close this window").grid(row=5, column=0)

				e1 = Entry(master)
				e2 = Entry(master)

				e1.grid(row=2, column=1)
				e2.grid(row=3, column=1)

				Button(master, text='         OK         ', command=set_2Player_Details).grid(row=4, column=1, sticky=W)
				mainloop()

				self.on_draw()

		if self.STATE != 0:

			if key == arcade.key.ESCAPE:
				self.STATE = 0
				self.on_draw()

			if 0 <= key - 97 < 26 or 0 <= key - 48 <= 9:
				letters = (
					'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
					'U',
					'V', 'W', 'X', 'Y', 'Z')
				numbers = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

				if 0 <= key - 97 < 26:
					key_pressed = letters[key - 97]
				else:
					key_pressed = numbers[key - 48]

				prev_mistakes = self.MISTAKES
				if self.CURRENT_WORD.__contains__(key_pressed) and not isVowel(key_pressed) and not self.LETTERS_USED.__contains__(key_pressed):
					song = pyglet.media.load('C:\\Users\\palli\\PycharmProjects\\HangMan\\Correct.wav')
					song.play()
					for i in range(self.CURRENT_WORD.count(key_pressed)):
						self.LETTERS_TO_DRAW.append(key_pressed)
						self.KEYS_TO_DRAW.append(find_nth(self.CURRENT_WORD, key_pressed, i + 1))

				elif not isVowel(key_pressed) and not self.LETTERS_USED.__contains__(key_pressed):
					self.MISTAKES += 1
					song = pyglet.media.load('C:\\Users\\palli\\PycharmProjects\\HangMan\\Mistake.wav')
					song.play()

				if not self.LETTERS_USED.__contains__(key_pressed) and not isVowel(key_pressed):
					self.LETTERS_USED.append(key_pressed)

				elif self.MISTAKES == prev_mistakes:
					song = pyglet.media.load('C:\\Users\\palli\\PycharmProjects\\HangMan\\Mistake.wav')
					song.play()

			self.on_draw()


window = Game(600, 600, "Hangman")
arcade.run()
pyglet.app.run()
