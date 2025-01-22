from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from random import shuffle
import time

class MatchingGameApp(App):
    def build(self):
        self.start_time = None
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.create_main_menu()
        return self.root

    def create_main_menu(self):
        self.root.clear_widgets()
        title = Label(text="Matching Game", font_size=32, size_hint=(1, 0.2))
        play_button = Button(text="Play", size_hint=(1, 0.2), on_press=self.show_mode_selection)
        self.root.add_widget(title)
        self.root.add_widget(play_button)

    def show_mode_selection(self, instance):
        self.root.clear_widgets()

        # สร้างแถบด้านบนพร้อมปุ่ม "left"
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        back_button = Button(background_normal='images/left.jpg', size_hint=(None, None), size=(50, 50),
                              on_press=lambda x: self.create_main_menu())
        top_bar.add_widget(back_button)

        # เพิ่มข้อความ "Select Difficulty"
        title = Label(text="Select Difficulty", font_size=24, size_hint=(1, 0.2))

        # เพิ่มปุ่มเลือกระดับความยาก
        easy_button = Button(text="Easy", size_hint=(1, 0.2), on_press=lambda x: self.start_game(4, 4, 'easy'))
        normal_button = Button(text="Normal", size_hint=(1, 0.2), on_press=lambda x: self.start_game(5, 4, 'normal'))
        hard_button = Button(text="Hard", size_hint=(1, 0.2), on_press=lambda x: self.start_game(6, 5, 'hard'))

        # เพิ่ม widgets ทั้งหมดใน root layout
        self.root.add_widget(top_bar)  # แถบด้านบน
        self.root.add_widget(title)  # ข้อความหัวเรื่อง
        self.root.add_widget(easy_button)  # ปุ่ม Easy
        self.root.add_widget(normal_button)  # ปุ่ม Normal
        self.root.add_widget(hard_button)  # ปุ่ม Hard

    def start_game(self, rows, cols, mode):
        self.root.clear_widgets()
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
                'images/hard/car.jpg', 'images/hard/bus.jpg', 'images/hard/train.jpg',
                'images/hard/plane.jpg', 'images/hard/ship.jpg', 'images/hard/bike.jpg',
                'images/hard/truck.jpg', 'images/hard/rocket.jpg', 'images/hard/helicopter.jpg',
                'images/hard/submarine.jpg', 'images/hard/tractor.jpg', 'images/hard/scooter.jpg',
                'images/hard/yacht.jpg', 'images/hard/balloon.jpg', 'images/hard/glider.jpg'
            ]

        images = images[:(rows * cols) // 2] * 2  # Limit images to fit the grid
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
                self.show_win_screen()
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

    def update_info(self):
        self.info_label.text = f"Moves: {self.moves} | Mistakes: {self.mistakes}"

    def show_win_screen(self):
        self.root.clear_widgets()
        elapsed_time = round(time.time() - self.start_time, 2)
        win_label = Label(text=f"You Win!\nTime: {elapsed_time} seconds\nMoves: {self.moves}", font_size=24, size_hint=(1, 0.5))
        back_button = Button(text="Back to Main Menu", size_hint=(1, 0.2), on_press=lambda x: self.create_main_menu())
        self.root.add_widget(win_label)
        self.root.add_widget(back_button)

if __name__ == '__main__':
    MatchingGameApp().run()
