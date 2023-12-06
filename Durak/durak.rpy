default persistent._durak_wins = {"Monika": 0, "Player": 0, "Draws": 0}
default persistent._durak_last_winner = None
default 10 persistent._durak_rules = dict(store.durak.DEF_RULES_VALUES)

label durak_rules:
    m 3esa "The deck is shuffled, and each player is dealt six cards."
    m "The bottom card of the deck is turned faced up and rotated so it can be seen, its suit determining the trump suit for the game."
    m "Cards of the trump suit can beat all cards of the other suits."
    m "After that, if it's the first game for the group of players, each of them says what's the lowest trump card they have."
    m "The player with the lowest of all starts the game, being the attacker."
    m "But if it's not the first game they're playing, then the player to the left of the one who lost starts."
    m "The attacker opens their turn by playing one of their cards face up on the table as an attacking card."
    m "The player to the attacker's left is the defender, who responds to the attack with a defending card."
    m "The defending card must be of the same suit as the attacking card and rank higher than it."
    m "Alternatively, if the attacking card is not of the trump suit, then, as I mentioned before, any card of the trump suit can be used to defend."
    m "The attacker can continue attacking with cards of the same ranks as the ones which have already been used in the round."
    m "The round ends when the attacker or the defender can't or is not willing to attack or defend."
    m "Then players take cards from the deck until everyone has at least 6 of them, unless the deck is exhausted of course."
    m "If the defender successfully defended, they become the new attacker. The cards used in the round are turned face down and passed to the side."
    m 3tsa "But if not, they take all of the cards used in the round, with the player to their left becoming the new attacker instead."
    m 3esa "The game continues until everyone except for one player is out of cards. The last player to still have some cards loses, {w=0.5}{nw}"
    extend 3tsa "becoming a {i}fool{/i}."
    m 1hublsdlb ".{w=0.5}.{w=0.5}.{w=0.5}Got it?~"
    m 3esa "However, if that last player has only one card and manages to defend with it, in case the players agreed beforehand to allow draws, then it's gonna be a draw."
    # hell no, I'm done with this
    #m "There's also a variant of Durak called {i}Perevodnoy{/i}, which translates from Russian to {i}transferrable{/i}."
    #m "The point of it is that at the start of the attack, if the defender has a card of the same rank the attacker used,"
    #m "they can add that card to the attacks and become the new attacker, with the player to their left becoming the new defender."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="durak_unlock",
            conditional="store.mas_xp.level() >= 10",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label durak_unlock:
    m 1esa "Hey, [player]. Have you ever heard of a game called {i}Durak{/i}?"
    m 3esa "Translating from Russian to {i}fool{/i}, it's the most popular card game in most of the post-Soviet countries."
    m "Typical french-suited playing cards are used for it, {w=0.5}{nw}"
    extend 3hubla "and it just happens I have a deck of such cards for us to play~"
    m 3esa "In this game, instead of a usual 52-card deck, a 36 one is used, excluding numerical cards 2 through 5."
    m 3eua "However, if you want, we can use those cards too so our games last a bit longer."
    $ durak_rules_seen = False
    label .menu_loop:
        if not durak_rules_seen:
            m 1eua "Do you want me to explain the rules?{nw}"
        else:
            m 1eua "So, that's about it. Do you want me to explain the rules again?{nw}"
        $ _history_list.pop()
        menu:
            extend ""
            "Yes.":
                m 1hua "Alright!"
                call durak_rules
                $ durak_rules_seen = True
                jump durak_unlock.menu_loop
            "No.":
                pass
    m 1hubla "Alright, can't wait to play with you~"
    $ del durak_rules_seen
    $ mas_unlockGame("durak")
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_game_database,
            eventlabel="durak",
            prompt="Durak"
        ),
        code="GME",
        restartBlacklist=True
    )

label durak:
    m 3eua "Do you want to change any rules?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you want to change any rules?{fast}"
        "Yes.":
            m "Which rules would you like to change?{nw}"
            call durak_rules_loop
        "No.":
            pass
    call durak_start
    return

label durak_start:
    m 1hua "Alright!"
    m 1eub "Let me deal our cards~"
    $ store.durak.game = store.durak.Durak()
    $ HKBHideButtons()
    $ disable_esc()
    scene bg cardgames desk onlayer master zorder 0
    $ store.durak.game.table.show()
    show screen durak_gui
    show screen durak_stats
    with Fade(0.2, 0, 0.2)
    $ renpy.pause(0.2, hard=True)
    $ store.durak.game.game_loop()
    jump durak_end

label durak_rules_loop:
    python:
        _history_list.pop()
        m("Which rules would you like to change?{fast}", interact=False)
        options = []
        if persistent._durak_rules.get("cards_amount") == 36:
            options.append(("Change deck size to 52", "ca52", False, False))
        else:
            options.append(("Change deck size to 36", "ca36", False, False))
        if persistent._durak_rules.get("allow_draws"):
            options.append(("Disable draws", "ad2", False, False))
        else:
            options.append(("Enable draws", "ad1", False, False))
        final_option = ("Done", "done", False, False, 20)
    show monika at t21
    call screen mas_gen_scrollable_menu(options, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_option)
    if _return == "ca36":
        $ persistent._durak_rules["cards_amount"] = 36
    elif _return == "ca52":
        $ persistent._durak_rules["cards_amount"] = 52
    elif _return == "ad1":
        $ persistent._durak_rules["allow_draws"] = True
    elif _return == "ad2":
        $ persistent._durak_rules["allow_draws"] = False
    elif _return == "done":
        show monika at t11
        return
    jump durak_rules_loop

label durak_end:
    $ store.durak.game.table.hide()
    hide screen durak_gui
    hide screen durak_stats
    call spaceroom(scene_change=True, force_exp="monika 1eua")
    $ enable_esc()
    $ HKBShowButtons()
    #window auto
    $ store.durak.game.end_quips()
    m 3eua "Would you like to play again?{nw}"
    $ _history_list.pop()
    menu:
        m "Would you like to play again?{fast}"
        "Yes.":
            jump durak_start
        "Yes, but I'd like to change some rules.":
            m "Which rules would you like to change?{nw}"
            call durak_rules_loop
            jump durak_start
        "No.":
            m 1hua "Alright! Can't wait to play with you again!"
    return

screen durak_gui():
    zorder 50
    style_prefix "nou"
    vbox:
        xalign 0.975
        yalign 0.5
        textbutton "Beaten":
            sensitive store.durak.game.beaten_button_active
            action [
                SetField(store.durak.game, "beaten_needed", True),
                Function(store.durak.game.getmeoutofloop)
            ]
        textbutton "Pass":
            sensitive store.durak.game.pass_button_active
            action [
                Function(store.durak.game.draw, store.durak.game.monika),
                Function(store.durak.game.getmeoutofloop)
            ]
        textbutton "Draw":
            sensitive store.durak.game.draw_button_active
            action [
                Function(store.durak.game.getmeoutofloop)
            ]
        textbutton "Can you help me?":
            sensitive store.durak.game.help_button_active
            action [
                SetField(store.durak.game, "help_needed", True),
                Function(store.durak.game.getmeoutofloop)
            ]


screen durak_stats():
    layer "master"
    zorder 5
    style_prefix "nou"
    $ nou_ma_dir = store.config.gamedir.replace("\\", "/") + "/mod_assets/games/nou/"
    add MASFilterSwitch(
        nou_ma_dir + "note.png"
    ) pos (5, 120) anchor (0, 0) at nou_note_rotate_left

    add MASFilterSwitch(
        nou_ma_dir + "pen.png"
    ) pos (130, 420) anchor (0.5, 0.5) at nou_pen_rotate_right

    text _("Our score!") pos (87, 110) anchor (0, 0.5) at nou_note_rotate_left
    text _("Monika: " + str(store.persistent._durak_wins["Monika"])) pos (60, 204) anchor (0, 0.5) at nou_note_rotate_left
    if store.persistent._durak_rules.get("allow_draws"):
        text _("[player]: " + str(store.persistent._durak_wins["Player"])) pos (78, 251) anchor (0, 0.5) at nou_note_rotate_left
        text _("Draws: " + str(store.persistent._durak_wins["Draws"])) pos (96, 298) anchor (0, 0.5) at nou_note_rotate_left
    else:
        text _("[player]: " + str(store.persistent._durak_wins["Player"])) pos (96, 298) anchor (0, 0.5) at nou_note_rotate_left

init 500 python in durak:
    Durak.load_sfx()

init 5 python in durak:
    import random
    import os
    import time
    from threading import Timer
    from store import (
        m,
        persistent,
        config,
        Solid,
        Null
    )
    from store.mas_cardgames import *

    ASSETS = "submods/Durak/submod_assets/"
    game = None

    DEF_RULES_VALUES = {
        "cards_amount": 36,
        "allow_draws": False
    }

    class Durak(object):
        DISCARDPILE_X = 785
        DISCARDPILE2C1_X = DISCARDPILE_X - 11 - 75
        DISCARDPILE2C2_X = DISCARDPILE_X + 11 + 75
        DISCARDPILE3C1_X = DISCARDPILE_X - 75 - 22 - 75
        DISCARDPILE3C2_X = DISCARDPILE_X
        DISCARDPILE3C3_X = DISCARDPILE_X + 75 + 22 + 75
        DISCARDPILE_Y = 360
        DISCARDPILE2R1_Y = 240
        DISCARDPILE2R2_Y = 480
        ACTUALDISCARDPILE_X = 1205
        ACTUALDISCARDPILE_Y = 360
        DRAWPILE_X = DISCARDPILE_X - 75 - 22 - 150 - 22 - 75 - 75
        DRAWPILE_Y = 360
        HAND_X = 640
        PLAYERHAND_Y = 720
        MONIKAHAND_Y = 0
        CARDS_OFFSET = 28
        MONIKA_THINK_TIME_MIN = 1.5
        MONIKA_THINK_TIME_MAX = 2.0

        CARD_VALUES_1 = (6, 7, 8, 9, 10, 11, 12, 13, 14)
        CARD_VALUES_2 = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
        SUITS = ("c", "d", "h", "s")

        trump_suit = None
        player_start_lowest_trump_card_value = None
        player_has_drawn_from_drawpile = False
        winner = None
        discardpiles_size = 0
        turn_in_progress = False
        beaten_button_active = False
        draw_button_active = False
        pass_button_active = False
        help_button_active = False
        help_needed = False
        beaten_needed = False

        SFX_EXT = ".mp3"
        SFX_SHUFFLE = []
        SFX_MOVE = []
        SFX_DRAW = []
        SFX_PLAY = []

        QUIPS_MONIKA_DRAWS_CARDS = (
            ("I draw...", "Ugh, I don't have anything...", "So fortunate..."),
            ("I draw.", "Can't beat that!", "Gotta draw."),
            ("Aw, I've almost beaten everything!", "How are you able to do all this?", "I can't keep up with this...")
        )
        QUIPS_PLAYER_DRAWS_CARDS = (
            ("Seems like your situation isn't the greatest~", "Sorry~", "You'll have better luck next time~"),
            ("Alrighty~", "Good~", "Go ahead~"),
            ("Perfect~", "Thought you could get away?~", "Hehe, that's a lot of cards you're getting~")
        )
        QUIPS_MONIKA_BEATEN = (
            ("Beaten.", "Nothing else I can do!", "Well done!", "Consider yourself lucky!", "Not bad!"),
            ("You're so lucky...", "Next time you definitely won't be getting away!", "...Beaten.")
        )
        QUIPS_PLAYER_BEATEN = (
            ("Okie dokie~", "Alright!", "Good~"),
            ("Thought I would have to draw?~", "You almost got me there~", "That was close!", "Phew!")
        )

        def __init__(self):
            self.table = Table(
                back = ASSETS + "back.png",
                base=Null(),
                springback=0.3,
                rotate=0.15,
            )
            self.drawpile = self.table.stack(
                self.DRAWPILE_X,
                self.DRAWPILE_Y,
                xoff=0,
                yoff=0,
            )
            self.getmeoutoflooppile = self.table.stack(
                640,
                360,
                xoff=0,
                yoff=0,
                hover=True
            )
            screen_card = DurakCard(0, "0")
            self.table.card(screen_card, ASSETS + "screen.png")
            self.getmeoutoflooppile.append(screen_card)
            self.table.stacks.remove(self.getmeoutoflooppile)
            self.discardpile = self.table.stack(
                self.DISCARDPILE_X,
                self.DISCARDPILE_Y,
                xoff=0,
                yoff=0,
                drop=True
            )
            placeholder_card = DurakCard(0, "0")
            self.table.card(placeholder_card, ASSETS + "placeholder.png")
            self.discardpile.append(placeholder_card)
            self.table.stacks.remove(self.discardpile)
            self.discardpile1 = self.table.stack(
                -500,
                -500,
                xoff=18,
                yoff=18,
                drop=True
            )
            self.discardpile2 = self.table.stack(
                -500,
                -500,
                xoff=18,
                yoff=18,
                drop=True
            )
            self.discardpile3 = self.table.stack(
                -500,
                -500,
                xoff=18,
                yoff=18,
                drop=True
            )
            self.discardpile4 = self.table.stack(
                -500,
                -500,
                xoff=18,
                yoff=18,
                drop=True
            )
            self.discardpile5 = self.table.stack(
                -500,
                -500,
                xoff=18,
                yoff=18,
                drop=True
            )
            self.discardpile6 = self.table.stack(
                -500,
                -500,
                xoff=18,
                yoff=18,
                drop=True
            )
            self.discardpiles = [self.discardpile1, self.discardpile2, self.discardpile3, self.discardpile4, self.discardpile5, self.discardpile6]
            self.actualdiscardpile = self.table.stack(
                self.ACTUALDISCARDPILE_X,
                self.ACTUALDISCARDPILE_Y,
                xoff = 0,
                yoff = 0,
            )
            self.player = DurakPlayer()
            self.monika = DurakPlayerAI(self)
            self.player.hand = self.table.stack(
                self.HAND_X,
                self.PLAYERHAND_Y,
                xoff=self.CARDS_OFFSET,
                yoff=0,
                click=True,
                drag=DRAG_CARD,
                hover=True,
                drop=True
            )
            self.monika.hand = self.table.stack(
                self.HAND_X,
                self.MONIKAHAND_Y,
                xoff=self.CARDS_OFFSET,
                yoff=0,
            )
            self.table.set_sensitive(False)
            self.fill_deck()

        def game_loop(self):
            self.shuffle_drawpile()
            if persistent._durak_last_winner == "Monika":
                self.deal_initial_cards(self.monika, self.player)
            elif persistent._durak_last_winner == "Player":
                self.deal_initial_cards(self.player, self.monika)
            else:
                if bool(renpy.random.randint(0, 1)):
                    self.deal_initial_cards(self.monika, self.player)
                else:
                    self.deal_initial_cards(self.player, self.monika)
            self.who_starts_game()
            while True:
                self.discardpiles_size = 0
                for card in self.player.hand:
                    self.table.get_card(card).hovered = False
                attacker_player, defender_player = self.get_attacker_defender_players()
                if self.drawpile and (len(self.monika.hand) < 6 or len(self.player.hand) < 6):
                    renpy.pause(0.5, hard=True)
                    self.deal_not_initial_cards(defender_player, attacker_player)
                if not self.player.hand or not self.monika.hand:
                    renpy.pause(1, hard=True)
                    break
                self.turn_in_progress = True
                if len(self.drawpile) <= 1:
                    for card in self.player.hand:
                        if (card.suit == self.trump_suit or card.value == 14) and card not in self.monika.player_cards:
                            self.monika.player_cards.append(card)
                if attacker_player.isAI:
                    self.monika_attack()
                else:
                    self.player_attack()
            if self.monika.hand:
                self.table.springback = 0.2
                for card in self.monika.hand:
                    self.table.set_faceup(card, True)
                self.monika.hand.y = 150
                self.monika.hand.xoff = 40
                self.update_cards_positions(self.monika)
                self.play_play_sfx()
                renpy.pause(2, hard=True)
            if self.winner == self.monika:
                winner = "Monika"
            elif self.winner == self.player:
                winner = "Player"
            if persistent._durak_rules.get("allow_draws") and not self.monika.hand and not self.player.hand:
                winner = "Draws"
            persistent._durak_wins[winner] = persistent._durak_wins.get(winner) + 1
            persistent._durak_last_winner = winner
            store.mas_gainAffection()

        def fill_deck(self):
            if persistent._durak_rules.get("cards_amount") == 36:
                values = self.CARD_VALUES_1
            else:
                values = self.CARD_VALUES_2
            for suit in self.SUITS:
                for value in values:
                    card = DurakCard(value, suit)
                    self.table.card(card, ASSETS + str(value) + suit + ".png")
                    self.table.set_rotate(card, renpy.random.randint(-5, 5))
                    self.table.set_faceup(card, False)
                    self.drawpile.append(card)
        
        def shuffle_drawpile(self):
            total_cards = len(self.drawpile)
            self.play_shuffle_sfx()
            k = renpy.random.randint(0, 9)
            self.table.springback = 0.2
            renpy.pause(0.2, hard=True)
            for i in range(7):
                card_id = renpy.random.randint(0, total_cards - 2)
                if k == i:
                    insert_id = total_cards - 1
                else:
                    insert_id = renpy.random.randint(0, total_cards - 2)
                self.table.set_rotate(self.drawpile[card_id], 0)
                card = self.table.get_card(self.drawpile[card_id])
                x_offset = renpy.random.randint(160, 190)
                y_offset = renpy.random.randint(-15, 15)
                card.set_offset(x_offset, y_offset)
                card.springback()
                renpy.pause(0.15, hard=True)
                self.drawpile.insert(insert_id, card.value)
                card.set_offset(0, 0)
                card.springback()
                renpy.pause(0.15, hard=True)
            self.table.springback = 0.3
            self.drawpile.shuffle()
            renpy.pause(0.2, hard=True)

        def who_starts_game(self, repeat=False):
            if persistent._durak_last_winner == "Player":
                self.say_quip("Since you won our last game, you can start~")
                self.player.attacker = True
            elif persistent._durak_last_winner == "Draws" or persistent._durak_last_winner is None:
                if persistent._durak_last_winner == "Draws" and not repeat:
                    self.say_quip("Since we had a draw our last game, we once again need to determine the attacker by the lowest trump card we have.")
                elif not repeat:
                    self.say_quip("Since this is our first game, we need to determine the attacker by the lowest trump card (i.e., in this case, of the " + self.card_suit_to_str(self.trump_suit) + " suit) we have.")
                self.say_quip("What's your lowest trump card? Don't try lying to me~")
                values_list = [("6", 6, False, False), ("7", 7, False, False), ("8", 8, False, False), ("9", 9, False, False), ("10", 10, False, False), ("Jack", 11, False, False), ("Queen", 12, False, False), ("King", 13, False, False), ("Ace", 14, False, False), ("None", 15, False, False)]
                if persistent._durak_rules.get("cards_amount") == 52:
                    values_list[0:0] = [("2", 2, False, False), ("3", 3, False, False), ("4", 4, False, False), ("5", 5, False, False)]
                result = renpy.call_screen("mas_gen_scrollable_menu", items=values_list, display_area=(540, 142, 200, 435), scroll_align=store.mas_ui.SCROLLABLE_MENU_XALIGN)
                if result == self.drawpile[0].value:
                    self.say_quip("...")
                    self.say_quip("That card is literally shown under the drawpile.")
                    self.say_quip("You can be so silly sometimes, you know that?~")
                    self.say_quip("Let's try again.")
                    self.who_starts_game(repeat=True)
                    return
                monika_lowest_trump_card_value = 15
                for card in self.monika.hand:
                    if card.value < monika_lowest_trump_card_value and card.suit == self.trump_suit:
                        monika_lowest_trump_card_value = card.value
                    if card.value == result and card.suit == self.trump_suit:
                        self.say_quip("...")
                        self.say_quip("But I have that card...")
                        self.say_quip("Let's imagine I didn't hear that.")
                        self.who_starts_game(repeat=True)
                        return
                if monika_lowest_trump_card_value > result:
                    self.player.attacker = True
                    if monika_lowest_trump_card_value == 15:
                        self.say_quip("Alright, I don't have any trump cards, so you can start.")
                    else:
                        self.say_quip("Alright, mine is " + self.card_value_to_str(monika_lowest_trump_card_value) + ", so you can start.")
                elif monika_lowest_trump_card_value == result == 15:
                    self.say_quip("Huh, me neither...")
                    k = renpy.random.randint(0, 1)
                    if k == 0:
                        self.player.attacker = True
                        self.say_quip("Whatever, you can start.")
                    else:
                        self.say_quip("Whatever, I'll start.")
                else:
                    self.say_quip("Heh, mine is " + self.card_value_to_str(monika_lowest_trump_card_value) + ", so I'll start.")
                self.player_start_lowest_trump_card_value = result
                for card in self.drawpile:
                    if card.suit == self.trump_suit and card.value == result:
                        self.monika.player_cards.append(card)
                        break
                for card in self.player.hand:
                    if card.suit == self.trump_suit and card.value == result:
                        self.monika.player_cards.append(card)
                        break
            else:
                self.say_quip("Since I won our last game, I'll start~")

        def card_value_to_str(self, card_value):
            if card_value == 11:
                return "a Jack"
            elif card_value == 12:
                return "a Queen"
            elif card_value == 13:
                return "a King"
            elif card_value == 14:
                return "an Ace"
            elif card_value == 8:
                return "an 8"
            else:
                return "a " + str(card_value)
        
        def card_suit_to_str(self, card_suit):
            if card_suit == "h":
                return "hearts"
            elif card_suit == "d":
                return "diamonds"
            elif card_suit == "c":
                return "clubs"
            elif card_suit == "s":
                return "spades"

        def get_attacker_defender_players(self):
            if self.player.attacker:
                attacker_player = self.player
                defender_player = self.monika
            else:
                attacker_player = self.monika
                defender_player = self.player
            return (attacker_player, defender_player)

        def deal_initial_cards(self, attacker_player, defender_player):
            for i in range(0, 6):
                self.deal_a_card(defender_player)
                self.deal_a_card(attacker_player)
            self.play_draw_sfx()
            card = self.drawpile[-1]
            self.table.get_card(card).set_offset(200, 0)
            self.table.set_rotate(card, 90)
            self.table.set_faceup(card, True)
            self.table.get_card(card).springback()
            renpy.pause(0.4, hard=True)
            self.table.get_card(card).set_offset(41, 0)
            self.table.get_card(card).springback()
            self.trump_suit = card.suit
            for i in range(len(self.drawpile)-1):
                card = self.drawpile[0]
                self.drawpile.append(card)

        def deal_not_initial_cards(self, attacker_player, defender_player):
            while len(attacker_player.hand) < 6 and self.drawpile:
                self.deal_a_card(attacker_player)
            while len(defender_player.hand) < 6 and self.drawpile:
                self.deal_a_card(defender_player)
        
        def deal_a_card(self, player):
            if player == self.player and len(self.drawpile) <= persistent._durak_rules.get("cards_amount") - 12:
                self.player_has_drawn_from_drawpile = True
            self.play_draw_sfx()
            card = self.drawpile[-1]
            self.table.get_card(card).set_offset(0, 0)
            self.table.set_rotate(card, 0)
            if player.isAI:
                faceup = False
                player.hand.insert(0, card)
            else:
                faceup = True
                player.hand.append(card)
            self.table.set_faceup(card, faceup)
            self.update_cards_positions(player)
            renpy.pause(0.3, hard=True)
            if player == self.monika and card.suit == self.trump_suit and card.value == self.player_start_lowest_trump_card_value:
                self.say_quip("...")
                self.say_quip("So at the beginning you said you had " + self.card_value_to_str(card.value) + " of " + self.card_suit_to_str(self.trump_suit) + ".")
                self.say_quip("Well, guess what, I just got that card from the drawpile.")
                self.say_quip("Why would you lie to me...")
                self.monika.player_cards.remove(card)
                store.mas_loseAffection()
        
        def update_cards_positions(self, player):
            xpos = self.HAND_X
            amount = len(player.hand) - 1
            xpos -= (amount * self.CARDS_OFFSET / 2)
            player.hand.x = xpos
            for card in player.hand:
                self.table.get_card(card).springback()

        def beaten(self):
            self.play_play_sfx()
            if self.player.attacker:
                self.player.attacker = False
            else:
                self.player.attacker = True
            for a_discardpile in self.discardpiles:
                cards_to_disable = []
                for card in a_discardpile:
                    self.table.set_faceup(card, False)
                    self.table.set_rotate(card, renpy.random.randint(45, 135))
                    self.table.get_card(card).set_offset(0, renpy.random.randint(-200, 200))
                    cards_to_disable.append(card)
                for card in cards_to_disable:
                    self.actualdiscardpile.append(card)    
            self.turn_in_progress = False

        def getmeoutofloop(self):
            self.table.stacks.append(self.getmeoutoflooppile)
            x, y = renpy.get_mouse_pos()
            renpy.set_mouse_pos(640, 360)
            renpy.set_mouse_pos(x, y)
            
        def draw(self, loser):
            self.play_draw_sfx()
            cards_in_discardpiles = []
            for a_discardpile in self.discardpiles:
                for card in a_discardpile:
                    cards_in_discardpiles.append(card)
            for card in cards_in_discardpiles:
                self.table.set_rotate(card, 0)
                if loser.isAI:
                    self.table.set_faceup(card, False)
                    self.monika.hand.insert(0, card)
                    self.update_cards_positions(self.monika)
                else:
                    if len(self.drawpile) <= max(0, 6-len(self.monika.hand)):
                        for card_couldnt_beat in self.monika.player_couldnt_beat:
                            if self.can_defend(card_couldnt_beat, card) and card.suit != self.trump_suit:
                                self.monika.player_couldnt_beat[:] = [card if x==card_couldnt_beat else x for x in self.monika.player_couldnt_beat]
                    self.player.hand.append(card)
                    self.update_cards_positions(self.player)
                    self.monika.player_cards.append(card)
                    self.monika.player_cards[:] = self.sort_cards(self.monika.player_cards)
            self.beaten_button_active = False
            self.pass_button_active = False
            self.draw_button_active = False
            self.turn_in_progress = False

        def help(self, card_to_defend = None):
            self.help_needed = False
            self.table.set_sensitive(False)
            if self.player.attacker == True:
                if self.pass_button_active:
                    self.pass_button_active = False
                    self.say_quip("I have to draw. You can place more cards of the same ranks as the ones on the table for me to draw. When you're done, say \"Pass\" and I'll draw.")
                    self.pass_button_active = True
                elif not self.monika.hand:
                    self.beaten_button_active = False
                    self.say_quip("I'm out of cards, so you can't attack anymore. End this round by saying the word \"Beaten\".")
                    self.beaten_button_active = True
                elif self.discardpiles_size == 0:
                    self.say_quip("You have to choose a card to attack and place it on the table. It's common practice in most cases to use the lowest non-trump card for the first attack.")
                else:
                    self.beaten_button_active = False
                    self.say_quip("You have to choose a card to attack with the same rank as any of the cards on the table and place it on the table. Or end this round by saying the word \"Beaten\".")
                    self.beaten_button_active = True
            else:
                self.draw_button_active = False
                if card_to_defend.suit == self.trump_suit:
                    if card_to_defend.value == 14:
                        self.say_quip("Heh, it's impossible to beat an Ace of the trump suit, so you gotta draw~")
                    else:
                        self.say_quip("You have to defend against my attacking card with a card of the same suit and of a higher rank. Or you draw.")
                else:
                    if card_to_defend.value == 14:
                        self.say_quip("The only way to beat an Ace is to use a trump card. Or you draw.")
                    else:
                        self.say_quip("You have to defend against my attacking card with a card of the same suit and of a higher rank. Alternatively, you can use any trump card. Or you draw.")
                self.draw_button_active = True
            self.table.set_sensitive(True)
            self.help_button_active = True

        def player_attack(self):
            monika_incoming_defence = Timer(renpy.random.uniform(self.MONIKA_THINK_TIME_MIN, self.MONIKA_THINK_TIME_MAX), self.monika_defend)
            self.table.set_sensitive(True)
            self.table.stacks.append(self.discardpile)
            monika_draws = False
            self.help_button_active = True
            while self.turn_in_progress:
                if self.pass_button_active and not monika_draws:
                    self.pass_button_active = False
                    self.table.set_sensitive(False)
                    if self.player.hand or self.drawpile:
                        self.say_quip(self.QUIPS_MONIKA_DRAWS_CARDS[int(round(self.discardpiles_size/2.0-0.6))])
                    if not self.player.hand:
                        self.draw(self.monika)
                        break
                    self.table.set_sensitive(True)
                    self.pass_button_active = True
                    monika_draws = True
                    self.help_button_active = True
                events = ui.interact(type="minigame")
                for event in events:
                    if event.type == "drag":
                        if event.drop_stack == self.player.hand:
                            x1 = self.player.hand.x - 75
                            x2 = x1 + len(self.player.hand) * self.CARDS_OFFSET + 150 - self.CARDS_OFFSET
                            if renpy.get_mouse_pos()[0] >= x1 and renpy.get_mouse_pos()[0] <= x2 and renpy.get_mouse_pos()[1] >= 720-109:
                                pos = (renpy.get_mouse_pos()[0] - x1) / self.CARDS_OFFSET
                                self.player.hand.insert(int(pos), event.card)
                                self.update_cards_positions(self.player)
                        else:
                            canAttack = False
                            for a_discardpile in self.discardpiles:
                                for card in a_discardpile:
                                    if (card.value == event.card.value):
                                        canAttack = True
                            if (self.discardpiles_size == 0 or (self.discardpiles_size > 0 and canAttack and self.discardpiles_size < 6)) and self.monika.hand:
                                self.beaten_button_active = False
                                self.attack_card(event.card, self.player)
                                if not monika_draws:
                                    self.help_button_active = False
                                if event.card in self.monika.player_cards:
                                    self.monika.player_cards.remove(event.card)
                                self.did_player_lie(event.card)
                                monika_incoming_defence.cancel()
                                if not self.pass_button_active:
                                    monika_incoming_defence = Timer(renpy.random.uniform(self.MONIKA_THINK_TIME_MIN, self.MONIKA_THINK_TIME_MAX), self.monika_defend)
                                    monika_incoming_defence.start()
                    elif event.type == "hover":
                        if event.card in self.player.hand:
                            card = self.table.get_card(event.card)
                            card.set_offset(0, -35)
                            card.springback()
                            stack = card.stack
                            self.table.stacks.remove(stack)
                            self.table.stacks.append(stack)
                        else:
                            self.table.get_card(self.getmeoutoflooppile[0]).hovered = False
                            self.table.stacks.remove(self.getmeoutoflooppile)
                            if self.help_needed:
                                self.help_button_active = False
                                self.help()
                            if self.beaten_needed:
                                self.beaten_needed = False
                                self.help_button_active = False
                                self.beaten_button_active = False
                                if self.winner is None:
                                    if self.discardpiles_size > 3:
                                        self.say_quip(self.QUIPS_PLAYER_BEATEN[1])
                                    elif not bool(renpy.random.randint(0, 2)):
                                        self.say_quip(self.QUIPS_PLAYER_BEATEN[0])
                                self.beaten()
                    elif event.type == "unhover":
                        card = self.table.get_card(event.card)
                        card.set_offset(0, 0)
                        card.springback()
            self.help_button_active = False
            self.table.stacks.remove(self.discardpile)
            self.table.set_sensitive(False)

        def attack_card(self, card, attacker):
            self.play_play_sfx()
            self.table.set_rotate(card, renpy.random.randint(-5, 5))
            if self.discardpiles_size == 0:
                self.discardpile1.x = self.DISCARDPILE_X
                self.discardpile1.y = self.DISCARDPILE_Y
                self.discardpile1.append(card)
            elif self.discardpiles_size == 1:
                self.discardpile1.x = self.DISCARDPILE2C1_X
                self.stack_springback(self.discardpile1)
                self.discardpile2.x = self.DISCARDPILE2C2_X
                self.discardpile2.y = self.DISCARDPILE_Y
                self.discardpile2.append(card)
            elif self.discardpiles_size == 2:
                self.discardpile1.x = self.DISCARDPILE3C1_X
                self.stack_springback(self.discardpile1)
                self.discardpile2.x = self.DISCARDPILE3C2_X
                self.stack_springback(self.discardpile2)
                self.discardpile3.x = self.DISCARDPILE3C3_X
                self.discardpile3.y = self.DISCARDPILE_Y
                self.discardpile3.append(card)
            elif self.discardpiles_size == 3:
                self.discardpile4.x = self.DISCARDPILE_X
                self.discardpile1.y = self.DISCARDPILE2R1_Y
                self.stack_springback(self.discardpile1)
                self.discardpile2.y = self.DISCARDPILE2R1_Y
                self.stack_springback(self.discardpile2)
                self.discardpile3.y = self.DISCARDPILE2R1_Y
                self.stack_springback(self.discardpile3)
                self.discardpile4.y = self.DISCARDPILE2R2_Y
                self.discardpile4.append(card)
            elif self.discardpiles_size == 4:
                self.discardpile4.x = self.DISCARDPILE2C1_X
                self.stack_springback(self.discardpile4)
                self.discardpile5.x = self.DISCARDPILE2C2_X
                self.discardpile5.y = self.DISCARDPILE2R2_Y
                self.discardpile5.append(card)
            elif self.discardpiles_size == 5:
                self.discardpile4.x = self.DISCARDPILE3C1_X
                self.stack_springback(self.discardpile4)
                self.discardpile5.x = self.DISCARDPILE3C2_X
                self.stack_springback(self.discardpile5)
                self.discardpile6.x = self.DISCARDPILE3C3_X
                self.discardpile6.y = self.DISCARDPILE2R2_Y
                self.discardpile6.append(card)
            self.update_cards_positions(attacker)
            self.discardpiles_size += 1
            attacker.made_a_move = True
            if not attacker.hand and not self.drawpile:
                self.winner = attacker

        def did_player_lie(self, card):
            if not self.player.hand and self.monika.player_cards:
                self.table.set_sensitive(False)
                self.say_quip("...")
                self.say_quip("So in the beginning you said you had " + self.card_value_to_str(card.value) + " of " + self.card_suit_to_str(self.trump_suit) + ".")
                self.say_quip("But you are out of cards now and you haven't played that card, which means you never had it in the first place.")
                self.say_quip("Why would you lie to me...")
                self.monika.player_cards.remove[0]
                store.mas_loseAffection()
                self.table.set_sensitive(True)
            if card.suit == self.trump_suit and card not in self.monika.player_cards and not self.player_has_drawn_from_drawpile:
                if self.player_start_lowest_trump_card_value == 15:
                    self.table.set_sensitive(False)
                    self.say_quip("Wait...")
                    self.say_quip("Didn't you say you don't have any trump cards?")
                    self.say_quip("Aw, did you want me to start first?")
                    self.say_quip("But I want to play fair, so don't do that again, okay?")
                    self.table.set_sensitive(True)
                    self.player_has_drawn_from_drawpile = True
                elif card.value < self.player_start_lowest_trump_card_value:
                    self.table.set_sensitive(False)
                    self.say_quip("Wait...")
                    self.say_quip("This is definitely a trump card of a lower rank than the one you mentioned in the beginning.")
                    self.say_quip("Not sure what your motive was... But don't do that again, okay?")
                    self.table.set_sensitive(True)
                    self.player_has_drawn_from_drawpile = True

        def stack_springback(self, a_discardpile):
            for card in a_discardpile:
                self.table.get_card(card).springback()

        def monika_defend(self):
            self.player.made_a_move = False
            # List of cards on the table, and another list of specifically the cards Monika needs to defend
            cards_to_defend = []
            cards_in_discardpiles = []
            cards_which_safely_defend_multiple = []
            card_to_use_multiple = []
            monika_sorted_cards = self.sort_cards(self.monika.hand)
            for a_discardpile in self.discardpiles:
                for card in a_discardpile:
                    cards_in_discardpiles.append(card)
                if (len(a_discardpile) == 1):
                    cards_to_defend.append(a_discardpile[0])
            # Can Monika defend all the cards on the table? :thinking:
            for card in cards_to_defend:
                # Which cards can Monika use to defend?
                cards_which_defend = []
                for card_moni in monika_sorted_cards:
                    if self.can_defend(card, card_moni) and card_moni not in card_to_use_multiple:
                        cards_which_defend.append(card_moni)
                # Is it safe to use the card to defend, considering the cards Monika knows player has?
                all_cards_to_defend_same_value = True
                for card_to_def in cards_to_defend:
                    if cards_to_defend[0].value != card_to_def.value:
                        all_cards_to_defend_same_value = False
                        break
                if all_cards_to_defend_same_value:
                    cards_which_defend.append(cards_to_defend[0])
                cards_which_safely_defend = []
                for card_def in cards_which_defend:
                    if len(self.monika.hand) == 1:
                        cards_which_safely_defend = cards_which_defend
                        break
                    player_cards_same_value = []
                    for card_player in self.monika.player_cards:
                        if card_def.value == card_player.value:
                            player_cards_same_value.append(card_player)
                    tolerable_risks = len(player_cards_same_value) - min((6 - self.discardpiles_size), len(self.monika.hand)-1)
                    if tolerable_risks < 0:
                        tolerable_risks = 0
                    risks = 0
                    cards_potentially_used = []
                    for card_player in player_cards_same_value:
                        if card_player.suit == self.trump_suit:
                            continue
                        defended = False
                        could_defend = False
                        for card_moni in monika_sorted_cards:
                            if (self.can_defend(card_player, card_moni) and card_moni not in cards_potentially_used
                            and card_moni not in card_to_use_multiple and card_moni != card_def):
                                if (card_def == cards_to_defend[0] and card_moni in cards_which_safely_defend and not could_defend):
                                    could_defend = True
                                else:
                                    cards_potentially_used.append(card_moni)
                                    defended = True
                                    break
                        if not defended:
                            risks += 1
                    if (risks <= tolerable_risks):
                        cards_which_safely_defend.append(card_def)
                if all_cards_to_defend_same_value:
                    if cards_to_defend[0] in cards_which_safely_defend:
                        cards_which_safely_defend.remove(cards_to_defend[0])
                    else:
                        cards_which_safely_defend = []
                # If the value of a card Monika can use is the same of some other one already on the table, play it
                if cards_which_safely_defend:
                    cards_which_safely_defend_multiple.append(cards_which_safely_defend)
                    card_to_use = cards_which_safely_defend[0]
                    cards_to_use_instead = []
                    for card_def in cards_which_safely_defend:
                        if (card_def == card_to_use):
                            continue
                        for card_dis in cards_in_discardpiles:
                            if card_def.value == card_dis.value and ((card_def.suit != self.trump_suit and card_def.value - card_to_use.value <= 4)
                            or (card_def.suit == self.trump_suit and card_to_use.suit == self.trump_suit and card_def.value - card_to_use.value == 1)):
                                cards_to_use_instead.append(card_def)
                    cards_to_use_instead[:] = self.sort_cards(cards_to_use_instead)
                    if cards_to_use_instead:
                        card_to_use = cards_to_use_instead[0]
                    card_to_use_multiple.append(card_to_use)
                    cards_in_discardpiles.append(card_to_use)
                else:
                    card_to_use_multiple.append(None)
            # Draw cards
            if None in card_to_use_multiple:
                self.pass_button_active = True
                self.getmeoutofloop()
            # Defend
            else:
                for i in range(0, len(cards_to_defend)):
                    if (self.player.made_a_move is True):
                        break
                    self.play_play_sfx()
                    a_discardpile = self.table.get_card(cards_to_defend[i]).stack
                    self.table.set_faceup(card_to_use_multiple[i], True)
                    a_discardpile.append(card_to_use_multiple[i])
                    self.table.set_rotate(card_to_use_multiple[i], renpy.random.randint(-5, 5))
                    self.update_cards_positions(self.monika)
                    if not self.monika.hand and not self.drawpile:
                        self.winner = self.monika
                    if i != len(cards_to_defend)-1:
                        time.sleep(renpy.random.uniform(self.MONIKA_THINK_TIME_MIN, self.MONIKA_THINK_TIME_MAX))
                self.beaten_button_active = True
                self.help_button_active = True
                self.getmeoutofloop()
        
        def sort_cards(self, cards):
            cards_sorted = sorted(cards, key = lambda card: card.value)
            trump_cards = [x for x in cards_sorted if x.suit == self.trump_suit]
            cards_sorted[:] = [x for x in cards_sorted if not x.suit == self.trump_suit]
            cards_sorted.extend(trump_cards)
            return cards_sorted

        def can_defend(self, attacking_card, defending_card):
            if ((attacking_card.value < defending_card.value and attacking_card.suit == defending_card.suit)
            or (attacking_card.suit != self.trump_suit and defending_card.suit == self.trump_suit)):
                return True
            else:
                return False

        def monika_attack(self):
            monika_sorted_cards = self.sort_cards(self.monika.hand)
            player_draws = False
            while self.turn_in_progress:
                #player draws
                if not monika_sorted_cards and player_draws:
                    self.draw(self.player)
                    break
                #find card to use
                renpy.pause(renpy.random.uniform(self.MONIKA_THINK_TIME_MIN, self.MONIKA_THINK_TIME_MAX), hard=True)
                card_to_really_use = None
                cards_in_discardpiles_values = []
                for a_discardpile in self.discardpiles:
                    for card_dis in a_discardpile:
                        cards_in_discardpiles_values.append(card_dis.value)
                if len(self.drawpile) <= max(0, 6-len(monika_sorted_cards)) and len(monika_sorted_cards) >= 2: #trickery when player can't draw anymore form the drawpile
                    #use better cards instead when close to the end
                    highest_card_value = monika_sorted_cards[-1].value
                    highest_card_value_count = 0
                    values = []
                    for card in monika_sorted_cards:
                        if card.value not in values:
                            values.append(card.value)
                        if card.value == highest_card_value:
                            highest_card_value_count += 1
                    if len(values) == 2 and (monika_sorted_cards[-1].suit == self.trump_suit or
                    (len(self.player.hand) < len(self.monika.hand) - highest_card_value_count and len(self.player.hand) >= highest_card_value_count)): 
                        player_cards_used = []
                        for card_moni in monika_sorted_cards:
                            if card_moni.value != highest_card_value:
                                continue
                            defended = False
                            for card_player in self.monika.player_cards:
                                if card_player in player_cards_used:
                                    continue
                                if self.can_defend(card_moni, card_player):
                                    player_cards_used.append(card_player)
                                    defended = True
                                    break
                            if not defended and (highest_card_value in cards_in_discardpiles_values or not cards_in_discardpiles_values):
                                card_to_really_use = card_moni
                                break             
                    #do stuff in case player doesn't have cards of a specific suit
                    for card_couldnt_beat in self.monika.player_couldnt_beat: 
                        if card_to_really_use is not None and monika_sorted_cards[-1].suit == self.trump_suit:
                            break
                        for card in monika_sorted_cards:
                            if card_couldnt_beat.suit == card.suit and card_couldnt_beat.value < card.value:
                                if card.value in cards_in_discardpiles_values or not cards_in_discardpiles_values:
                                    card_to_really_use = card
                                    break
                if len(self.player.hand) < len(self.monika.hand) and len(self.drawpile) <= max(0, 6-len(monika_sorted_cards)) and not player_draws:
                    determine_max_trump_value_by = self.player.hand
                else:
                    determine_max_trump_value_by = self.monika.hand
                #find card under normal circumstances
                if persistent._durak_rules.get("cards_amount") == 36:
                    max_trump_value = 16-2*len(determine_max_trump_value_by)
                else:
                    max_trump_value = 17-3*len(determine_max_trump_value_by)
                for card in monika_sorted_cards:
                    if card_to_really_use is not None:
                        break
                    if self.discardpiles_size == 0:
                        card_to_really_use = card
                        break
                    for card_in_discardpile_value in cards_in_discardpiles_values:
                        if card.value == card_in_discardpile_value and (card.suit != self.trump_suit or (card.suit == self.trump_suit and card.value <= max_trump_value)):
                            card_to_really_use = card
                            break
                #end turn
                if not player_draws and (card_to_really_use is None or self.discardpiles_size == 6 or not self.player.hand):
                    if self.winner is None:
                        if self.discardpiles_size > 3:
                            self.say_quip(self.QUIPS_MONIKA_BEATEN[1])
                        elif not bool(renpy.random.randint(0, 2)):
                            self.say_quip(self.QUIPS_MONIKA_BEATEN[0])
                    self.beaten()
                #play card and make player defend
                else:
                    if card_to_really_use is not None:
                        self.attack_card(card_to_really_use, self.monika)
                        self.table.set_faceup(card_to_really_use, True)
                        monika_sorted_cards.remove(card_to_really_use)
                    if not player_draws:
                        self.draw_button_active = True
                        self.table.set_sensitive(True)
                        while not self.player.made_a_move:
                            self.help_button_active = True
                            events = ui.interact(type="minigame")
                            self.help_button_active = False
                            for event in events:
                                if event.type == "drag":
                                    if event.drop_stack == self.player.hand:
                                        x1 = self.player.hand.x - 75
                                        x2 = x1 + len(self.player.hand) * self.CARDS_OFFSET + 150 - self.CARDS_OFFSET
                                        if renpy.get_mouse_pos()[0] >= x1 and renpy.get_mouse_pos()[0] <= x2 and renpy.get_mouse_pos()[1] >= 720-109:
                                            pos = (renpy.get_mouse_pos()[0] - x1) / self.CARDS_OFFSET
                                            self.player.hand.insert(int(pos), event.card)
                                            self.update_cards_positions(self.player)
                                    else:
                                        x, y = renpy.get_mouse_pos()
                                        actual_drop_stack = event.drop_stack
                                        for a_discardpile in self.discardpiles:
                                            if len(a_discardpile) == 1:
                                                x1 = a_discardpile.x - 75
                                                y1 = a_discardpile.y - 109
                                                x2 = a_discardpile.x + 75
                                                y2 = a_discardpile.y + 109
                                                if x > x1 and x < x2 and y > y1 and y < y2:
                                                    actual_drop_stack = a_discardpile
                                                break
                                        if self.can_defend(actual_drop_stack[0], event.card) and len(actual_drop_stack) < 2:
                                            self.play_play_sfx()
                                            actual_drop_stack.append(event.card)
                                            self.player.made_a_move = True
                                            self.update_cards_positions(self.player)
                                            self.draw_button_active = False
                                            if event.card in self.monika.player_cards:
                                                self.monika.player_cards.remove(event.card)
                                            self.did_player_lie(event.card)
                                            if not self.player.hand and not self.drawpile:
                                                self.winner = self.player
                                            if len(self.drawpile) <= max(0, 6-len(monika_sorted_cards)) and event.card.suit == self.trump_suit and actual_drop_stack[0].suit != self.trump_suit:
                                                self.player_couldnt_beat_append(actual_drop_stack[0], False)
                                elif event.type == "hover":
                                    if event.card in self.player.hand:
                                        card = self.table.get_card(event.card)
                                        card.set_offset(0, -35)
                                        card.springback()
                                        stack = card.stack
                                        self.table.stacks.remove(stack)
                                        self.table.stacks.append(stack)
                                    else:
                                        self.table.get_card(self.getmeoutoflooppile[0]).hovered = False
                                        self.table.stacks.remove(self.getmeoutoflooppile)
                                        #draw
                                        if not self.help_needed:
                                            self.table.set_sensitive(False)
                                            self.draw_button_active = False
                                            player_draws = True
                                            if len(self.drawpile) <= max(0, 6-len(monika_sorted_cards)) and card_to_really_use.suit != self.trump_suit:
                                                self.player_couldnt_beat_append(card_to_really_use, True)
                                            self.player.made_a_move = True
                                        else:
                                            self.help(card_to_really_use)
                                elif event.type == "unhover":
                                    if event.card in self.player.hand:
                                        card = self.table.get_card(event.card)
                                        card.set_offset(0, 0)
                                        card.springback()
                        self.player.made_a_move = False
                        self.table.set_sensitive(False)
                    elif card_to_really_use is None:
                        if self.monika.hand or self.drawpile:
                            self.say_quip(self.QUIPS_PLAYER_DRAWS_CARDS[int(round(self.discardpiles_size/2.0-0.6))])
                        self.draw(self.player)

        def player_couldnt_beat_append(self, card_to_add, isDraw):
            player_couldnt_beat_copy = []
            for card in self.monika.player_couldnt_beat:
                player_couldnt_beat_copy.append(card)
            if isDraw:
                for card in player_couldnt_beat_copy:
                    if card.value < card_to_add.value and card.suit == card_to_add.suit:
                        self.monika.player_couldnt_beat.remove(card)
                self.monika.player_couldnt_beat.append(card_to_add)
                self.monika.player_couldnt_beat[:] = self.sort_cards(self.monika.player_couldnt_beat)
            else:
                add = True
                for card in player_couldnt_beat_copy:
                    if card.value < card_to_add.value and card.suit == card_to_add.suit:
                        add = False
                        break
                if add:
                    self.monika.player_couldnt_beat.append(card_to_add)
                    self.monika.player_couldnt_beat[:] = self.sort_cards(self.monika.player_couldnt_beat)

        def end_quips(self):
            renpy.show("monika 1kua")
            if persistent._durak_last_winner == "Monika":
                self.say_quip(("I won~", "Try better next time~", "I'm sure you'll win next time~"))
            elif persistent._durak_last_winner == "Player":
                self.say_quip(("Good job!", "Well played!", "Nice!"))
            elif persistent._durak_last_winner == "Draws":
                if self.winner == self.monika:
                    self.say_quip("Looks like we have a draw~")
                elif self.winner == self.player:
                    self.say_quip("Heh, luckily for you, we play with draws.")
                

        def say_quip(self, what, interact=True, new_context=False):
            if isinstance(what, (list, tuple)):
                quip = renpy.random.choice(what)
            else:
                quip = what
            if new_context:
                renpy.invoke_in_new_context(renpy.say, m, quip, interact=interact)
            else:
                renpy.say(m, quip, interact=interact)

        @classmethod
        def load_sfx(cls):
            nou_ma_dir = os.path.join(config.gamedir, "mod_assets/games/nou/sfx")
            nou_sfx = os.listdir(nou_ma_dir)

            cls.SFX_SHUFFLE = []
            cls.SFX_MOVE = []
            cls.SFX_DRAW = []
            cls.SFX_PLAY = []

            name_to_sfx_list_map = {
                "shuffle": cls.SFX_SHUFFLE,
                "move": cls.SFX_MOVE,
                "slide": cls.SFX_DRAW,
                "place": cls.SFX_PLAY,
                "shove": cls.SFX_PLAY
            }

            for f in nou_sfx:
                if not f.endswith(cls.SFX_EXT):
                    continue

                name, undscr, rest = f.partition("_")
                sfx_list = name_to_sfx_list_map.get(name, None)
                if sfx_list is None:
                    continue

                f = os.path.join(nou_ma_dir, f).replace("\\", "/")
                sfx_list.append(f)

        @staticmethod
        def play_sfx(sfx_files):
            if not sfx_files:
                return
            sfx_file = random.choice(sfx_files)
            renpy.play(sfx_file, channel="sound")

        @classmethod
        def play_shuffle_sfx(cls):
            cls.play_sfx(cls.SFX_SHUFFLE)

        @classmethod
        def play_move_sfx(cls):
            cls.play_sfx(cls.SFX_MOVE)

        @classmethod
        def play_draw_sfx(cls):
            cls.play_sfx(cls.SFX_DRAW)

        @classmethod
        def play_play_sfx(cls):
            cls.play_sfx(cls.SFX_PLAY)

    class DurakPlayer(object):
        def __init__(self):
            self.hand = None
            self.isAI = False
            self.attacker = False
            self.made_a_move = False

    class DurakPlayerAI(object):
        def __init__(self, game):
            self.hand = None
            self.isAI = True
            self.player_cards = []
            self.player_couldnt_beat = []

    class DurakCard(object):
        def __init__(self, value, suit):
            self.value = value
            self.suit = suit