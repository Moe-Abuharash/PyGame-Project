import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

# When the player holds down the right arrow key, we want the ship to
# continue moving right until the player releases the key. We’ll have the
# game detect a pygame.KEYUP event so we’ll know when the right arrow key is
# released; then we’ll use the KEYDOWN and KEYUP events together with a flag
# called moving_right to implement continuous motion.
# When the moving_right flag is False, the ship will be motionless. When
# the player presses the right arrow key, we’ll set the flag to True, and when the
# player releases the key, we’ll set the flag to False again.
# The Ship class controls all attributes of the ship, so we’ll give it an attribute called moving_right and an update() method to check the status of the
# moving_right flag. The update() method will change the position of the ship if
# the flag is set to True. We’ll call this method once on each pass through the
# while loop to update the position of the ship.

        # Movement Flags
        self.moving_right = False
        self.moving_left = False

# In __init__(), we add a self.moving_left flag. In update(), we use two
# separate if blocks rather than an elif to allow the ship’s rect.x value to be
# increased and then decreased when both arrow keys are held down. This
# results in the ship standing still. If we used elif for motion to the left, the
# right arrow key would always have priority. Doing it this way makes the
# movements more accurate when switching from right to left when the player
# might momentarily hold down both keys.
    def update(self):
        """Update the ship's position based on the movement flag."""
        # update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

# This code checks the position of the ship before changing the value of
# self.x. The code self.rect.right returns the x-coordinate of the right edge
# of the ship’s rect. If this value is less than the value returned by self.screen
# _rect.right, the ship hasn’t reached the right edge of the screen u. The same
# goes for the left edge: if the value of the left side of the rect is greater than
# zero, the ship hasn’t reached the left edge of the screen v. This ensures the
# ship is within these bounds before adjusting the value of self.x.
# When you run alien_invasion.py now, the ship should stop moving at
# either edge of the screen. This is pretty cool; all we’ve done is add a conditional test in an if statement, but it feels like the ship hits a wall or a force
# field at either edge of the screen!


# We create a settings attribute for Ship, so we can use it in update() u.
# Because we’re adjusting the position of the ship by fractions of a pixel, we
# need to assign the position to a variable that can store a decimal value. You
# can use a decimal value to set an attribute of rect, but the rect will only
# keep the integer portion of that value. To keep track of the ship’s position
# accurately, we define a new self.x attribute that can hold decimal values v.
# We use the float() function to convert the value of self.rect.x to a decimal
# and assign this value to self.x.
# Now when we change the ship’s position in update(), the value of self.x
# is adjusted by the amount stored in settings.ship_speed w. After self.x has
# been updated, we use the new value to update self.rect.x, which controls
# the position of the ship x. Only the integer portion of self.x will be stored
# in self.rect.x, but that’s fine for displaying the ship.
# Now we can change the value of ship_speed, and any value greater than
# one will make the ship move faster. This will help make the ship respond
# quickly enough to shoot down aliens, and it will let us change the tempo of
# the game as the player progresses in gameplay.

        # update rect object from self.x
        self.rect.x = self.x

# We add a self.moving_right attribute in the __init__() method and set it
# to False initially u. Then we add update(), which moves the ship right if the
# flag is True v. The update() method will be called through an instance of
# Ship, so it’s not considered a helper method.
# Now we need to modify _check_events() so that moving_right is set to True
# when the right arrow key is pressed and False when the key is released:

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)


# We import the pygame module before defining the class. The __init__()
# method of Ship takes two parameters: the self reference and a reference to
# the current instance of the AlienInvasion class. This will give Ship access to
# all the game resources defined in AlienInvasion. At u we assign the screen
# to an attribute of Ship, so we can access it easily in all the methods in this
# class. At v we access the screen’s rect attribute using the get_rect() method
# and assign it to self.screen_rect. Doing so allows us to place the ship in the
# correct location on the screen.
# To load the image, we call pygame.image.load() w and give it the location of our ship image.
# This function returns a surface representing the
# ship, which we assign to self.image. When the image is loaded, we call
# get_rect() to access the ship surface’s rect attribute so we can later use it
# to place the ship.
# When you’re working with a rect object, you can use the x- and y-coordinates
# of the top, bottom, left, and right edges of the rectangle, as well as the
# center, to place the object. You can set any of these values to establish the
# current position of the rect. When you’re centering a game element, work
# with the center, centerx, or centery attributes of a rect. When you’re working
# at an edge of the screen, work with the top, bottom, left, or right attributes.
# There are also attributes that combine these properties, such as midbottom,
# midtop, midleft, and midright. When you’re adjusting the horizontal or vertical placement of
# the rect, you can just use the x and y attributes, which are
# the x- and y-coordinates of its top-left corner. These attributes spare you
# from having to do calculations that game developers formerly had to do
# manually, and you’ll use them often.


    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
