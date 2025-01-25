from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.core.window import Window
from random import shuffle
import time


class MatchingGameApp(App):
    def build(self):
        Window.size = (1280, 720)
        self.start_time = None
        self.root = RelativeLayout()
        self.create_main_menu()
        return self.root

    def set_background(self, image_path):
        background = Image(
            source=image_path,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        self.root.add_widget(background)

    def create_main_menu(self):
        self.root.clear_widgets()
        self.set_background('images/bnk123.png')

        front_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(text="", font_size=32, size_hint=(1, 0.2))

        play_button_container = BoxLayout(
            size_hint=(1, 1),
            orientation='vertical',
            padding=[0, 50, 0, 50]
        )

        play_button = Button(
            background_normal='images/play1.png',
            background_down='images/play2.png',
            size_hint=(None, None),
            size=(816, 79),
            pos_hint={'center_x': 0.5},
            on_press=self.show_mode_selection
        )

        play_button_container.add_widget(Label(size_hint=(1, 0.5)))
        play_button_container.add_widget(play_button)
        play_button_container.add_widget(Label(size_hint=(1, 0.4)))

        front_layout.add_widget(title)
        front_layout.add_widget(play_button_container)

        self.root.add_widget(front_layout)

    def show_mode_selection(self, instance):
        self.root.clear_widgets()
        self.set_background('images/bnnn.png')

        layout = RelativeLayout()

        # Back Button
        back_button = Button(
            background_normal='images/leftblack.png',
            size_hint=(None, None),
            size=(223.2, 72),
            pos_hint={'x': 0.05, 'y': 0.85},
            on_press=lambda x: self.create_main_menu()
        )
        layout.add_widget(back_button)

        # Easy Button
        easy_button = Button(
            background_normal='images/easy1.png',
            background_down='images/easy2.png',
            size_hint=(None, None),
            size=(816, 79),
            pos_hint={'center_x': 0.5, 'y': 0.45}
        )
        easy_button.bind(on_press=lambda x: self.start_game(4, 4, 'easy'))
        layout.add_widget(easy_button)

        # Normal Button
        normal_button = Button(
            background_normal='images/normal1.png',
            background_down='images/normal2.png',
            size_hint=(None, None),
            size=(816, 79),
            pos_hint={'center_x': 0.5, 'y': 0.35}
        )
        normal_button.bind(on_press=lambda x: self.start_game(5, 4, 'normal'))
        layout.add_widget(normal_button)

        # Hard Button
        hard_button = Button(
            background_normal='images/hard1.png',
            background_down='images/hard2.png',
            size_hint=(None, None),
            size=(816, 79),
            pos_hint={'center_x': 0.5, 'y': 0.25}
        )
        hard_button.bind(on_press=lambda x: self.start_game(6, 5, 'hard'))
        layout.add_widget(hard_button)

        self.root.add_widget(layout)

    def start_game(self, rows, cols, mode):
        self.root.clear_widgets()
        self.set_background('images/bnk11.png')

        self.score = 0
        self.moves = 0
        self.mistakes = 0
        self.first_card = None
        self.second_card = None
        self.waiting = False
        self.start_time = time.time()

        if mode == 'easy':
            images = [
                'images/ea1.png', 'images/ea4.png', 'images/ea7.png',
                'images/ea2.png', 'images/ea5.png', 'images/ea8.png',
                'images/ea3.png', 'images/ea6.png'
            ]
        elif mode == 'normal':
            images = [
                'images/no1.png', 'images/no5.png', 'images/no8.png',
                'images/no2.png', 'images/no6.png', 'images/no9.png',
                'images/no3.png', 'images/no7.png', 'images/no10.png',
                'images/no4.png'
            ]
        elif mode == 'hard':
            images = [
                'images/ha1.png', 'images/ha6.png', 'images/ha11.png',
                'images/ha2.png', 'images/ha7.png', 'images/ha12.png',
                'images/ha3.png', 'images/ha8.png', 'images/ha13.png',
                'images/ha4.png', 'images/ha9.png', 'images/ha14.png',
                'images/ha5.png', 'images/ha10.png', 'images/ha15.png'
            ]

        images = images[:(rows * cols) // 2] * 2
        shuffle(images)

        top_bar = RelativeLayout(size_hint_y=None, height=100)

        # Back Button
        back_button = Button(
            background_normal='images/leftblack.png',
            size_hint=(None, None),
            size=(223.2, 72),
            pos_hint={'x': 0.05, 'y': 7.65},
            on_press=lambda x: self.show_mode_selection(None)
        )
        top_bar.add_widget(back_button)

        grid = GridLayout(cols=cols, spacing=10, padding=10, size_hint=(None, None))
        grid.bind(minimum_width=grid.setter('width'))
        grid.width = cols * 148 + (cols - 1) * 10
        grid.height = rows * 132 + (rows - 1) * 10
        grid.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.cards = []

        for image in images:
            card = Button(
                background_normal='images/heatt.png',
                background_color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(148, 132)
            )
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
            self.check_match()

    def check_match(self):
        if self.first_card.image == self.second_card.image:
            self.first_card = None
            self.second_card = None
            self.score += 1
            if self.score == len(self.cards) // 2:
                self.waiting = True
                Clock.schedule_once(self.delayed_show_win_screen, 3)
        else:
            self.mistakes += 1
            self.waiting = True
            Clock.schedule_once(self.hide_cards, 1)

    def hide_cards(self, dt):
        self.first_card.background_normal = 'images/heatt.png'
        self.second_card.background_normal = 'images/heatt.png'
        self.first_card.revealed = False
        self.second_card.revealed = False
        self.first_card = None
        self.second_card = None
        self.waiting = False

    def delayed_show_win_screen(self, dt):
        self.show_win_screen()

    def update_info(self):
        pass  # ไม่แสดงข้อมูล Moves และ Mistakes

    def show_win_screen(self):
        self.root.clear_widgets()
        self.set_background('images/youwinn.png')  # เปลี่ยนพื้นหลังเป็น youwinn.png

        front_layout = BoxLayout(
            orientation='vertical',
            padding=[50, 50, 50, 50],
            spacing=20,
            size_hint=(None, None),
            size=(900, 400),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        elapsed_time = round(time.time() - self.start_time, 2)

        win_label = Label(
            text=f"",
            font_size=24,
            size_hint=(1, 0.7),
            halign='center',
            valign='middle'
        )
        win_label.bind(size=win_label.setter('text_size'))

        back_button = Button(
            background_normal='images/back_black.png',
            size_hint=(None, None),
            size=(816, 80),
            pos_hint={'center_x': 0.5},
            on_press=lambda x: self.create_main_menu()
        )

        front_layout.add_widget(win_label)
        front_layout.add_widget(back_button)

        self.root.add_widget(front_layout)


if __name__ == '__main__':
    MatchingGameApp().run()
