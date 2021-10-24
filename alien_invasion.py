import sys
from time import sleep
# We first import the sys and pygame modules. The pygame module contains the functionality
# needed to make a game, and use tools in the sys module to exit the game when the player quits

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    # Alien invasion starts with a class called AlienInvasion. In the __init__() method, the pygame.init()
    # function initalizes the background settings that pygame needs to work properly.

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
# When creating the screen surface, we pass a size of (0, 0) and the
# parameter pygame.FULLSCREEN u. This tells Pygame to figure out a window size
# that will fill the screen. Because we don’t know the width and height of the
# screen ahead of time, we update these settings after the screen is created v.
# We use the width and height attributes of the screen’s rect to update the
# settings object.

        # Here, we call the pygame.display.set_mode() to create a display window, on which we'll draw all the game's
        # graphical elements. The argument (1200,800) is a tuple that defines the dimensions of the game window,
        # which will be 1200 pixels wide by 800 pixels high. We assign this display window to the attribute self.screen,
        # so it will be available in all methods in the class.
        # self.screen = pygame.display.set_mode(
        #    (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        # Now that we have a Bullet class and the necessary settings defined, we can
        # write code to fire a bullet each time the player presses the spacebar. We’ll
        # create a group in AlienInvasion to store all the live bullets so we can manage the bullets that have already been fired. This group will be an instance
        # of the pygame.sprite.Group class, which behaves like a list with some extra
        # functionality that’s helpful when building games. We’ll use this group
        # to draw bullets to the screen on each pass through the main loop and to
        # update each bullet’s position.
        # We’ll create the group in __init__():
        # Then we need to update the position of the bullets on each pass
        # through the while loop
        self.bullets = pygame.sprite.Group()
        # We import Settings into the main program file. Then we create an
        # instance of Settings and assign it to self.settings u, after making the call
        # to pygame.init(). When we create a screen v, we use the screen_width and
        # screen_height attributes of self.settings, and then we use self.settings to
        # access the background color when filling the screen at w as well.
        # When you run alien_invasion.py now you won’t yet see any changes,
        # because all we’ve done is move the settings we were already using elsewhere.
        # Now we’re ready to start adding new elements to the screen

  #  We’ll move the code that manages events to a separate method called
  # _check_events(). This will simplify run_game() and isolate the event management loop. Isolating the event loop allows you to manage events separately
  # from other aspects of the game, such as updating the screen.
  # Here’s the AlienInvasion class with the new _check_events() method,
  # which only affects the code in run_game():
  # We make a new _check_events() method v and move the lines that check
  # whether the player has clicked to close the window into this new method.
  # To call a method from within a class, use dot notation with the variable
  # self and the name of the method u. We call the method from inside the
  # while loop in run_game()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")
        self.game_active = True

# We want to create an instance of Alien so we can see the first alien on
# the screen. Because it’s part of our setup work, we’ll add the code for this
# instance at the end of the __init__() method in AlienInvasion. Eventually,
# we’ll create an entire fleet of aliens, which will be quite a bit of work,
# so we’ll make a new helper method called _create_fleet().
# The order of methods in a class doesn’t matter, as long as there’s some
# consistency to how they’re placed. I’ll place _create_fleet() just before the
# _update_screen() method, but anywhere in AlienInvasion will work. First, we’ll
# import the Alien class.
# In this method, we’re creating one instance of Alien, and then adding it
# to the group that will hold the fleet. The alien will be placed in the default
# upper-left area of the screen, which is perfect for the first alien.

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # We’ve already thought through most of this code. We need to know the
        # alien’s width and height to place aliens, so we create an alien at u before
        # we perform calculations. This alien won’t be part of the fleet, so don’t add
        # it to the group aliens. At v we get the alien’s width from its rect attribute
        # and store this value in alien_width so we don’t have to keep working through
        # the rect attribute. At w we calculate the horizontal space available for aliens
        # and the number of aliens that can fit into that space.
        # Next, we set up a loop that counts from 0 to the number of aliens we
        # need to make x. In the main body of the loop, we create a new alien and
        # then set its x-coordinate value to place it in the row y. Each alien is pushed
        # to the right one alien width from the left margin. Next, we multiply the
        # alien width by 2 to account for the space each alien takes up, including the
        # empty space to its right, and we multiply this amount by the alien’s position
        # in the row. We use the alien’s x attribute to set the position of its rect. Then
        # we add each new alien to the group aliens.

        # Create the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # create an alien and place it in the row.
        # self._create_alien(alien_number)
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
# We need the width and height of an alien, so at u we use the attribute
# size, which contains a tuple with the width and height of a rect object. To
# calculate the number of rows we can fit on the screen, we write our available
# _space_y calculation right after the calculation for available_space_x v. The
# calculation is wrapped in parentheses so the outcome can be split over two
# lines, which results in lines of 79 characters or less, as is recommended.
# To create multiple rows, we use two nested loops: one outer and one
# inner loop w. The inner loop creates the aliens in one row. The outer loop
# counts from 0 to the number of rows we want; Python uses the code for
# making a single row and repeats it number_rows times.
# To nest the loops, write the new for loop and indent the code you want
# to repeat. (Most text editors make it easy to indent and unindent blocks of
# code, but for help see Appendix B.) Now when we call _create_alien(), we
# include an argument for the row number so each row can be placed farther
# down the screen.
# The definition of _create_alien() needs a parameter to hold the row
# number. Within _create_alien(), we change an alien’s y-coordinate value
# when it’s not in the first row x by starting with one alien’s height to create
# empty space at the top of the screen. Each row starts two alien heights below
# the previous row, so we multiply the alien height by two and then by the row
# number. The first row number is 0, so the vertical placement of the first row
# is unchanged. All subsequent rows are placed farther down the screen.

    def _check_fleet_edges(self):
        """Respond appropriatley if any aliens have reahced an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

# In _check_fleet_edges(), we loop through the fleet and call check_edges()
# on each alien u. If check_edges() returns True, we know an alien is at an
# edge and the whole fleet needs to change direction; so we call _change_fleet
# _direction() and break out of the loop v. In _change_fleet_direction(), we
# loop through all the aliens and drop each one using the setting fleet_drop
# _speed w; then we change the value of fleet_direction by multiplying its current value by −1. The line that changes the fleet’s direction isn’t part of the
# for loop. We want to change each alien’s vertical position, but we only want
# to change the direction of the fleet once.

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_aliens()


# When you call update() on a group u, the group automatically calls
# update() for each sprite in the group. The line self.bullets.update() calls
# bullet.update() for each bullet we place in the group bullets

        # get rid of bullets that have disapperead.
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

# When you use a for loop with a list (or a group in Pygame), Python
# expects that the list will stay the same length as long as the loop is running. Because we can’t remove items from a list or group within a for loop,
# we have to loop over a copy of the group. We use the copy() method to set
# up the for loop u, which enables us to modify bullets inside the loop. We
# check each bullet to see whether it has disappeared off the top of the screen
# at v. If it has, we remove it from bullets w. At x we insert a print() call to
# show how many bullets currently exist in the game and verify that they’re
# being deleted when they reach the top of the screen.
# If this code works correctly, we can watch the terminal output while firing bullets and see that the number of bullets decreases to zero after each
# series of bullets has cleared the top of the screen. After you run the game
# and verify that bullets are being deleted properly, remove the print() call. If
# you leave it in, the game will slow down significantly because it takes more
# time to write output to the terminal than it does to draw graphics to the
# game window.


# The ship’s position will be updated after we’ve checked for keyboard
# events and before we update the screen. This allows the ship’s position to be
# updated in response to player input and ensures the updated position will
# be used when drawing the ship to the screen.
# When you run alien_invasion.py and hold down the right arrow key, the
# ship should move continuously to the right until you release the key
            self._update_screen()


# Whenever the player presses a key, that keypress is registered in Pygame as
# an event. Each event is picked up by the pygame.event.get() method. We need
# to specify in our _check_events() method what kind of events we want the
# game to check for. Each keypress is registered as a KEYDOWN event.
# When Pygame detects a KEYDOWN event, we need to check whether the
# key that was pressed is one that triggers a certain action. For example, if the
# player presses the right arrow key, we want to increase the ship’s rect.x value
# to move the ship to the right:
# Inside _check_events() we add an elif block to the event loop to respond
# when Pygame detects a KEYDOWN event u. We check whether the key pressed,
# event.key, is the right arrow key v. The right arrow key is represented by
# pygame.K_RIGHT. If the right arrow key was pressed, we move the ship to the
# right by increasing the value of self.ship.rect.x by 1 w.
# When you run alien_invasion.py now, the ship should move to the right
# one pixel every time you press the right arrow key. That’s a start, but it’s not
# an efficient way to control the ship. Let’s improve this control by allowing
# continuous movement.

    def _ship_hit(self):
        # respond to the ship being hit by an alien.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # looks for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        "Check if aliens hit bottom"
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if if the ship got hit.
                self._ship_hit()
                break

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                '''if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True'''

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                '''if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False'''

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start new game when player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
# In _check_keydown_events(), we add a new block that ends the game when
# the player presses Q. Now, when testing, you can press Q to close the game
# rather than using your cursor to close the window.


# We make two new helper methods: _check_keydown_events() and _check
# _keyup_events(). Each needs a self parameter and an event parameter. The
# bodies of these two methods are copied from _check_events(), and we’ve
# replaced the old code with calls to the new methods. The _check_events()
# method is simpler now with this cleaner code structure, which will make it
# easier to develop further responses to player input.


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


# If a KEYDOWN event occurs for the K_LEFT key, we set moving_left to True. If a
# KEYUP event occurs for the K_LEFT key, we set moving_left to False. We can use
# elif blocks here because each event is connected to only one key. If the player
# presses both keys at once, two separate events will be detected.
# When you run alien_invasion.py now, you should be able to move the ship
# continuously to the right and left. If you hold down both keys, the ship should
# stop moving.
# Next, we’ll further refine the ship’s movement. Let’s adjust the ship’s
# speed and limit how far the ship can move so it can’t disappear off the sides
# of the screen.


# At u, we modify how the game responds when the player presses the
# right arrow key: instead of changing the ship’s position directly, we merely
# set moving_right to True. At v, we add a new elif block, which responds to
# KEYUP events. When the player releases the right arrow key (K_RIGHT), we set
# moving_right to False.
# Next, we modify the while loop in run_game() so it calls the ship’s update()
# method on each pass through the loop:

            # Move the ship to the right.
            self.ship.rect.x += 1

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            # When the player presses the spacebar, we check the length of bullets.
            # If len(self.bullets) is less than three, we create a new bullet. But if three
            # bullets are already active, nothing happens when the spacebar is pressed.
            # When you run the game now, you should be able to fire bullets only in
            # groups of three.

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # destroy exisiting bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # When you call draw() on a group, Pygame draws each element in the
        # group at the position defined by its rect attribute. The draw() method
        # requires one argument: a surface on which to draw the elements from the
        # group.
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()

        # First, we import Bullet u. Then we call _fire_bullet() when the spacebar is pressed v. In _fire_bullet(), we make an instance of Bullet and call it
        # new_bullet w. We then add it to the group bullets using the add() method x.
        # The add() method is similar to append(), but it’s a method that’s written specifically for Pygame groups.
        # The bullets.sprites() method returns a list of all sprites in the group
        # bullets. To draw all fired bullets to the screen, we loop through the sprites
        # in bullets and call draw_bullet() on each one
        self.sb.show_score()

        # Make the most recently drawn screen visible.
        pygame.display.flip()
# Colors in Pygame are specified as RGB colors: a mix of red, green,
# and blue. Each color value can range from 0 to 255. The color value (255,
# 0, 0) is red, (0, 255, 0) is green, and (0, 0, 255) is blue. You can mix different RGB values to create up to 16 million colors. The color value (230, 230,
# 230) mixes equal amounts of red, blue, and green, which produces a light
# gray background color. We assign this color to self.bg_color u.
# At v, we fill the screen with the background color using the fill()
# method, which acts on a surface and takes only one argument: a color.

# We’ll position the ship at the bottom center of the screen. To do so,
# make the value of self.rect.midbottom match the midbottom attribute of the
# screen’s rect x. Pygame uses these rect attributes to position the ship
# image so it’s centered horizontally and aligned with the bottom of the
# screen.
# At y, we define the blitme() method, which draws the image to the
# screen at the position specified by self.rect.

# We import Ship and then make an instance of Ship after the screen
# has been created u. The call to Ship() requires one argument, an instance
# of AlienInvasion. The self argument here refers to the current instance of
# AlienInvasion. This is the parameter that gives Ship access to the game’s
# resources, such as the screen object. We assign this Ship instance to
# self.ship.
# After filling the background, we draw the ship on the screen by calling
# ship.blitme(), so the ship appears on top of the background.


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

# First, we import the sys and pygame modules. The pygame module contains the functionality we need to make a game. We’ll use tools in the sys
# module to exit the game when the player quits.
# Alien Invasion starts as a class called AlienInvasion. In the __init__()
# method, the pygame.init() function initializes the background settings that
# Pygame needs to work properly u. At v, we call pygame.display.set_mode() to
# create a display window, on which we’ll draw all the game’s graphical elements. The argument (1200, 800) is a tuple that defines the dimensions of
# the game window, which will be 1200 pixels wide by 800 pixels high. (You
# can adjust these values depending on your display size.) We assign this display window to the attribute self.screen, so it will be available in all methods
# in the class.
# The object we assigned to self.screen is called a surface. A surface in
# Pygame is a part of the screen where a game element can be displayed.
# Each element in the game, like an alien or a ship, is its own surface. The
# surface returned by display.set_mode() represents the entire game window.
# When we activate the game’s animation loop, this surface will be redrawn
# on every pass through the loop, so it can be updated with any changes triggered by user input.
# The game is controlled by the run_game() method. This method contains
# a while loop w that runs continually. The while loop contains an event loop
# and code that manages screen updates. An event is an action that the user
# performs while playing the game, such as pressing a key or moving the
# mouse. To make our program respond to events, we write this event loop to
# listen for events and perform appropriate tasks depending on the kinds of
# events that occur. The for loop at x is an event loop.
# To access the events that Pygame detects, we’ll use the pygame.event
# get() function. This function returns a list of events that have taken place
# since the last time this function was called. Any keyboard or mouse event
# will cause this for loop to run. Inside the loop, we’ll write a series of if
# statements to detect and respond to specific events. For example, when the
# player clicks the game window’s close button, a pygame.QUIT event is detected
# and we call sys.exit() to exit the game y.
# The call to pygame.display.flip() at z tells Pygame to make the most
# recently drawn screen visible. In this case, it simply draws an empty screen
# on each pass through the while loop, erasing the old screen so only the new
# screen is visible. When we move the game elements around, pygame.display
# .flip() continually updates the display to show the new positions of game
# elements and hides the old ones, creating the illusion of smooth movement.
# At the end of the file, we create an instance of the game, and then call
# run_game(). We place run_game() in an if block that only runs if the file is
# called directly. When you run this alien_invasion.py file, you should see an
# empty Pygame window.
