from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from random import shuffle
import time

class MatchingGameApp(App):
    def build(self):
        self.start_time = None
        self.root = RelativeLayout()  # ใช้ RelativeLayout เพื่อรองรับพื้นหลัง
        self.create_main_menu()
        return self.root

    def set_background(self, image_path):
        """ตั้งค่าพื้นหลังด้วยรูปภาพ"""
        background = Image(source=image_path, allow_stretch=True, keep_ratio=False)
        self.root.add_widget(background)

    def create_main_menu(self):
        self.root.clear_widgets()
        self.set_background('images/bnk123.png')  # พื้นหลังเฉพาะสำหรับหน้าแรก

        # Layout สำหรับ Widget ด้านหน้า
        front_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title label
        title = Label(text="", font_size=32, size_hint=(1, 0.2))

        # Container to center the play button
        play_button_container = BoxLayout(
            size_hint=(1, 1),
            orientation='vertical',
            padding=[0, 50, 0, 50]
        )

        # Play button with an image
        play_button = Button(
            background_normal='images/play.jpg',
            background_down='images/play_button_down.jpg',
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={'center_x': 0.5},
            on_press=self.show_mode_selection
        )

        play_button_container.add_widget(Label(size_hint=(1, 0.7)))
        play_button_container.add_widget(play_button)
        play_button_container.add_widget(Label(size_hint=(1, 0.3)))

        # Add widgets to the layout
        front_layout.add_widget(title)
        front_layout.add_widget(play_button_container)

        self.root.add_widget(front_layout)

    def show_mode_selection(self, instance):
        self.root.clear_widgets()
        self.set_background('images/bnk11.png')  # พื้นหลังสำหรับหน้าที่เหลือ

        front_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        back_button = Button(background_normal='images/left.jpg', size_hint=(None, None), size=(50, 50),
                              on_press=lambda x: self.create_main_menu())
        top_bar.add_widget(back_button)

        title = Label(text="Select Difficulty", font_size=24, size_hint=(1, 0.2))
        easy_button = Button(text="Easy", size_hint=(0.5, None), height=50, pos_hint={'center_x': 0.5})
        normal_button = Button(text="Normal", size_hint=(0.5, None), height=50, pos_hint={'center_x': 0.5})
        hard_button = Button(text="Hard", size_hint=(0.5, None), height=50, pos_hint={'center_x': 0.5})

        # Bind actions to buttons
        easy_button.bind(on_press=lambda x: self.start_game(4, 4, 'easy'))
        normal_button.bind(on_press=lambda x: self.start_game(5, 4, 'normal'))
        hard_button.bind(on_press=lambda x: self.start_game(6, 5, 'hard'))

        front_layout.add_widget(top_bar)
        front_layout.add_widget(title)
        front_layout.add_widget(easy_button)
        front_layout.add_widget(normal_button)
        front_layout.add_widget(hard_button)

        self.root.add_widget(front_layout)

    def start_game(self, rows, cols, mode):
        self.root.clear_widgets()
        self.set_background('images/bnk11.png')  # พื้นหลังสำหรับหน้าที่เหลือ

        self.score = 0
        self.moves = 0
        self.mistakes = 0
        self.first_card = None
        self.second_card = None
        self.waiting = False
        self.start_time = time.time()

        if mode == 'easy':
            images = [
                'images/cat1.jpg', 'images/cat4.jpg', 'images/cat7.jpg',
                'images/cat2.jpg', 'images/cat5.jpg', 'images/cat8.jpg',
                'images/cat3.jpg', 'images/cat6.jpg'
            ]
        elif mode == 'normal':
            images = [
                'images/meme1.jpg', 'images/meme5.jpg', 'images/meme8.jpg',
                'images/meme2.jpg', 'images/meme6.jpg', 'images/meme9.jpg',
                'images/meme3.jpg', 'images/meme7.jpg', 'images/meme10.jpg',
                'images/meme4.jpg'
            ]
        elif mode == 'hard':
            images = [
                'images/lfc1.jpg', 'images/lfc6.jpg', 'images/lfc11.jpg',
                'images/lfc2.jpg', 'images/lfc7.jpg', 'images/lfc12.jpg',
                'images/lfc3.jpg', 'images/lfc8.jpg', 'images/lfc13.jpg',
                'images/lfc4.jpg', 'images/lfc9.jpg', 'images/lfc14.jpg',
                'images/lfc5.jpg', 'images/lfc10.jpg', 'images/lfc15.jpg'
            ]

        images = images[:(rows * cols) // 2] * 2
        shuffle(images)

        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        back_button = Button(background_normal='images/left.jpg', size_hint=(None, None), size=(50, 50),
                              on_press=lambda x: self.show_mode_selection(None))
        top_bar.add_widget(back_button)
        self.info_label = Label(text=f"Moves: {self.moves} | Mistakes: {self.mistakes}", font_size=20)
        top_bar.add_widget(self.info_label)

        grid = GridLayout(cols=cols, spacing=10, padding=10)
        self.cards = []

        for image in images:
            card = Button(background_normal='', background_color=(1, 1, 1, 1))
            card.image = image
            card.revealed = False
            card.bind(on_press=self.on_card_click)
            self.cards.append(card)
            grid.add_widget(card)

        self.root.add_widget(top_bar)
        self.root.add_widget(grid)

    def on_card_click(self, card):
        if self.waiting or card.revealed:
            return

        card.background_normal = card.image
        card.revealed = True

        if not self.first_card:
            self.first_card = card
        elif not self.second_card:
            self.second_card = card
            self.moves += 1
            self.update_info()
            self.check_match()

    def check_match(self):
        if self.first_card.image == self.second_card.image:
            self.first_card = None
            self.second_card = None
            self.score += 1
            if self.score == len(self.cards) // 2:
                self.waiting = True
                Clock.schedule_once(self.delayed_show_win_screen, 3)  # Add a 3-second delay
        else:
            self.mistakes += 1
            self.update_info()
            self.waiting = True
            Clock.schedule_once(self.hide_cards, 1)

    def hide_cards(self, dt):
        self.first_card.background_normal = ''
        self.second_card.background_normal = ''
        self.first_card.revealed = False
        self.second_card.revealed = False
        self.first_card = None
        self.second_card = None
        self.waiting = False

    def delayed_show_win_screen(self, dt):
        self.show_win_screen()

    def update_info(self):
        self.info_label.text = f"Moves: {self.moves} | Mistakes: {self.mistakes}"

    def show_win_screen(self):
        self.root.clear_widgets()
        self.set_background('images/bnk11.png')  # พื้นหลังสำหรับหน้าที่เหลือ

        front_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        elapsed_time = round(time.time() - self.start_time, 2)
        win_label = Label(text=f"You Win!\nTime: {elapsed_time} seconds\nMoves: {self.moves}", font_size=24, size_hint=(1, 0.5))
        back_button = Button(text="Back to Main Menu", size_hint=(1, 0.2), on_press=lambda x: self.create_main_menu())

        front_layout.add_widget(win_label)
        front_layout.add_widget(back_button)

        self.root.add_widget(front_layout)

if __name__ == '__main__':
    MatchingGameApp().run()
