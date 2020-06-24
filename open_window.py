"""
Platformer Game
"""
import arcade
import constants
import player
import os
import enemy


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


class MenuView(arcade.View):
    """
    Menu class
    """
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Welcome!", 240, 400, arcade.color.BLACK, 54)
        arcade.draw_text("Click to start the game", 310, 300, arcade.color.BLACK, 24)

    def on_mouse_press(self, x, y, button, key_modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


def assign_new_high_score(score):
    f = open("highscore.txt", "w")
    f.write('%d' % score)
    arcade.draw_text(f"New highscore: {score}",
                     constants.SCREEN_WIDTH/2,
                     200,
                     arcade.color.GRAY,
                     font_size=15,
                     anchor_x="center")


def calculate_high_score(score):
    file_score = open("highscore.txt", "r").read()

    if len(file_score.strip()) != 0 :
        highest_score = int(file_score.strip())
        if highest_score > score :
            arcade.draw_text(f"High score: {highest_score}",
                             constants.SCREEN_WIDTH / 2,
                             200,
                             arcade.color.GRAY,
                             font_size=15,
                             anchor_x="center")
            arcade.draw_text(f"Your score: {score}",
                             constants.SCREEN_WIDTH / 2,
                             180,
                             arcade.color.GRAY,
                             font_size=15,
                             anchor_x="center")
        else:
            assign_new_high_score(score)
    else:
        assign_new_high_score(score)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.score = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)
        calculate_high_score(self.score)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.gold_coin_list = None
        self.bronze_coin_list = None
        self.wall_list = None
        self.player_list = None
        self.enemy_list = None
        self.level_jewel_list = None
        self.background_list = None
        self.ladders_list = None
        self.do_not_touch_list = None
        self.exit_sign_list = None
        self.enemy_list = None

        # Separate variable that holds the player sprite
        self.player = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0
        self.lives = 3

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")
        self.jump_sound = arcade.load_sound("sounds/jump1.wav")
        self.game_over = arcade.load_sound("sounds/gameover1.wav")

        # Level
        self.level = 1

        self.setup(self.level)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        if level == 1:
            self.score = 0
            self.lives = 3

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.gold_coin_list = arcade.SpriteList()
        self.bronze_coin_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.level_jewel_list = arcade.SpriteList()
        self.ladders_list = arcade.SpriteList()
        self.do_not_touch_list = arcade.SpriteList()
        self.exit_sign_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        self.player = player.PlayerCharacter()
        self.player.center_x = constants.PLAYER_START_X
        self.player.center_y = constants.PLAYER_START_Y
        self.player_list.append(self.player)

        if level == 3:
            self.player.center_y = 128 * constants.TILE_SCALING * 8

        # --- Load in a map from the tiled editor ---

        # Name of map file to load
        map_name = f"maps/level_{level}.tmx"
        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer that has items for pick-up
        gold_coins_layer_name = 'GoldCoins'
        bronze_coins_layer_name = "BronzeCoins"
        jewels_layer_name = "LevelJewel"
        ladders_layer_name = "Ladders"
        # Name of the layers that have objects or monsters that kills us
        do_not_touch_layer_name = "Obstacles"
        # Name of the layer that finishes a level
        finish_layer_name = "ExitSign"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        self.enemy_list = arcade.SpriteList()
        enemy_layer_name = "Enemies"

        e_list = arcade.tilemap.process_layer(my_map, enemy_layer_name, constants.ENEMY_SCALING)
        for e in e_list:
            my_enemy = enemy.Enemy()

            my_enemy.center_y = e.center_y + 307
            my_enemy.center_x = e.center_x + 1000
            my_enemy.change_x = -constants.PLAYER_MOVEMENT_SPEED
            self.enemy_list.append(my_enemy)
        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=constants.TILE_SCALING)

        # -- Collectibles
        self.gold_coin_list = arcade.tilemap.process_layer(my_map, gold_coins_layer_name, constants.TILE_SCALING)
        self.bronze_coin_list = arcade.tilemap.process_layer(my_map, bronze_coins_layer_name, constants.TILE_SCALING)
        self.level_jewel_list = arcade.tilemap.process_layer(my_map, jewels_layer_name, constants.TILE_SCALING)
        self.ladders_list = arcade.tilemap.process_layer(my_map, ladders_layer_name, constants.TILE_SCALING)
        self.do_not_touch_list = arcade.tilemap.process_layer(my_map, do_not_touch_layer_name, constants.TILE_SCALING)

        # --- Other stuff
        self.background_list = arcade.tilemap.process_layer(my_map, "Background", constants.TILE_SCALING)
        self.exit_sign_list = arcade.tilemap.process_layer(my_map, finish_layer_name, constants.TILE_SCALING)
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.wall_list,
                                                             constants.GRAVITY,
                                                             self.ladders_list)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.background_list.draw()
        self.level_jewel_list.draw()
        self.wall_list.draw()
        self.gold_coin_list.draw()
        self.ladders_list.draw()
        self.player_list.draw()
        self.bronze_coin_list.draw()
        self.do_not_touch_list.draw()
        self.exit_sign_list.draw()
        self.enemy_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.GOLD, 18)

        lives_text = f"Lives: {self.lives}"
        arcade.draw_text(lives_text, 10 + self.view_left, 30 + self.view_bottom,
                         arcade.csscolor.RED, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = constants.PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump():
                self.player.change_y = constants.PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = constants.PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0

    def on_update(self, delta_time: float = 1/10):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.physics_engine.update()
        self.player_list.update()
        self.player_list.update_animation(delta_time)
        self.enemy_list.update()
        self.enemy_list.update_animation(delta_time)

        # See if we hit any coins
        gold_coin_hit_list = arcade.check_for_collision_with_list(self.player,
                                                                  self.gold_coin_list)

        bronze_coin_hit_list = arcade.check_for_collision_with_list(self.player,
                                                                    self.bronze_coin_list)

        jewel_hit_list = arcade.check_for_collision_with_list(self.player,
                                                              self.level_jewel_list)

        zombie_hit_list = arcade.check_for_collision_with_list(self.player,
                                                               self.enemy_list)

        # Track if we need to change the viewport
        changed = False

        for zombie in zombie_hit_list:
            self.player.change_x = 0
            self.player.change_y = 0
            self.player.center_y = 128 * constants.TILE_SCALING * 8
            self.player.center_x = constants.PLAYER_START_X

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed = True
            self.lives -= 1
            if 300 < self.score:
                self.score -= 300
            elif 100 < self.score < 150:
                self.score -= 100
            elif 50 < self.score < 100:
                self.score -= 50
            elif 25 < self.score < 50:
                self.score -= 25
            arcade.play_sound(self.game_over)

        # Loop through each coin we hit (if any) and remove it
        for coin in gold_coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add 10 to the score
            self.score += 10

        for coin in bronze_coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 1

        for jewel in jewel_hit_list:
            # Remove the jewel
            jewel.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add 100 to score
            self.score += 100

        # Did the player fall off the map?
        if self.player.center_y < -100:
            self.lives -= 1
            if self.level == 3:
                self.player.center_y = 128 * constants.TILE_SCALING * 8
            else:
                self.player.center_y = constants.PLAYER_START_Y

            self.player.center_x = constants.PLAYER_START_X

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed = True
            arcade.play_sound(self.game_over)

        if arcade.check_for_collision_with_list(self.player, self.do_not_touch_list):
            self.player.change_x = 0
            self.player.change_y = 0

            if self.level == 3:
                self.player.center_y = 128 * constants.TILE_SCALING * 8
            else:
                self.player.center_y = constants.PLAYER_START_Y

            self.player.center_x = constants.PLAYER_START_X

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed = True
            self.lives -= 1
            arcade.play_sound(self.game_over)

        if self.level == 3:
            if arcade.check_for_collision_with_list(self.player, self.exit_sign_list):
                self.level = 1
                self.setup(self.level)
        else:
            if arcade.check_for_collision_with_list(self.player, self.exit_sign_list):
                self.level += 1
                # Set the camera to the start
                self.view_left = 0
                self.view_bottom = 0
                changed = True
                # Load the next level
                self.setup(self.level)

        # --- Manage Scrolling ---
        # Scroll left
        left_boundary = self.view_left + constants.LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + constants.SCREEN_WIDTH - constants.RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + constants.SCREEN_HEIGHT - constants.TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + constants.BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                constants.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                constants.SCREEN_HEIGHT + self.view_bottom)

        if self.lives == 0:
            game_over_view = GameOverView()
            game_over_view.score = self.score
            self.window.show_view(game_over_view)


def main():
    """ Main method """
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
