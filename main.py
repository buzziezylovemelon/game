from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from random import shuffle


class MatchingGameApp(App):
    def build(self):
        self.score = 0
        self.first_card = None
        self.second_card = None
        self.waiting = False

        self.root = GridLayout(cols=4, spacing=10, padding=10)
        self.cards = []

        # รูปภาพตัวอย่าง (สามารถเปลี่ยนเป็น path ของรูปจริง)
        images = ['🍎', '🍌', '🍓', '🍇', '🍉', '🍍', '🍒', '🥝']
        images = images * 2  # ทำให้มี 2 ใบต่อรูป
        shuffle(images)

        for image in images:
            card = Button(text='', font_size=32, background_normal='', background_color=(1, 1, 1, 1))
            card.image = image
            card.revealed = False
            card.bind(on_press=self.on_card_click)
            self.cards.append(card)
            self.root.add_widget(card)

        self.score_label = Label(text=f"Score: {self.score}", font_size=24, size_hint_y=None, height=50)
        self.root.add_widget(self.score_label)
        return self.root

    def on_card_click(self, card):
        if self.waiting or card.revealed:
            return

        # แสดงรูปของไพ่
        card.text = card.image
        card.revealed = True

        if not self.first_card:
            self.first_card = card
        elif not self.second_card:
            self.second_card = card
            self.check_match()

    def check_match(self):
        if self.first_card.image == self.second_card.image:
            self.score += 1
            self.update_score()
            self.first_card = None
            self.second_card = None
        else:
            self.waiting = True
            Clock.schedule_once(self.hide_cards, 1)

    def hide_cards(self, dt):
        self.first_card.text = ''
        self.second_card.text = ''
        self.first_card.revealed = False
        self.second_card.revealed = False
        self.first_card = None
        self.second_card = None
        self.waiting = False

    def update_score(self):
        self.score_label.text = f"Score: {self.score}"


if __name__ == '__main__':
    MatchingGameApp().run()
