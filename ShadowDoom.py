#!/usr/bin/env python3
__version__ = "2.3.0"

import base64
import json
import random
import sys
import time
from tkinter import filedialog

try:
    from utils import tui
    from utils import audio

    import pygame
except ImportError:
    import subprocess

    try:
        print("Error: Missing dependencies!\nInstalling...")
        subprocess.call([sys.executable, "-m", "pip", "install", "rich", "pygame"], stdout = subprocess.DEVNULL,
                        stderr = subprocess.STDOUT)
    except ImportError:
        print("Error: Failed to install dependencies!\nPlease install manually!\nDependencies: rich, pygame")
        sys.exit()

    from utils import tui
    from utils import audio

    import pygame


class Game:
    def __init__(self, _tui, _audio_manager):
        self.tui = _tui
        self.audio_manager = _audio_manager

        self.journey_events = [self.pre_battle, self.treasure]
        self.journey_events_chances = [0.75, 0.25]

        self.main_menu_music = [1, 2, 3]
        self.attack_phrases = ["Slash!", "Bang!", "Pow!", "Boom!", "Splat!", "Bish!", "Bash!", "Biff!", "Ouch!", "Ow!",
                               "Whoosh!", "Arghh!", "Paf!", "Slice!", "Wham!", "Bam!"]
        self.monsters_list = ["Ogre", "Orc", "Beast", "Demon", "Giant", "Golem", "Mummy", "Zombie", "Skeleton", "Witch",
                              "Dragon", "Pirate", "Vampire"]
        self.treasure_list = ["some Dust", "nothing", f"${random.randint(1, 150)}", "An old rusty sword",
                              "a Mystery Liquid", "a healing potion", "a Colt Anaconda"]
        self.treasure_weights = [0.25, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05]
        self.reset_player_state()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.leave()

            self.audio_manager.play_audio(f"menu/{random.choice(self.main_menu_music)}", busy_check = True)

            self.tui.clear()
            art_lines = [
                "       .:+sss+:`    `-/ossss/`    `:+++o/.               `-:+oss:    .:+osssssso/-.          ````:+sso:`  `-+sso:`  .:oss+-   `:+ss+.",
                "     `ohy+//shh+` `/yy///ydd/`  `:ydo``/o:`            -+o+:odmh: `-sy+//sdmy++shdh+.      .+o/:sy++hmd+``///odmh+ .+//smmy- `:+/omds`",
                "    `+mmo`  `--`  :dd/  :hmy-   :hmd-   `             /ho.`.smmo` .yds` .ymd/` `-ommy.   `/hy/`-s+``+mmd. `  -smmy` `  /dmm/`   `/md+.",
                "     +mmdo-`      `/-` `ymmo.``.omms`               `/d+`  /hmh/  `    .odms-    -ymm/  `odd+`  `` `+mmd.    .ommy.   `smmm/`  `:yh+`",
                "    `.+hdmds:`         :dmmhyyyhdmd:          ```  `/dd+///ymms.       .hmm/`    .smm/  :dmy-      `smmo`    `ommy.  .symmm/` `/yy:",
                "  ./++o+/sdmdo.       `smms:---ommy`       `:/+o+.`:ddsssshmmh/        +dmy-     -ymh-  odms.     `/mmy.     `ommy``:y+:dmm/`.oy+.",
                " .sd: `` `+dms-       -dmd:`  -ymd+       .sh+````:hd:   `smms.       .hmh:`    .odh:   odmy-    `/hmy.      `omms-os- .dmd//so-",
                " .ymy:..-/ydy:` `-/-  omd/`   /dmd+-:/    -ymy/.-+hy:    .ymms-:/.   .smh/-..-:oyy+.    -ymms:.-/sdy/`       .smmds/`  .dmmho:`",
                "  ./shhhys+-`   `:oso+s/.     .+yhyo:`     -oyhhyo:`      :shhs+-  .oyhhhhhhhys+-`       `:oyhhys/-          .oyo:.    -ys+-`",
                "\n                     `.:+osssssso/-.          `` .:oss+-`        `` -/oss/.      `./osso:`        `-/o++o+-`",
                "                     :sy+//sdmy++ohdh+.     `-+o:-yy/+dmd/`    `:oo./do/sdmy:     -o//ommds-     .+ydmy.`:+/.",
                "                     hdo` -smd/  `.ommy.   .+hy:`:y/ `ymms.   -ohs.`+s- -hmm+`     ` `sddmm+`  `/sydmm:",
                "                     /:. `odmy-    .hmm:` .odh/   `   smms.  -ymy-  ``  -hmm+`       :ds+hmy- .+y+/mmy`",
                "                         -ymd+`    `smm/` +dms-      .hmm/` .omdo`      /dmh:        sd:.smd/-os:.smm/",
                "                         +dmy-     .hmh- `smmo.      +mms.  :ymd+      .ymd+`       .dy. +dmyys-`:dmd.",
                "                        -ymh/`    .omh:  `smms.    `/mdo.   -ymdo     .sdh/`        +m/` -hmdo. .omms",
                "                       .sdh/-..-:oyh+.    :ymdo-.-/ydy:`    `/dmh+-.-ohho.    .:/` .hy`  `os/`  -hmmo.:/`",
                "                     .oyhhhhhhhys+-`       ./shhhyo/.         .+shhhy+:`      .+ss++/`          `/yhhs/.",
                f"\n                                                 Version: {__version__}                                                 \n\n",
            ]
            for line in art_lines:
                self.tui.styled_print(line, fore_color = "cyan")

            self.input("Press Enter to start... ")
            self.menu()

    def menu(self):
        self.tui.clear()
        self.tui.decorative_header("Main Menu", width = 40)

        options = ["Begin a New Game", "Exit", "Credits"]
        self.tui.render_menu(options, width = 40)
        c = self.input("CHOOSE>> ")

        if c == "1":
            self.new()
        elif c == "2":
            self.leave()
        elif c == "3":
            self.game_credits()
        else:
            self.tui.decorative_header("Invalid Choice!", fore_color = "red", width = 40)
            time.sleep(1)
            self.menu()

    def leave(self):
        self.tui.clear()

        self.tui.decorative_header("Thanks for Playing!", fore_color = "green", width = 90)
        self.tui.decorative_header("Keep ShadowDooming!", fore_color = "green", width = 90)

        ascii_art = [
            "                                         `o.                                          ",
            "                 ````````                `osdys++/:-.`                                ",
            "             `````..........`              `mmd+hhyssso+:.`                           ",
            "          `````....-.                       hNmdNMMNmdhyssso/.`                       ",
            "        ``  `..` `:do   `:       -`         hMmNNdNMMMMMNmhyyhho-`                    ",
            "      ``  `.`     -N/  .ys       :h`       .NMyNNNhdNNMMMMMNmhshddo-`                 ",
            "     .`  `.`      sN: `dMh       +Ny       sMMsNMMNhomMMMMMMMm@REMymNNh/`             ",
            "    -`  `-        dd+ .Nmm/`  ``-dmm      /NMNsMMMMMhyNMMMMMMN/NmhsydNdo.             ",
            "  ..   -`       `Nhh  /`sNdhhhdNo`/     :NMNohMMMMMd/hMMMMMMMsyMMNmyyhmmo.            ",
            "   :    :        .Ndm:   yyhMNMyhs     `+NMNy:dMMMMMdodNMMMMMMN/NMMNMMmhhmm+`         ",
            "   -    :        .Nmhh  `sdhNsNhmo`   .yNNNssmhMMMMMNodMMMMMMMMdoNMMMMMNmyodh:        ",
            "   .    :        .NdyN:-/oosdodoo+/-`omMNdodMMNNNNNMMm+MMMMNMMMMhhNMMMMMMMmssmo`      ",
            "   .`   -`       `Nymyd`.mMNmmdNMd-smNNh//mNMNh+--:omN+NNh+/+smNMhmNMNdsshmNNyhh.     ",
            "    -   `-       `dhmsd+yNMMMMMMMMyNNNdmh/sNd-      .dym+     `/dNmNN:    `:odmhd:    ",
            "    `-   `.       yhdN+myNMMMMMMMMhNMMMMMyNd`        -dy         +mNy         :hdm/   ",
            "     `.`  `.`     /h/ddomhMMMMMMMNyNms/+hmN-          h.          `sd`          :dN:  ",
            "       .`   ..`   `msNNsymdNMMMNddm/    `do           /             ./`          `om- ",
            "         ```  `..` odmm:.smdMNh-dN-      /`                                        /d`",
            "           ````` `-:mNN:ysNNmN/ yh                                                  /o",
            "               ```..+NM+ddshm+/``+`                                                  +.",
            "                     sNdoNNhsd+`                                                      .",
            "                     `yNomNMNyys.                                                       ",
            "                      `yNoNMMNhos:                                                      ",
            "                       `ymyNMNhy+o+`                                                    ",
            "                        `odhNN.`-+ss-                                                   ",
            "                          :hdNo   .oho`                                                 ",
            "                           .odN+    -yh/`                                               ",
            "                             -sms`    .+s:                                              ",
            "                               .+s-     .++-                                            ",
            "                                 `-/.     `::`                                          ",
            "                                   `-.       `                                          ",
        ]
        for line in ascii_art:
            self.tui.styled_print(line, "yellow", style = "bold")

        time.sleep(2)
        self.tui.decorative_header("Bye!", fore_color = "cyan", width = 90)
        sys.exit()

    def reset_player_state(self):
        self.health = 100
        self.max_health = 100
        self.money = 0
        self.playerdamage = 7
        self.killcount = 0
        self.currentweapon = "Bare Hands"
        self.possession = False
        self.difficulty = 1
        self.boss = False

        self.stick = False
        self.club = False
        self.spiked_mace = False
        self.fire_axe = False
        self.poison_dagger = False
        self.spear = False
        self.double_axe = False
        self.katana = False
        self.shotgun = False
        self.magic_scythe = False
        self.flamethrower = False
        self.rusty_sword = False
        self.colt_anaconda = False

    def new(self):
        self.reset_player_state()
        self.tui.decorative_header("Starting a New Game!", fore_color = "green", width = 40)
        self.tui.styled_print("Your journey begins...", fore_color = "cyan")

        time.sleep(2)
        self.home()

    def home(self):
        self.audio_manager.play_audio(f"menu/{random.choice(self.main_menu_music)}", busy_check = True)

        self.tui.clear()
        self.health = min(self.health, self.max_health)
        self.money = max(self.money, 0)

        self.tui.decorative_header("Welcome to the Village of ShadowDoom")

        stats = {
            "Health":         f"{self.health} HP / {self.max_health} HP",
            "Money":          f"${self.money}",
            "Current Weapon": self.currentweapon,
            "Weapon Damage":  self.playerdamage,
            "Kills":          self.killcount
        }
        self.tui.section_title("Statistics")
        self.tui.key_value_display(stats, align = True)

        options = [
            "Go out of your Village and Fight!",
            "Go to Shop",
            "View Inventory",
            "Save Game",
            "Load Game",
            "Exit to Home Screen"
        ]
        self.tui.section_title("What would you like to do?")
        self.tui.render_menu(options)

        c = self.input("CHOOSE>> ")
        if c == "1":
            self.pre_battle()
        elif c == "2":
            self.shop()
        elif c == "3":
            self.inventory()
        elif c == "4":
            self.save_game()
        elif c == "5":
            self.load_game()
        elif c == "6":
            c = ""
            while c not in ["y", "n"]:
                c = self.input("Are you sure you want to exit? Any unsaved progress will be lost. (y/n) ").lower()

                if c == "y":
                    self.menu()
                elif c == "n":
                    self.home()
                else:
                    self.tui.decorative_header("Invalid Choice!", fore_color = "red")
        else:
            self.tui.decorative_header("Invalid Choice!", fore_color = "red")
            time.sleep(1)
            self.home()

    def inventory(self):
        self.is_inventory = True
        self.audio_manager.play_audio("shop")
        self.tui.clear()

        self.tui.decorative_header("Your Inventory")
        stats = {"Current Weapon": self.currentweapon}
        self.tui.key_value_display(stats)
        self.tui.section_title("Other Weapons")

        weapons = {
            "Stick":         (self.stick, 5),
            "Old Club":      (self.club, 10),
            "Spiked Mace":   (self.spiked_mace, 15),
            "Fire Axe":      (self.fire_axe, 20),
            "Poison Dagger": (self.poison_dagger, 25, 3, 3),
            "Spear":         (self.spear, 35),
            "Double Axe":    (self.double_axe, 40),
            "Katana":        (self.katana, 50),
            "Shotgun":       (self.shotgun, 70),
            "Magic Scythe":  (self.magic_scythe, 90),
            "Flamethrower":  (self.flamethrower, 80, 5, 3),
            "Rusty Sword":   (self.rusty_sword, 15),
            "Colt Anaconda": (self.colt_anaconda, 100),
        }

        possession = False
        for weapon, values in weapons.items():
            owned, damage, *extra = values
            if owned and self.currentweapon != weapon:
                if extra:
                    extra_dmg, extra_turns = extra
                    self.tui.styled_print(f"{weapon} - {damage} Damage (+{extra_dmg} Damage over {extra_turns} turns)",
                                          fore_color = "yellow")
                else:
                    self.tui.styled_print(f"{weapon} - {damage} Damage", fore_color = "yellow")
                possession = True

        if not possession:
            self.tui.decorative_header("You don't have any Weapons. Buy them in the Shop!", fore_color = "red")
            time.sleep(2)
            self.audio_manager.stop_audio()
            self.home()

            return

        self.tui.section_title("Equip a Weapon")
        self.tui.styled_print("Press the corresponding key to equip a weapon or type '0' to quit:", fore_color = "cyan")
        equip_keys = {
            1:  "Stick",
            2:  "Old Club",
            3:  "Spiked Mace",
            4:  "Fire Axe",
            5:  "Poison Dagger",
            6:  "Spear",
            7:  "Double Axe",
            8:  "Katana",
            9:  "Shotgun",
            10: "Magic Scythe",
            11: "Flamethrower",
            12: "Rusty Sword",
            13: "Colt Anaconda"
        }

        for key, weapon in equip_keys.items():
            if weapons[weapon][0]:
                self.tui.styled_print(f"{key} - {weapon}", fore_color = "yellow")
        c = self.input("\nCHOOSE>> ")

        if c.isdigit() and int(c) in equip_keys and weapons[equip_keys[int(c)]][0]:
            selected_weapon = equip_keys[int(c)]
            self.currentweapon = selected_weapon
            self.playerdamage = weapons[selected_weapon][1]

            self.tui.styled_print(f"\nYou have equipped the {selected_weapon}!", fore_color = "green")
            time.sleep(1)
            self.inventory()
        elif c == "0":
            self.audio_manager.stop_audio()
            self.home()
        else:
            self.tui.decorative_header("Invalid Choice!", fore_color = "red")
            time.sleep(1)
            self.inventory()

    def shop(self):
        self.audio_manager.play_audio("shop", busy_check = True)
        self.money = max(self.money, 0)
        self.tui.clear()

        self.tui.decorative_header("Welcome to the Shop!", width = 120)
        stats = [{
            "Your Money":     f"${self.money}",
            "Health":         f"{self.health} HP / {self.max_health} HP",
            "Current Weapon": self.currentweapon,
            "Weapon Damage":  self.playerdamage
        }]
        self.tui.list_display(stats, center = True, width = 120)
        self.tui.decorative_header("Tip: Keep your health high and kill monsters to earn more money.",
                                   fore_color = "cyan", width = 120)

        items = {
            1:         {
                "name":        "Stick",
                "price":       5,
                "effect":      "+10 Damage",
                "description": "Hand-crafted from an oak tree.",
                "attr":        "stick"
            },
            2:         {
                "name":        "Old Club",
                "price":       10,
                "effect":      "+13 Damage",
                "description": "This ol' bird still packs a punch.",
                "attr":        "club"
            },
            3:         {
                "name":        "Spiked Mace",
                "price":       20,
                "effect":      "+15 Damage",
                "description": "Crush bones with ease.",
                "attr":        "spiked_mace"
            },
            4:         {
                "name":        "Fire Axe",
                "price":       35,
                "effect":      "+20 Damage",
                "description": "Ring an alarm inside your enemy.",
                "attr":        "fire_axe"
            },
            5:         {
                "name":        "Poison Dagger",
                "price":       40,
                "effect":      "+25 Damage (+3 Damage over 3 turns)",
                "description": "Small but deadly. Weakens your enemy over time.",
                "attr":        "poison_dagger"
            },
            6:         {
                "name":        "Spear",
                "price":       50,
                "effect":      "+35 Damage",
                "description": "Pierce or stab. The choice is yours.",
                "attr":        "spear"
            },
            7:         {
                "name":        "Double Axe",
                "price":       60,
                "effect":      "+40 Damage",
                "description": "Enough to kill two people at once.",
                "attr":        "double_axe"
            },
            8:         {
                "name":        "Katana",
                "price":       100,
                "effect":      "+50 Damage",
                "description": "Slice them in half!",
                "attr":        "katana"
            },
            9:         {
                "name":        "Shotgun",
                "price":       200,
                "effect":      "+70 Damage",
                "description": "Boom! Headshot!!",
                "attr":        "shotgun"
            },
            10:        {
                "name":        "Magic Scythe",
                "price":       250,
                "effect":      "+90 Damage",
                "description": "You will have power beyond that of a God!",
                "attr":        "magic_scythe"
            },
            11:        {
                "name":        "Flamethrower",
                "price":       300,
                "effect":      "+80 Damage (+5 Damage over 3 turns)",
                "description": "Set your enemies ablaze! Watch them burn!",
                "attr":        "flamethrower"
            },
            "DIVIDER": {},
            12:        {
                "name":        "Healing Pill",
                "price":       5,
                "effect":      "+10 HP",
                "description": "A small boost to your health.",
                "attr":        "health_pill"
            },
            13:        {
                "name":        "Health Potion",
                "price":       20,
                "effect":      "+50 HP",
                "description": "Use this to get back on your feet.",
                "attr":        "health_potion"
            },
            14:        {
                "name":        "Large Health Potion",
                "price":       40,
                "effect":      "+100 HP",
                "description": "A large dose of health.",
                "attr":        "large_health_potion"
            }
        }

        self.tui.section_title("Items for Sale", width = 120)

        display_items = []
        for i, item in items.items():
            if not item:
                display_items.append("DIVIDER")
                continue

            display_items.append({
                "ID":          i,
                "Name":        item["name"],
                "Description": item["description"],
                "Price":       f"${item['price']}",
                "Effect":      item["effect"]
            })

        self.tui.table_display(display_items, width = 120)
        self.tui.styled_print("\nType the item number to buy, or 'quit' to go back home.", fore_color = "cyan")
        choice = self.input("CHOOSE>> ")

        if choice.lower() == "quit":
            self.tui.styled_print("Going back home...", fore_color = "green")
            time.sleep(2)
            self.audio_manager.stop_audio()
            self.home()

            return

        if not choice.isdigit() or int(choice) not in items:
            self.tui.decorative_header("Invalid Choice!", fore_color = "red", width = 120)
            time.sleep(2)
            self.shop()
            return

        choice = int(choice)
        item = items[choice]

        if item["attr"] in {"health_pill", "health_potion", "large_health_potion"}:
            if self.health >= self.max_health:
                self.tui.styled_print("You already have full health!", fore_color = "red")
            elif self.money >= item["price"]:
                self.money -= item["price"]

                self.health = min(self.health + int(item["effect"].split('+')[1].split()[0]), self.max_health)
                self.tui.styled_print(f"You replenished your health by {item['effect']}!", fore_color = "green")
            else:
                self.tui.styled_print("You don't have enough money!", fore_color = "red")
        else:
            if getattr(self, item["attr"], False):
                self.tui.styled_print("You already own this item!", fore_color = "red")
            elif self.money >= item["price"]:
                self.money -= item["price"]
                self.playerdamage = int(item["effect"].split('+')[1].split()[0])

                setattr(self, item["attr"], True)
                self.tui.styled_print(f"You bought the {item['name']}!", fore_color = "green")
            else:
                self.tui.styled_print("You don't have enough money!", fore_color = "red")

        time.sleep(2)
        self.shop()

    def die(self):
        self.audio_manager.play_audio("heartbeat", loop = True, stop_previous = False, volume = 200)
        self.audio_manager.play_audio("die", loop = False, stop_previous = False, volume = 50)
        self.money = max(self.money, 0)

        self.tui.clear()
        self.tui.decorative_header("You Died!", fore_color = "red")

        self.tui.section_title("Statistics")
        stats = {
            "Max Health":     f"{self.max_health} HP",
            "Money":          f"${self.money}",
            "Current Weapon": self.currentweapon,
            "Kills":          self.killcount
        }
        self.tui.key_value_display(stats, align = True)

        time.sleep(4)
        self.tui.styled_print("But by some magic from a village wizard, you live again!", fore_color = "cyan")
        time.sleep(1)
        self.tui.styled_print("However, you lose all your weapons and money.", fore_color = "cyan")

        self.input("\nPress Enter to continue...")

        self.reset_player_state()
        self.audio_manager.stop_audio()
        self.home()

    def pre_battle(self):
        self.tui.clear()

        if not self.boss and self.killcount > 100 and random.random() < 0.75 and self.difficulty > 10:
            self.boss_battle()
            return

        self.audio_manager.play_audio("attack", loop = True, stop_previous = False)
        self.tui.decorative_header("Get Ready to Fight!", fore_color = "red")
        time.sleep(2)

        base_health = [30, 60, 60, 60, 60]
        base_damage = [4, 8, 15, 20, 35]

        difficulty_settings = [
            # (min kill count, max kill count, difficulty, max health, health list, damage list)
            (0, 5, 1, 100, [30, 60, 70, 75, 80], [4, 8, 15, 20, 35]),
            (6, 10, 2, 200, [35, 65, 75, 80, 85], [5, 10, 15, 20, 35]),
            (11, 16, 3, 200, [45, 70, 80, 85, 95], [7, 15, 20, 25, 40]),
            (17, 25, 4, 300, [50, 75, 85, 90, 100], [8, 20, 25, 30, 40]),
            (26, 35, 5, 300, [55, 80, 90, 95, 105], [10, 25, 30, 35, 50]),
            (36, 45, 6, 400, [60, 85, 95, 100, 110], [15, 30, 35, 40, 50]),
            (46, 55, 7, 400, [65, 90, 100, 105, 115], [20, 35, 40, 45, 60]),
            (56, 65, 8, 500, [70, 95, 105, 110, 120], [25, 40, 45, 50, 65]),
            (66, 75, 9, 500, [75, 100, 110, 115, 125], [35, 50, 55, 60, 75]),
            (76, 85, 10, 600, [90, 105, 115, 120, 130], [40, 55, 60, 65, 80]),
            (86, 95, 11, 600, [95, 110, 120, 125, 135], [50, 65, 70, 75, 90]),
            (96, 105, 12, 700, [100, 115, 125, 130, 140], [55, 70, 75, 80, 95]),
            (106, 115, 13, 700, [105, 120, 130, 135, 145], [60, 75, 80, 85, 100]),
            (116, 125, 14, 800, [110, 125, 135, 140, 150], [65, 80, 85, 90, 105]),
            (126, 135, 15, 800, [115, 130, 140, 145, 155], [70, 85, 90, 95, 110]),
            (136, 145, 16, 900, [120, 135, 145, 150, 160], [75, 90, 95, 100, 115]),
            (146, 155, 17, 900, [125, 140, 150, 155, 165], [80, 95, 100, 105, 120]),
            (156, 165, 18, 1000, [130, 145, 155, 160, 170], [85, 100, 105, 110, 125]),
            (166, 175, 19, 1000, [135, 150, 160, 165, 175], [90, 105, 110, 115, 130]),
            (176, 185, 20, 1100, [140, 155, 165, 170, 180], [95, 110, 115, 120, 135]),
            (186, 195, 21, 1100, [145, 160, 170, 175, 185], [100, 115, 120, 125, 140]),
            (196, 205, 22, 1200, [150, 165, 175, 180, 190], [105, 120, 125, 130, 145]),
            (206, 215, 23, 1200, [155, 170, 180, 185, 195], [110, 125, 130, 135, 150]),
            (216, 225, 24, 1300, [160, 175, 185, 190, 200], [115, 130, 135, 140, 155]),
            (226, 235, 25, 1300, [165, 180, 190, 195, 205], [120, 135, 140, 145, 160]),
        ]

        for start, end, diff, max_hp, health_list, damage_list in difficulty_settings:
            if start <= self.killcount <= end:
                self.difficulty = diff
                self.max_health = max_hp
                base_health.extend(health_list)
                base_damage.extend(damage_list)
                break

        base_health = [h + random.randint(-10, 10) for h in base_health]
        base_damage = [d + random.randint(-3, 3) for d in base_damage]

        self.monster = random.choice(self.monsters_list)
        article = "an" if self.monster[0].lower() in "aeiou" else "a"
        self.tui.styled_print(f"You encounter {article} {self.monster}!", "yellow", style = "bold")

        try:
            setattr(self, f"monsterhealth{self.difficulty}", base_health[self.difficulty - 1])
            setattr(self, f"monsterdamage{self.difficulty}", base_damage[self.difficulty - 1])
        except IndexError:
            setattr(self, f"monsterhealth{self.difficulty}", base_health[-1])
            setattr(self, f"monsterdamage{self.difficulty}", base_damage[-1])

        self.encounter()

    def treasure(self):
        self.tui.clear()
        self.audio_manager.play_audio("treasure", loop = False, stop_previous = False)
        self.tui.decorative_header("You found a treasure chest!")
        self.tui.styled_print(
            """
                 _.--.          
             _.-'_:-'||         
         _.-'_.-::::'||         
        _.-:'_.-::::::'  ||         
      .'`-.-:::::::'     ||         
     /.'`;|:::::::'      ||_        
    ||   ||::::::'     _.;._'-._    
    ||   ||:::::'  _.-!oo @.!-._'-. 
    \\'.  ||:::::.-!()oo @!()@.-'_.|
     '.'-;|:.-'.&$@.& ()$%-'o.'\\U||
       `>'-.!@%()@'@_%-'_.-o _.|'|| 
        ||-._'-.@.-'_.-' _.-o  |'|| 
        ||=[ '-._.-\\U/.-'    o |'|| 
        || '-.]=|| |'|      o  |'|| 
        ||      || |'|        _| '; 
        ||      || |'|    _.-'_.-'  
        |'-._   || |'|_.-'_.-'      
         '-._'-.|| |' `_.-'         
             '-.||_/.-'             
                '-.__.              
            """,
            fore_color = "yellow",
        )
        self.tui.styled_print("You open the treasure chest and find... ", fore_color = "cyan", end = "")
        time.sleep(2)

        treasure = random.choice(random.choices(population = self.treasure_list, weights = self.treasure_weights))
        self.tui.styled_print(f"{treasure}!", fore_color = "green", style = "bold")

        if "$" in treasure:
            amount = int(treasure.replace("$", "").strip())
            self.money += amount
            self.tui.styled_print(f"Ka-Ching! You found ${amount}!", fore_color = "yellow")
        elif treasure == "An old rusty sword":
            self.tui.styled_print("You equip the sword.", fore_color = "cyan")
            self.rusty_sword = True
            self.currentweapon = "Rusty Sword"
            self.playerdamage = 15
        elif treasure in {"nothing", "some Dust"}:
            self.tui.styled_print("Damn, just your luck.", fore_color = "red")
        elif treasure == "a Mystery Liquid":
            c = ""
            while c not in ["y", "n"]:
                c = self.input("You found a Mystery Liquid. Drink it? (y/n) ").lower()

                if c == "y":
                    self.tui.styled_print("You drink the Mystery Liquid...", fore_color = "yellow")
                    time.sleep(1)
                    random.choice(random.choices(
                        population = [self.mystery_liquid1, self.mystery_liquid2, self.mystery_liquid3,
                                      self.mystery_liquid4], weights = [0.3, 0.25, 0.2, 0.15]))()
                elif c == "n":
                    self.tui.styled_print("You decide not to drink the liquid.", fore_color = "cyan")
                else:
                    self.tui.decorative_header("Invalid Choice!", fore_color = "red")
        elif treasure == "a healing potion":
            self.tui.styled_print("You drink the healing potion.", fore_color = "green")
            self.health += 50
            self.health = min(self.health, self.max_health)
            self.tui.styled_print(f"You now have {self.health} health.", fore_color = "yellow")
        elif treasure == "a Colt Anaconda":
            self.tui.styled_print("Wow, that's rare!", fore_color = "yellow")
            self.tui.styled_print("You equip the Colt Anaconda.", fore_color = "cyan")
            self.colt_anaconda = True
            self.currentweapon = "Colt Anaconda"
            self.playerdamage = 100

        self.audio_manager.stop_audio()
        time.sleep(2)
        self.continue_journey()

    def mystery_liquid1(self):
        self.tui.styled_print("You feel very strong.", fore_color = "green")
        time.sleep(2)
        self.health += 50
        self.health = min(self.health, self.max_health)

        self.tui.styled_print(f"You now have {self.health} health.", fore_color = "green")
        time.sleep(1)

    def mystery_liquid2(self):
        self.tui.styled_print("You feel a bit dizzy.", fore_color = "green")
        time.sleep(2)
        self.health -= 10
        if self.health <= 0:
            self.health = 5

        self.tui.styled_print(f"You now have {self.health} health.", fore_color = "green")
        time.sleep(1)

    def mystery_liquid3(self):
        self.money = max(self.money, 0)
        self.tui.styled_print("You suddenly vomit some paper.", fore_color = "green")
        time.sleep(2)
        self.tui.styled_print("Nope, it's cash!", fore_color = "green")
        self.money += 100

        self.tui.styled_print(f"You now have {self.money} money.", fore_color = "green")
        time.sleep(1)

    def mystery_liquid4(self):
        self.tui.styled_print("You feel nothing.", fore_color = "green")
        time.sleep(1)
        self.tui.styled_print("You now feel a bit stronger, but nothing else.", fore_color = "green")
        self.playerdamage += 10
        self.tui.styled_print("You go back to your village.", fore_color = "green")

        time.sleep(2)
        self.home()

    def encounter(self, attacked=False, turns=0, custom_health=None, custom_damage=None):
        monster_health = custom_health if custom_health is not None else getattr(self,
                                                                                 f"monsterhealth{self.difficulty}")
        monster_damage = custom_damage if custom_damage is not None else getattr(self,
                                                                                 f"monsterdamage{self.difficulty}")

        self.tui.clear()
        if attacked:
            self.tui.styled_print(random.choice(self.attack_phrases), fore_color = "cyan")

        self.tui.decorative_header("Fight!", fore_color = "red")
        stats = [
            {
                "You (HP)":    f"{self.health} HP",
                "Money":       f"${self.money}",
                "Your Damage": f"{self.playerdamage}",
            },
            {
                f"{self.monster} (HP)": f"{monster_health} HP",
                "Monster Damage":       f"{monster_damage}",
            }
        ]
        self.tui.list_display(stats, center = True)

        self.tui.section_title("What would you like to do?")
        options = ["Attack", "Retreat back to your village"]
        self.tui.render_menu(options)

        c = self.input("CHOOSE>> ")
        if c == "1":
            self.tui.clear()
            self.attack(turns, custom_health, custom_damage)
        elif c == "2":
            if self.boss:
                self.boss = False

            self.tui.styled_print("You retreat back to your village.", fore_color = "yellow")
            time.sleep(1)
            self.home()
        else:
            self.tui.decorative_header("Invalid Choice!", fore_color = "red")
            time.sleep(1)
            self.encounter()

    def attack(self, turns=0, custom_health=None, custom_damage=None):
        monster_health_attr = f"monsterhealth{self.difficulty}"
        monster_damage_attr = f"monsterdamage{self.difficulty}"

        monster_health = custom_health if custom_health is not None else getattr(self, monster_health_attr)
        monster_damage = custom_damage if custom_damage is not None else getattr(self, monster_damage_attr)

        self.audio_manager.play_audio(f"attack/{random.choice([1, 2, 3, 4, 5, 6])}", loop = False)
        self.health -= monster_damage
        monster_health -= self.playerdamage

        if self.currentweapon == "Poison Dagger" and turns < 3:
            monster_health -= 3
        if self.currentweapon == "Flamethrower" and turns < 3:
            monster_health -= 5

        if monster_health <= 0:
            setattr(self, monster_health_attr, 0)
            if self.health <= 0:
                self.die()

            self.health += monster_damage
            self.tui.styled_print(f"\nYou killed the {self.monster}!", fore_color = "green")
            self.killcount += 1

            if self.boss and self.monster == "Shadow King":
                self.win()
            else:
                reward = int(random.uniform(self.difficulty, self.difficulty * 5)) * 2
                self.money += reward
                self.tui.styled_print(f"You earned ${reward}!", fore_color = "yellow")
                time.sleep(2)

                if random.random() < 0.2 and self.max_health - self.health < 50:
                    heal_amount = random.randint(10, 30)
                    self.health = min(self.health + heal_amount, self.max_health)
                    self.tui.styled_print(f"You found a healing potion! Restored {heal_amount} HP.",
                                          fore_color = "green", style = "bold")
                    time.sleep(2)

                self.continue_journey()
        elif self.health <= 0:
            self.die()
        else:
            setattr(self, monster_health_attr, monster_health)
            self.encounter(True, turns + 1, monster_health, monster_damage)

    def continue_journey(self):
        self.tui.clear()
        self.tui.decorative_header("Continue Your Journey?", width = 40)

        options = ["Yes", "No"]
        self.tui.render_menu(options, width = 40)

        c = self.input("\nCHOOSE>> ")
        if c == "1":
            self.tui.styled_print("\nYou continue on your journey.", fore_color = "green")
            time.sleep(1)
            random.choice(random.choices(population = self.journey_events, weights = self.journey_events_chances))()
        elif c == "2":
            self.tui.styled_print("\nYou go back to your village.", fore_color = "yellow")
            time.sleep(1)
            self.home()
        else:
            self.tui.decorative_header("Invalid Choice!", fore_color = "red", width = 40)
            time.sleep(1)
            self.continue_journey()

    def boss_battle(self):
        self.audio_manager.play_audio("boss", loop = True, stop_previous = False)
        self.tui.decorative_header("You've encountered the Shadow King!", fore_color = "bold red")
        time.sleep(1)
        self.tui.decorative_header("The Shadow King is a formidable opponent. You must defeat him to win the game!",
                                   fore_color = "yellow")
        time.sleep(3)

        self.monster = "Shadow King"
        self.boss = True

        self.encounter(custom_health = 200, custom_damage = 100)

    def win(self):
        self.boss = False

        self.audio_manager.play_audio("win", loop = False, stop_previous = False)
        self.tui.clear()
        self.tui.decorative_header("Congratulations!", fore_color = "green")

        self.tui.decorative_header("You defeated the Shadow King and saved the village from his tyranny!",
                                   fore_color = "cyan")
        self.tui.decorative_header("You are a true hero!", fore_color = "cyan")

        time.sleep(3)
        self.home()

    def save_game(self):
        self.tui.clear()
        self.tui.decorative_header("Saving Game...", fore_color = "cyan")

        file_path = filedialog.asksaveasfilename(
            defaultextension = ".sdoom",
            title = "Save Game As...",
            filetypes = [("ShadowDoom Save File", "*.sdoom")],
        )

        if not file_path:
            self.tui.decorative_header("Game not saved.", fore_color = "red")
            time.sleep(1)
            self.home()

            return

        game_data = {
            "health":         self.health,
            "max_health":     self.max_health,
            "money":          self.money,
            "playerdamage":   self.playerdamage,
            "killcount":      self.killcount,
            "current_weapon": self.currentweapon,
            "difficulty":     self.difficulty,
            "boss":           self.boss,
            "weapons":        {
                "stick":         self.stick,
                "club":          self.club,
                "spiked_mace":   self.spiked_mace,
                "fire_axe":      self.fire_axe,
                "poison_dagger": self.poison_dagger,
                "spear":         self.spear,
                "double_axe":    self.double_axe,
                "katana":        self.katana,
                "shotgun":       self.shotgun,
                "magic_scythe":  self.magic_scythe,
                "flamethrower":  self.flamethrower,
                "rusty_sword":   self.rusty_sword,
                "colt_anaconda": self.colt_anaconda,
            },
            "monsters":       [
                {"health": getattr(self, f"monsterhealth{i}"), "damage": getattr(self, f"monsterdamage{i}")} for i in
                range(1, self.difficulty + 1)
            ]
        }

        json_data = json.dumps(game_data)
        encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')

        try:
            with open(file_path, "w") as f:
                f.write(encoded_data)
            self.tui.styled_print("\nGame saved successfully!", fore_color = "green")
        except Exception as e:
            self.tui.styled_print(f"\nFailed to save the game. Error: {e}", fore_color = "red")
        finally:
            time.sleep(1)
            self.home()

    def load_game(self):
        self.tui.clear()
        self.tui.decorative_header("Loading Game...", fore_color = "cyan")

        file_path = filedialog.askopenfilename(
            title = "Select Save File",
            filetypes = [("ShadowDoom Save Files", "*.sdoom")],
        )

        if not file_path:
            self.tui.decorative_header("No file selected.", fore_color = "red")
            time.sleep(1)
            self.home()

            return

        try:
            with open(file_path, "r") as f:
                encoded_data = f.read()
            json_data = base64.b64decode(encoded_data.encode('utf-8')).decode('utf-8')

            try:
                game_data = json.loads(json_data)
            except json.JSONDecodeError as e:
                raise Exception("Invalid save file.") from e
            if not all(key in game_data for key in
                       ["health", "max_health", "money", "playerdamage", "killcount", "current_weapon", "difficulty",
                        "boss", "weapons", "monsters"]):
                raise Exception("Invalid save file.")

            self.health = game_data["health"]
            self.max_health = game_data["max_health"]
            self.money = game_data["money"]
            self.playerdamage = game_data["playerdamage"]
            self.killcount = game_data["killcount"]
            self.currentweapon = game_data["current_weapon"]
            self.difficulty = game_data["difficulty"]
            self.boss = game_data["boss"]

            for weapon, owned in game_data["weapons"].items():
                setattr(self, weapon, owned)
            for i, monster in enumerate(game_data["monsters"], start = 1):
                setattr(self, f"monsterhealth{i}", monster["health"])
                setattr(self, f"monsterdamage{i}", monster["damage"])

            self.tui.styled_print("\nGame loaded successfully!", fore_color = "green")
        except Exception as e:
            self.tui.styled_print(f"\nFailed to load the game. Error: {e}", fore_color = "red")
        finally:
            time.sleep(1)
            self.home()

    def game_credits(self):
        self.tui.clear()
        self.tui.decorative_header("Credits", width = 50, fore_color = "cyan")

        credits_text = {
            "Programming":                         "Siddharth",
            "Playtesting":                         "Aditya, Krithik",
            "Written in":                          "Python",
            "Version":                             __version__,
            "DIVIDER":                             None,
            "This Game was made possible by you.": None,
            "Keep ShadowDooming!!":                None,
        }
        self.tui.key_value_display(credits_text, align = True, width = 50, fore_color = "yellow")

        self.input("\nPress Enter to continue...")
        self.menu()

    def input(self, prompt=""):
        while True:
            user_input = input(prompt).strip()
            if user_input.lower() == "m":
                self.audio_manager.muted = not self.audio_manager.muted
            else:
                return user_input


if __name__ == "__main__":
    tui = tui.TUI()
    audio_manager = audio.AudioManager()

    if sys.version_info < (3, 6):
        tui.decorative_header(
            "ShadowDoom requires Python 3.6 or higher. Please update your Python version.",
            fore_color = "red"
        )
        tui.styled_print("Exiting...", fore_color = "red")
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == "--mute":
        audio_manager.muted = True

    try:
        Game(tui, audio_manager)
    except KeyboardInterrupt:
        tui.section_title("Game Interrupted!", fore_color = "red")
        tui.styled_print("Interrupted by Keyboard!", fore_color = "yellow")
        tui.styled_print("Exiting...", fore_color = "red")

        try:
            audio_manager.play_audio("bye", loop = False, stop_previous = True)
            time.sleep(3)
        except KeyboardInterrupt:
            tui.styled_print("Okay, I'm exiting!! Jeez!", fore_color = "red")

        sys.exit()
