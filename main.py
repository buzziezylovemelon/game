from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from random import shuffle
import time

class MatchingGameApp(App):
    def build(self):
        Window.size = (1280, 720)
        Window.top, Window.left = 50, 150
        self.root = RelativeLayout()
        self.load_sounds()
        self.create_main_menu()
        return self.root

    def load_sounds(self):
        """Load the sound for card clicks."""
        self.click_sound = SoundLoader.load('sound/test.mp3')
        if self.click_sound:
            self.click_sound.volume = 1.0
        else:
            print("Failed to load sound. Check the file path.")

    def set_background(self, image_path):
        """Set the background image for the screen."""
        background = Image(source=image_path, allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.root.add_widget(background)

    def create_main_menu(self):
        """Create the main menu layout."""
        self.root.clear_widgets()
        self.set_background('images/bnk123.png')

        menu_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        play_button = Button(
            background_normal='images/play1.png',
            background_down='images/play2.png',
            size_hint=(None, None),
            size=(816, 79),
            pos_hint={'center_x': 0.5},
            on_press=self.show_mode_selection
        )
        play_button.bind(on_state=self.on_play_button_state)

        menu_layout.add_widget(BoxLayout(size_hint=(1, 0.5)))  # Spacer
        menu_layout.add_widget(play_button)
        menu_layout.add_widget(BoxLayout(size_hint=(1, 0.4)))  # Spacer

        self.root.add_widget(menu_layout)

    def on_play_button_state(self, button, state):
        """Change button image on hover or press."""
        button.background_normal = 'images/play2.png' if state == 'down' else 'images/play1.png'

    def show_mode_selection(self, instance):
        """Display the mode selection screen."""
        self.root.clear_widgets()
        self.set_background('images/bnnn.png')

        layout = RelativeLayout()

        back_button = Button(
            background_normal='images/leftblack.png',
            size_hint=(None, None),
            size=(223.2, 72),
            pos_hint={'x': 0.05, 'y': 0.85},
            on_press=lambda x: self.create_main_menu()
        )
        layout.add_widget(back_button)

        modes = [
            ('easy', 'images/easy1.png', 'images/easy2.png', 4, 4, 0.45),
            ('normal', 'images/normal1.png', 'images/normal2.png', 5, 4, 0.35),
            ('hard', 'images/hard1.png', 'images/hard2.png', 6, 5, 0.25)
        ]

        for mode, img_normal, img_down, rows, cols, pos_y in modes:
            button = Button(
                background_normal=img_normal,
                background_down=img_down,
                size_hint=(None, None),
                size=(816, 79),
                pos_hint={'center_x': 0.5, 'y': pos_y},
                on_press=lambda x, r=rows, c=cols, m=mode: self.start_game(r, c, m)
            )
            layout.add_widget(button)

        self.root.add_widget(layout)

    def start_game(self, rows, cols, mode):
        """Initialize the game board."""
        self.root.clear_widgets()
        self.set_background('images/bnk11.png')

        self.score, self.moves, self.mistakes = 0, 0, 0
        self.first_card, self.second_card = None, None
        self.waiting = False
        self.start_time = time.time()

        images = self.get_images_by_mode(mode)
        shuffle(images)

        top_bar = RelativeLayout(size_hint_y=None, height=100)
        back_button = Button(
            background_normal='images/leftblack.png',
            size_hint=(None, None),
            size=(223.2, 72),
            pos_hint={'x': 0.05, 'y': 7.65},
            on_press=lambda x: self.show_mode_selection(None)
        )
        top_bar.add_widget(back_button)
        self.root.add_widget(top_bar)

        grid = GridLayout(cols=cols, spacing=10, padding=10, size_hint=(None, None))
        grid.width = cols * 148 + (cols - 1) * 10
        grid.height = rows * 132 + (rows - 1) * 10
        grid.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.cards = []
        for image in images:
            card = Button(
                background_normal='images/heatt.png',
                size_hint=(None, None),
                size=(148, 132)
            )
            card.image, card.revealed = image, False
            card.bind(on_press=self.on_card_click)
            self.cards.append(card)
            grid.add_widget(card)

        self.root.add_widget(grid)

    def get_images_by_mode(self, mode):
        """Return a list of images based on the selected difficulty."""
        image_sets = {
            'easy': ['images/ea1.png', 'images/ea2.png', 'images/ea3.png', 'images/ea4.png',
                     'images/ea5.png', 'images/ea6.png', 'images/ea7.png', 'images/ea8.png'],
            'normal': ['images/no1.png', 'images/no2.png', 'images/no3.png', 'images/no4.png',
                       'images/no5.png', 'images/no6.png', 'images/no7.png', 'images/no8.png',
                       'images/no9.png', 'images/no10.png'],
            'hard': ['images/ha1.png', 'images/ha2.png', 'images/ha3.png', 'images/ha4.png',
                     'images/ha5.png', 'images/ha6.png', 'images/ha7.png', 'images/ha8.png',
                     'images/ha9.png', 'images/ha10.png', 'images/ha11.png', 'images/ha12.png',
                     'images/ha13.png', 'images/ha14.png', 'images/ha15.png']
        }
        return image_sets[mode] * 2

    def on_card_click(self, card):
        """Handle card click events."""
        if self.waiting or card.revealed:
            return

        if self.click_sound:
            self.click_sound.play()

        card.background_normal = card.image
        card.revealed = True

        if not self.first_card:
            self.first_card = card
        elif not self.second_card:
            self.second_card = card
            self.moves += 1
            self.check_match()

    def check_match(self):
        """Check if two selected cards match."""
        if self.first_card.image == self.second_card.image:
            self.first_card, self.second_card = None, None
            self.score += 1
            if self.score == len(self.cards) // 2:
                self.waiting = True
                Clock.schedule_once(self.show_win_screen, 3)
        else:
            self.waiting = True
            Clock.schedule_once(self.hide_cards, 1)

    def hide_cards(self, dt):
        """Hide unmatched cards after a delay."""
        self.first_card.background_normal = 'images/heatt.png'
        self.second_card.background_normal = 'images/heatt.png'
        self.first_card.revealed = False
        self.second_card.revealed = False
        self.first_card, self.second_card = None, None
        self.waiting = False

    def show_win_screen(self, dt):
        """Display the win screen."""
        self.root.clear_widgets()
        self.set_background('images/youwinn.png')

        layout = BoxLayout(orientation='vertical', padding=[50, 50, 50, 50], spacing=20, size_hint=(None, None), size=(900, 400), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        back_button = Button(
            background_normal='images/back_black.png',
            size_hint=(None, None),
            size=(816, 80),
            pos_hint={'center_x': 0.5},
            on_press=lambda x: self.create_main_menu()
        )
        layout.add_widget(back_button)
        self.root.add_widget(layout)

if __name__ == '__main__':
    MatchingGameApp().run()
