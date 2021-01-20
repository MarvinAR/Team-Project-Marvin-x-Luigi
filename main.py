
#************************#
# ~~~ PYTHON MODULES ~~~ #
#************************#

import pygame
from   datetime       import datetime
from   sys            import exit
from   random         import randint
from   playsound      import playsound
from   json           import dump
from   tkinter        import messagebox as Msg
from   tkinter        import Tk, Label
from   time           import sleep
from   PIL            import Image, ImageTk

#*********************#
# ~~~ CONTROLLERS ~~~ #
#*********************#

from controller       import settings, button
from controller.stats import GameStatistics
from controller.score import Scoreboard

#*************************#
# ~~~ MODELS / ASSETS ~~~ #
#*************************#

from models.monsters  import TinyMonster, MediumMonster, LargeMonster, Boss
from models.bg        import Bg
from models.life      import Life
from models.innocent  import Innocent
from models.potion    import Potion


class Game:

	def __init__(self):
		pygame.init()

		#*****************************************#
		# OBJECT YANG INVISIBLE BEHIND THE SCREEN #
		#*****************************************#

		self.game_settings = settings.Settings()
		self.screen        = pygame.display.set_mode([self.game_settings.screen_width, self.game_settings.screen_height])
		self.screen_rect   = self.screen.get_rect()
		self.title         = pygame.display.set_caption(self.game_settings.title)

		self.running       = True
		self.counter       = 0
		self.boss_counter  = 0

		self.current_time        = 0
		self.potion_pressed_time = 0

		#*************************#
		# BOOLEAN TYPE INDICATORS #
		#*************************#

		self.create_tiny_monster   = False
		self.create_medium_monster = False
		self.create_large_monster  = False
		self.create_innocent       = False
		self.create_potion         = False

		#*****************************************************#
		# Group OBJEK / MODELS IN OUR GAME (OBJECT IN OBJECT) #
		#*****************************************************
		#
		self.game_tiny_monster   = pygame.sprite.Group()

		self.game_medium_monster = pygame.sprite.Group()

		self.game_large_monster  = pygame.sprite.Group()

		self.game_innocent       = pygame.sprite.Group()

		self.game_potion         = pygame.sprite.Group()

		#*****************************************#
		# OBJECT YANG INVISIBLE BEHIND THE SCREEN #
		#*****************************************#
		self.game_boss = Boss(self)

		#*******************#
		# ON SCREEN OBJECTS #
		#*******************#

		self.bg_screen = Bg(self)
		self.stats     = GameStatistics(self)
		self.score     = Scoreboard(self)

		#*******************#
		# BUTTONS INITIATON #
		#*******************#

		self.play_button  = button.Button(self, "PLAY")
		self.reset_button = button.Button_2(self, "RESET")
		self.exit_button  = button.Button_3(self, "EXIT")
		self.pause_button = button.Button_4(self, "||")
		self.help_button  = button.Button_5(self, "?")
		self.life         = Life(self)

	#*****************************#
	# ~~~ PROPERTY GAME UTAMA ~~~ #
	#*****************************#

	def run_game(self):
		while self.running:
			self.rg_check_events()

			if self.stats.game_active:
				self.bg_screen.update()

				self.rg_game_over_check()

				tiny_monsters = self.game_tiny_monster.sprites()
				for tinyMonster in tiny_monsters:
					tinyMonster.update()

				med_monsters  = self.game_medium_monster.sprites()
				for medMonster in med_monsters:
					medMonster.update()

				large_monsters = self.game_large_monster.sprites()
				for largeMonster in large_monsters:
					largeMonster.update()

				innocents     = self.game_innocent.sprites()
				for innocent in innocents:
					innocent.update()

				potions       = self.game_potion.sprites()
				for potion in potions:
					potion.update()

				#self.update_boss()
				self.beyond_the_screen_check()
				#print(len(self.game_tiny_monster))

			self.rg_update_screen()

	def rg_check_events(self):
		events = pygame.event.get()
		#print(events)

		for event in events:
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYDOWN:
				self.rg_check_keydown_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.rg_check_mousebutton_down(event.button)

	def rg_check_mousebutton_down(self, event_button):
		if event_button == 1:
			mouse_pos = pygame.mouse.get_pos()
			monster_hit = pygame.mouse.get_pos()
			
			self._check_play_button(mouse_pos)
			self._check_monsters_hit(monster_hit)
			self._check_pause_button(mouse_pos)
			#self.tap_boss(monster_hit)

			if not self.stats.game_active:
				self._check_reset_button(mouse_pos)
				self._check_exit_button(mouse_pos)
				self._check_help_button(mouse_pos)

	def rg_check_keydown_events(self, event):
		if event.key == pygame.K_q:
			exit()

	def rg_update_screen(self):
		self.bg_screen.blitme()
		if self.stats.game_active:
			#if self.stats.level % 5 != 0:
			#self.game_settings.monsters_speed = 2
			self.update_tiny_monsters()
			self.update_medium_monsters()
			self.update_large_monsters()
			self.update_innocent()
			self.update_potion()

			self.score.create_cover(self)
			self.pause_button._draw_button()

			#else:
				#self.game_settings.monsters_speed = 0
				#self.update_boss()

			self.score.draw_score()

			self.show_healthbar()
			#self.update_medium_monsters()
			#self.update_large_monsters()
			
		if not self.stats.game_active:
			self.play_button._draw_button()
			self.reset_button._draw_button()
			self.exit_button._draw_button()
			img_menu = pygame.image.load('img/main_menu.png')
			img_rect_menu = img_menu.get_rect()
			self.screen.blit(img_menu, img_rect_menu)
			self.help_button._draw_button()


		pygame.display.flip()

	def rg_game_over_check(self):
		if self.game_settings.life == 0:
			self.stats.game_active = False
			#print("Game Over")
			self.game_settings.life = 3

	#**************#
	# ~~~ LIFE ~~~ #
	#**************#

	def show_healthbar(self):
		if self.game_settings.life !=0:

			if self.game_settings.life > 3:
				self.game_settings.life = 3

			#print(self.game_settings.life)

			self.life.show_life_background()
			self.life.show_string()
			if self.game_settings.life == 1:
				self.life.show_red()
			if self.game_settings.life == 2:
				self.life.show_yellow()
			if self.game_settings.life == 3:
				self.life.show_green()

	#*****************#
	# ~~~ BUTTONS ~~~ #
	#*****************#

	def _check_play_button(self, mouse_pos):

		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		status = self.stats.game_active

		if button_clicked and not status:

			self.stats.game_active = True

			if self._check_pause_button(mouse_pos):
				self.stats.reset_statistics()

			self.score.show_score()
			self.score.check_high_score()

	def _check_reset_button(self, mouse_pos):
		button_clicked = self.reset_button.rect.collidepoint(mouse_pos)

		if button_clicked:

			Tk().withdraw()
			result_user = Msg.askyesno("Confirmation", "Are you sure to reset the highscore that you've made so far ?")

			if result_user:
				with open('highscore.json', "w") as f:
					self.stats.high_score = 0
					dump(self.stats.high_score,f)

				self.stats.reset_statistics()

				self.score.show_score()
				self.score.check_high_score()

	def _check_pause_button(self, mouse_pos):
		button_clicked   = self.pause_button.rect.collidepoint(mouse_pos)

		if button_clicked:
			self.stats.game_active = False

	def _check_exit_button(self, mouse_pos):
		button_clicked = self.exit_button.rect.collidepoint(mouse_pos)

		if button_clicked:
			Tk().withdraw()
			result_user = Msg.askyesno("Confirmation", "Are you sure to exit the game ?")

			if result_user:
				quit()

	def _check_help_button(self, mouse_pos):
		button_clicked = self.help_button.rect.collidepoint(mouse_pos)

		if button_clicked:
			window = Tk()
			window.title("Directions")

			title1 = Label(window, text='About Game', font=('arial', 18, 'bold'))
			title1.grid(column = 2, row = 0)

			title2 = Label(window, text='Monsters', font=('arial', 18, 'bold'))
			title2.grid(column = 1, row = 0)

			title3 = Label(window, text='RARE Entity', font=('arial', 18, 'bold'))
			title3.grid(column = 4, row = 0)

			title4 = Label(window, text='Info', font=('arial', 18, 'bold'))
			title4.grid(column = 2, row = 2)

			open_tiny_image = Image.open('tinyImg/tiny.png')
			tiny_image_done = ImageTk.PhotoImage(open_tiny_image)
			tiny_image_label = Label(window, image=tiny_image_done)
			tiny_image_label.grid(column = 0, row = 1)

			tiny_description = """
Stone Golem a.k.a Tiny Monster
Killed : Score +15
Passed : Score -5, Life -1
			"""

			tiny_description_label = Label(window, text=tiny_description, font=('arial', 12))
			tiny_description_label.grid(column = 1, row = 1)

			open_med_image = Image.open('tinyImg/medium.png')
			med_image_done = ImageTk.PhotoImage(open_med_image)
			med_image_label = Label(window, image=med_image_done)
			med_image_label.grid(column = 0, row = 2)

			med_description = """
Mythical Wolf a.k.a Medium Monster
Killed : Score +10
Passed : Score -10, Life -1
			"""

			med_description_label = Label(window, text=med_description, font=('arial', 12))
			med_description_label.grid(column = 1, row = 2)

			open_large_image = Image.open('tinyImg/large.png')
			large_image_done = ImageTk.PhotoImage(open_large_image)
			large_image_label = Label(window, image=large_image_done)
			large_image_label.grid(column = 0, row = 3)

			large_description = """
Demon Dragon a.k.a Large Monster
Killed : Score +5
Passed : Score -15, Life -1
			"""

			large_description_label = Label(window, text=large_description, font=('arial', 12))
			large_description_label.grid(column = 1, row = 3)

			open_boss_image = Image.open('tinyImg/bos.png')
			boss_image_done = ImageTk.PhotoImage(open_boss_image)
			boss_image_label = Label(window, image=boss_image_done)
			boss_image_label.grid(column = 3, row = 1)

			boss_description = """
Prehistoric Giant Turtle a.k.a Boss
10 Taps required
Killed : Score +50
			"""

			boss_description_label = Label(window, text=boss_description, font=('arial', 12))
			boss_description_label.grid(column = 4, row = 1)

			open_human_image = Image.open('tinyImg/innocent.png')
			human_image_done = ImageTk.PhotoImage(open_human_image)
			human_image_label = Label(window, image=human_image_done)
			human_image_label.grid(column = 3, row = 2)

			human_description = """
Human a.k.a Innocent
Killed : Score -10, Life -1
Passed : Score +15, Life +1
			"""

			human_description_label = Label(window, text=human_description, font=('arial', 12))
			human_description_label.grid(column = 4, row = 2)

			open_potion_image = Image.open('tinyImg/potion.png')
			potion_image_done = ImageTk.PhotoImage(open_potion_image)
			potion_image_label = Label(window, image=potion_image_done)
			potion_image_label.grid(column = 3, row = 3)

			potion_description = """
Freeze Time Potion
Tapped : Time Freeze
Duration : at least 2 seconds
Tips : Tap after 2 seconds, tap anywhere to continue.
			"""

			potion_description_label = Label(window, text=potion_description, font=('arial', 12))
			potion_description_label.grid(column = 4, row = 3)

			tips_description = """
This is basically a tapping game.
In this game, you only have 3 lives.
Monsters, potions, innocents will fall from the top of the screen.
Tap them to get points, but don't tap the innocent
because you will gain some points and restore 1 life.
			"""

			tips_description_label = Label(window, text=tips_description, font=('Comic Sans Ms', 10))
			tips_description_label.grid(column = 2, row = 1)

			about_description = """
Developed by Marvin AR and Luigi E
Antah Berantah
Contact : -1 - 2345 - 6789
Since December 2020
© 2021 Project. All rights reserved. 
			"""

			about_description_label = Label(window, text=about_description, font=('Comic Sans Ms', 15))
			about_description_label.grid(column = 2, row = 3)

			window.mainloop()



	def _check_monsters_hit(self, monster_hit):

		for tinyMonster in self.game_tiny_monster.copy():
			if tinyMonster.image_rect.collidepoint(monster_hit):
				tinyMonster.hit = True

			if tinyMonster.hit == True:
				self.game_tiny_monster.remove(tinyMonster)

				#playsound('sfx/tapped.mp3')

				self.update_score_tiny()
				self.update_level()

		for medMonster in self.game_medium_monster.copy():
			if medMonster.image_rect.collidepoint(monster_hit):
				medMonster.hit = True

			if medMonster.hit == True:
				self.game_medium_monster.remove(medMonster)

				self.update_score_medium()
				self.update_level()

		for largeMonster in self.game_large_monster.copy():
			if largeMonster.image_rect.collidepoint(monster_hit):
				largeMonster.hit = True

			if largeMonster.hit == True:
				self.game_large_monster.remove(largeMonster)

				self.update_score_large()
				self.update_level()

		for innocent in self.game_innocent.copy():
			if innocent.image_rect.collidepoint(monster_hit):
				innocent.hit = True

			if innocent.hit == True:
				self.game_innocent.remove(innocent)

				self.update_score_innocent()

				self.game_settings.life -= 1

		for potion in self.game_potion.copy():
			if potion.image_rect.collidepoint(monster_hit):
				potion.hit = True

			if potion.hit == True:
				self.game_potion.remove(potion)

				self.potion_pressed_time = pygame.time.get_ticks()

				self.game_settings.bg_speed       = 0
				self.game_settings.monsters_speed = 0

		self.current_time                = pygame.time.get_ticks()

		print(f"current : {self.current_time} potion : {self.potion_pressed_time}")

		if self.current_time - self.potion_pressed_time >= 2000:
			self.game_settings.bg_speed       = 2
			self.game_settings.monsters_speed = 2

		'''
		if self.game_boss.image_rect.collidepoint(monster_hit):
			self.game_boss.hit = True
			self.boss_counter += 1

		if self.game_boss.hit == True:
			print(self.boss_counter)

			if self.boss_counter % 10 == 0:
				del self.game_boss
				self.stats.level += 1
				self.stats.score += 50
				self.score.show_level()
				self.score.show_score()
		'''


	#***********************#
	# ~~~ Tiny Monsters ~~~ #
	#***********************#

	def update_tiny_monsters(self):
		self.show_tinyMons_oneByOne()
		tiny_monsters = self.game_tiny_monster.sprites()
		
		for tinyMonster in tiny_monsters:
			tinyMonster.show_tinyMonster()
			#tinyMonster.update()

	def show_tinyMons_oneByOne(self):
		now = datetime.now()
		current_time = now - self.stats.start_time
		#print(current_time.seconds)
		if current_time.seconds > 1:
			if current_time.seconds % 2 == 0 and self.create_tiny_monster == False:
				self.create_tinyMons_oneByOne()
				#print('SUMMONED')
				self.create_tiny_monster = True

			elif current_time.seconds % 2 != 0 and self.create_tiny_monster == True:
				self.create_tiny_monster = False

	def create_tinyMons_oneByOne(self):
		tiny = TinyMonster(self)
		tiny.image_rect.x = randint(0, self.game_settings.screen_width - 70)
		self.game_tiny_monster.add(tiny)

	def tiny_mons_reset_pos(self):
		tiny = TinyMonster(self)
		tiny.image_rect.bottom = self.screen_rect.top

	#*************************#
	# ~~~ Medium Monsters ~~~ #
	#*************************#

	def update_medium_monsters(self):
		self.show_medMons_oneByOne()
		med_monsters = self.game_medium_monster.sprites()
		
		for medMonster in med_monsters:
			medMonster.show_mediumMonster()
			#tinyMonster.update()

	def show_medMons_oneByOne(self):
		now = datetime.now()
		current_time = now - self.stats.start_time
		#print(current_time.seconds)
		if current_time.seconds > 2:
			if current_time.seconds % 3 == 0 and self.create_medium_monster == False:
				self.create_medMons_oneByOne()
				#print('SUMMONED')
				self.create_medium_monster = True

			elif current_time.seconds % 3 != 0 and self.create_medium_monster == True:
				self.create_medium_monster = False

	def create_medMons_oneByOne(self):
		med = MediumMonster(self)
		med.image_rect.x = randint(0, self.game_settings.screen_width - 100)
		self.game_medium_monster.add(med)

	#************************#
	# ~~~ Large Monsters ~~~ #
	#************************#

	def update_large_monsters(self):
		self.show_largeMons_oneByOne()
		large_monsters = self.game_large_monster.sprites()
		
		for largeMonster in large_monsters:
			largeMonster.show_largeMonster()
			#tinyMonster.update()

	def show_largeMons_oneByOne(self):
		now = datetime.now()
		current_time = now - self.stats.start_time
		#print(current_time.seconds)
		if current_time.seconds > 4:
			if current_time.seconds % 5 == 0 and self.create_large_monster == False:
				self.create_largeMons_oneByOne()
				#print('SUMMONED')
				self.create_large_monster = True

			elif current_time.seconds % 5 != 0 and self.create_large_monster == True:
				self.create_large_monster = False

	def create_largeMons_oneByOne(self):
		large = LargeMonster(self)
		large.image_rect.x = randint(0, self.game_settings.screen_width - 130)
		self.game_large_monster.add(large)

	#******************#
	# ~~~ INNOCENT ~~~ #
	#******************#

	def update_innocent(self):
		self.show_innocent_oneByOne()
		innocents = self.game_innocent.sprites()
		
		for innocent in innocents:
			innocent.show_innocent()
			#tinyMonster.update()

	def show_innocent_oneByOne(self):
		now = datetime.now()
		current_time = now - self.stats.start_time
		#print(current_time.seconds)
		if current_time.seconds > 9:
			if current_time.seconds % 10 == 0 and self.create_innocent == False:
				self.create_innocent_oneByOne()
				#print('SUMMONED')
				self.create_innocent = True

			elif current_time.seconds % 10 != 0 and self.create_innocent == True:
				self.create_innocent = False

	def create_innocent_oneByOne(self):
		innocent = Innocent(self)
		innocent.image_rect.x = randint(0, self.game_settings.screen_width - 130)
		self.game_innocent.add(innocent)

	#****************#
	# ~~~ POTION ~~~ #
	#****************#

	def update_potion(self):
		self.show_potion_oneByOne()
		potions = self.game_potion.sprites()
		
		for potion in potions:
			potion.show_potion()

	def show_potion_oneByOne(self):
		now = datetime.now()
		current_time = now - self.stats.start_time
		#print(self.current_time.seconds)
		if current_time.seconds > 14:

			if current_time.seconds % 15 == 0 and self.create_potion == False:
				self.create_potion_oneByOne()
				self.create_potion = True

			elif current_time.seconds % 15 != 0 and self.create_potion == True:
				self.create_potion = False

	def create_potion_oneByOne(self):
		potion = Potion(self)
		potion.image_rect.x = randint(0, self.game_settings.screen_width-50)
		self.game_potion.add(potion)

	#**************#
	# ~~~ BOSS ~~~ #
	#**************#

	def update_boss(self):
		self.game_boss.show_boss()
		self.game_boss.update()

	#*************************#
	# ~~~ SCORE AND LEVEL ~~~ #
	#*************************#

	def update_score_tiny(self):
		self.stats.score += 15
		self.score.show_score()
		self.score.check_high_score()

		self.stats.saveData()

	def update_score_medium(self):
		self.stats.score += 10
		self.score.show_score()
		self.score.check_high_score()

		self.stats.saveData()
		
	def update_score_large(self):
		self.stats.score += 5
		self.score.show_score()
		self.score.check_high_score()

		self.stats.saveData()	

	def update_score_innocent(self):
		self.stats.score -= 10
		self.score.show_score()
		self.score.check_high_score()

		self.stats.saveData()	

	def update_level(self):
		self.counter += 1

		if self.counter % 10 == 0 :
			self.stats.level += 1
			self.score.show_level()

	def beyond_the_screen_check(self):
		for tinyMonster in self.game_tiny_monster.copy():
			if tinyMonster.image_rect.top >= 713:
				#print(self.game_settings.life)
				self.stats.score -= 5

				self.score.show_score()
				self.score.check_high_score()

				self.game_tiny_monster.remove(tinyMonster)
				self.game_settings.life -= 1

		for mediumMonster in self.game_medium_monster.copy():
			if mediumMonster.image_rect.top >= 713:
				#print(self.game_settings.life)
				self.stats.score -= 10

				self.score.show_score()
				self.score.check_high_score()

				self.game_medium_monster.remove(mediumMonster)
				self.game_settings.life -= 1

		for largeMonster in self.game_large_monster.copy():
			if largeMonster.image_rect.top >= 713:
				#print(self.game_settings.life)
				self.stats.score -= 15

				self.score.show_score()
				self.score.check_high_score()

				self.game_large_monster.remove(largeMonster)
				self.game_settings.life -= 1

		for innocent in self.game_innocent.copy():
			if innocent.image_rect.top >= 713:
				#print(self.game_settings.life)
				self.stats.score += 15

				self.score.show_score()
				self.score.check_high_score()

				self.game_innocent.remove(innocent)
				self.game_settings.life += 1

if __name__ == "__main__": #expression (True / False)
	theGame = Game()       #assignment
	theGame.run_game()