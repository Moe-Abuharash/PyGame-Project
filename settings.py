class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's Static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # Ship settings
# We set the initial value of ship_speed to 1.5. When the ship moves
# now, its position is adjusted by 1.5 pixels rather than 1 pixel on each pass
# through the loop.
# We’re using decimal values for the speed setting to give us finer control of the ship’s speed when we increase the tempo of the game later on.
# However, rect attributes such as x store only integer values, so we need to
# make some modifications to Ship:
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
# These settings create dark gray bullets with a width of 3 pixels and a
# height of 15 pixels. The bullets will travel slightly slower than the ship.
        self.bullets_allowed = 3
# This limits the player to three bullets at a time. We’ll use this setting in
# AlienInvasion to check how many bullets exist before creating a new bullet
# in _fire_bullet()

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        # how quickly the game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # The setting fleet_drop_speed controls how quickly the fleet drops down
        # the screen each time an alien reaches either edge. It’s helpful to separate
        # this speed from the aliens’ horizontal speed so you can adjust the two
        # speeds independently.
        # To implement the setting fleet_direction, we could use a text value, such
        # as 'left' or 'right', but we’d end up with if-elif statements testing for the
        # fleet direction. Instead, because we have only two directions to deal with,
        # let’s use the values 1 and −1, and switch between them each time the fleet
        # changes direction. (Using numbers also makes sense because moving right
        # involves adding to each alien’s x-coordinate value, and moving left involves
        # subtracting from each alien’s x-coordinate value.)

    def initialize_dynamic_settings(self):
        """Iinitializae settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction of 1 representations right; -1 represents left.
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)
