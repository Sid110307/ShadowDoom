#!/usr/bin/env python3
__version__ = "2.0.0"

import base64
import json
import os
import random
import sys
import time
import tkinter
from tkinter import filedialog

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

try:
    import colorama
    from colorama import Fore, Back, Style
    import pygame
except ImportError:
    import subprocess

    try:
        print("Error: Missing dependencies!\nInstalling...")
        subprocess.call([sys.executable, "-m", "pip", "install", "colorama", "pygame"],
                        stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT)
    except ImportError:
        print("Error: Failed to install dependencies!\nPlease install manually!")
        print("Dependencies: colorama, pygame")
        sys.exit()

    import colorama
    from colorama import Fore, Back, Style
    import pygame


class TUI:
    def __init__(self):
        colorama.init()
        self.clear()

    @staticmethod
    def styled_print(message="", fore_color=Fore.RESET, back_color=Back.RESET, style=Style.NORMAL):
        print(f"{style}{fore_color}{back_color}{message}{Style.RESET_ALL}")

    def decorative_header(self, text, width=60, fore_color=Fore.CYAN):
        border = "+" + "-" * (width - 2) + "+"

        self.styled_print(border, fore_color)
        self.styled_print(f"| {text.center(width - 4)} |", fore_color)
        self.styled_print(border, fore_color)

    def section_title(self, text, width=60, fore_color=Fore.GREEN):
        self.styled_print(f"\n {text.center(width)} ", fore_color, style = Style.BRIGHT)
        self.styled_print("-" * width, fore_color)

    def render_menu(self, options, width=60, fore_color=Fore.YELLOW, border_char="|"):
        for i, option in enumerate(options, 1):
            option_text = f"{i}. {option}".center(width - 4)
            self.styled_print(f"{border_char} {option_text} {border_char}", fore_color)

        self.styled_print("+" + "-" * (width - 2) + "+", fore_color)

    def key_value_display(self, items, width=60, fore_color=Fore.YELLOW, border_char="|"):
        for key, value in items.items():
            key_text = f"{key}: {value}".ljust(width - 4)
            self.styled_print(f"{border_char} {key_text} {border_char}", fore_color)
        self.styled_print("+" + "-" * (width - 2) + "+", fore_color)

    def list_display(self, items, center=False, width=60, fore_color=Fore.YELLOW, border_char="|"):
        for item in items:
            item_text = " | ".join([f"{key}: {value}" for key, value in item.items()]).strip()
            item_text = item_text.center(width - 4) if center else item_text.ljust(width - 4)

            self.styled_print(f"{border_char} {item_text} {border_char}", fore_color)
        self.styled_print("+" + "-" * (width - 2) + "+", fore_color)

    def table_display(self, items, width=60, fore_color=Fore.YELLOW, border_char="|"):
        headers = [header for header in items[0] if isinstance(items[0], dict)]
        column_widths = {
            header: max(len(str(header)), *(len(str(row[header])) for row in items if isinstance(row, dict)))
            for header in headers
        }

        total_table_width = sum(column_widths.values()) + len(headers) * 3 + 1

        if total_table_width > width:
            available_width = width - (len(headers) * 3 + 1)
            scaling_factor = available_width / sum(column_widths.values())
            column_widths = {header: max(5, int(width * scaling_factor)) for header, width in column_widths.items()}
        else:
            remaining_space = width - total_table_width
            for header in headers:
                column_widths[header] += remaining_space // len(headers)

        def format_row(row):
            return f"{border_char} " + " | ".join(
                f"{str(row[header])[:column_widths[header]].ljust(column_widths[header])}" for header in headers
            ) + f" {border_char}"

        header_line = format_row({header: header for header in headers})
        border_line = "+" + "+".join("-" * (column_widths[header] + 2) for header in headers) + "+"

        self.styled_print(border_line, fore_color)
        self.styled_print(header_line, fore_color)
        self.styled_print(border_line, fore_color)

        for item in items:
            self.styled_print(border_line if item == "DIVIDER" else format_row(item), fore_color)
        self.styled_print(border_line, fore_color)

    @staticmethod
    def clear():
        return os.system("cls" if os.name == "nt" else "clear")


class Game:
    @staticmethod
    def play_music(file: str, loop: bool = True, stop_previous: bool = False, volume: int = 100):
        if stop_previous:
            pygame.mixer.music.stop()
        pygame.mixer.music.load(f"{os.path.dirname(__file__)}/audio/{file}.wav")
        pygame.mixer.music.set_volume(volume / 100)
        pygame.mixer.music.play(loops = -1 if loop else 0)

        while not pygame.mixer.music.get_busy():
            continue

    def play_attack_music(self):
        self.play_music(f"attack/{random.choice([1, 2, 3, 4, 5, 6])}", False, False)

    def menu(self):
        self.tui.clear()
        self.tui.decorative_header("Main Menu")

        options = ["Begin a New Game", "Exit", "Credits"]
        self.tui.render_menu(options)
        c = input("CHOOSE>> ")

        if c == "1":
            self.new()
        elif c == "2":
            self.leave()
        elif c == "3":
            self.game_credits()
        else:
            self.tui.decorative_header("Invalid Choice!", fore_color = Fore.RED)
            self.menu()

    def leave(self):
        self.tui.clear()

        self.tui.decorative_header("Thanks for Playing!", fore_color = Fore.GREEN, width = 80)
        self.tui.decorative_header("Keep ShadowDooming!", fore_color = Fore.GREEN, width = 80)

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
            self.tui.styled_print(line, Fore.YELLOW)

        time.sleep(3)
        self.tui.styled_print("\n\nBye!", Fore.LIGHTCYAN_EX)
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

        self.stick = False
        self.club = False
        self.spiked_mace = False
        self.fire_axe = False
        self.spear = False
        self.double_axe = False
        self.katana = False
        self.shotgun = False
        self.magic_scythe = False
        self.rusty_sword = False
        self.colt_anaconda = False

    def new(self):
        self.reset_player_state()
        self.tui.decorative_header("Starting a New Game!", fore_color = Fore.GREEN)
        self.tui.styled_print("Your journey begins...", Fore.CYAN)

        time.sleep(2)
        self.home()

    def home(self):
        if not pygame.mixer.music.get_busy():
            self.play_music(f"menu/{random.choice(self.main_menu_music)}")

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
        self.tui.key_value_display(stats)

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

        c = input("CHOOSE>> ")
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
            self.menu()
        else:
            self.tui.decorative_header("Invalid Choice!", fore_color = Fore.RED)
            time.sleep(2)
            self.home()

    def inventory(self):
        self.is_inventory = True
        self.play_music("shop")
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
            "Spear":         (self.spear, 35),
            "Double Axe":    (self.double_axe, 40),
            "Katana":        (self.katana, 50),
            "Shotgun":       (self.shotgun, 70),
            "Magic Scythe":  (self.magic_scythe, 90),
            "Rusty Sword":   (self.rusty_sword, 15),
            "Colt Anaconda": (self.colt_anaconda, 100),
        }

        possession = False
        for weapon, (owned, damage) in weapons.items():
            if owned and self.currentweapon != weapon:
                self.tui.styled_print(f"{weapon} ({damage} Damage)", Fore.YELLOW)
                possession = True

        if not possession:
            self.tui.styled_print("You don't have any Weapons. Buy them in the Shop!", Fore.RED)
            time.sleep(3)
            pygame.mixer.music.stop()

            self.home()
            return

        self.tui.section_title("Equip a Weapon")
        self.tui.styled_print("Press the corresponding key to equip a weapon or type 'Q' to quit:", Fore.CYAN)
        equip_keys = {
            "S": "Stick",
            "C": "Old Club",
            "P": "Spiked Mace",
            "F": "Fire Axe",
            "R": "Spear",
            "D": "Double Axe",
            "K": "Katana",
            "G": "Shotgun",
            "M": "Magic Scythe",
            "T": "Rusty Sword",
            "A": "Colt Anaconda"
        }

        for key, weapon in equip_keys.items():
            if weapons[weapon][0]:
                self.tui.styled_print(f"{key} - {weapon}", Fore.YELLOW)
        c = input("\nCHOOSE>> ").strip().upper()

        if c in equip_keys and weapons[equip_keys[c]][0]:
            selected_weapon = equip_keys[c]
            self.currentweapon = selected_weapon
            self.playerdamage = weapons[selected_weapon][1]

            setattr(self, selected_weapon.lower().replace(" ", "_"), False)
            self.tui.styled_print(f"\nYou have equipped the {selected_weapon}!", Fore.GREEN)

            time.sleep(1)
            self.inventory()
        elif c == "Q":
            pygame.mixer.music.stop()
            self.home()
        else:
            self.tui.decorative_header("Invalid Choice!", fore_color = Fore.RED)
            time.sleep(1)
            self.inventory()

    def shop(self):
        if not pygame.mixer.music.get_busy():
            self.play_music("shop")
        self.money = max(self.money, 0)
        self.tui.clear()

        self.tui.decorative_header("Welcome to the Shop!", width = 100)
        stats = [{
            "Your Money":     f"${self.money}",
            "Health":         f"{self.health} HP / {self.max_health} HP",
            "Current Weapon": self.currentweapon,
            "Weapon Damage":  self.playerdamage
        }]
        self.tui.list_display(stats, center = True, width = 100)

        # if self.money == 0:
        #     self.tui.styled_print("You have no money to spend. Go kill Monsters and earn more!", Fore.RED)
        #     time.sleep(3)
        #     self.home()
        #
        #     return

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
                "name":        "Spear",
                "price":       50,
                "effect":      "+35 Damage",
                "description": "Pierce or stab. The choice is yours.",
                "attr":        "spear"
            },
            6:         {
                "name":        "Double Axe",
                "price":       60,
                "effect":      "+40 Damage",
                "description": "Enough to kill two people at once.",
                "attr":        "double_axe"
            },
            7:         {
                "name":        "Katana",
                "price":       100,
                "effect":      "+50 Damage",
                "description": "Slice them in half!",
                "attr":        "katana"
            },
            8:         {
                "name":        "Shotgun",
                "price":       200,
                "effect":      "+70 Damage",
                "description": "Boom! Headshot!!",
                "attr":        "shotgun"
            },
            9:         {
                "name":        "Magic Scythe",
                "price":       250,
                "effect":      "+90 Damage",
                "description": "You will have power beyond that of a God!",
                "attr":        "magic_scythe"
            },
            "DIVIDER": {},
            10:        {
                "name":        "Healing Pill",
                "price":       5,
                "effect":      "+10 HP",
                "description": "A small boost to your health.",
                "attr":        "health_pill"
            },
            11:        {
                "name":        "Health Potion",
                "price":       20,
                "effect":      "+50 HP",
                "description": "Use this to get back on your feet.",
                "attr":        "health_potion"
            }
        }

        self.tui.section_title("Items for Sale", width = 100)

        display_items = []
        for i, item in items.items():
            if item == {}:
                display_items.append("DIVIDER")
                continue

            display_items.append({
                "ID":          i,
                "Name":        item["name"],
                "Description": item["description"],
                "Price":       f"${item['price']}",
                "Effect":      item["effect"]
            })

        self.tui.table_display(display_items, width = 100)
        self.tui.styled_print("\nType the item number to buy, or 'quit' to go back home.", Fore.CYAN)
        choice = input("CHOOSE>> ").strip()

        if choice.lower() == "quit":
            self.tui.styled_print("Going back home...", Fore.GREEN)
            time.sleep(2)
            pygame.mixer.music.stop()
            self.home()
            return

        if not choice.isdigit() or int(choice) not in items:
            self.tui.styled_print("Please enter a valid number!", Fore.RED)
            time.sleep(2)
            self.shop()
            return

        choice = int(choice)
        item = items[choice]

        if item["attr"] in {"health_pill", "health_potion"}:
            if self.health >= self.max_health:
                self.tui.styled_print("You already have full health!", Fore.RED)
            elif self.money >= item["price"]:
                self.money -= item["price"]

                self.health = min(self.health + (10 if item["attr"] == "health_pill" else 50), self.max_health)
                self.tui.styled_print(f"You replenished your health by {item['effect']}!", Fore.GREEN)
            else:
                self.tui.styled_print("You don't have enough money!", Fore.RED)
        else:
            if getattr(self, item["attr"], False):
                self.tui.styled_print("You already own this item!", Fore.RED)
            elif self.money >= item["price"]:
                self.money -= item["price"]
                self.playerdamage = int(item["effect"].split('+')[1].split()[0])
                self.currentweapon = item["name"]

                setattr(self, item["attr"], True)
                self.tui.styled_print(f"You bought the {item['name']}!", Fore.GREEN)
            else:
                self.tui.styled_print("You don't have enough money!", Fore.RED)

        time.sleep(2)
        self.shop()

    def die(self):
        self.play_music("heartbeat", loop = True, stop_previous = False, volume = 200)
        self.play_music("die", loop = False, stop_previous = False, volume = 50)
        self.money = max(self.money, 0)
        death_phrase = random.choice(self.death_phrases)

        self.tui.clear()
        print(
            " =     =     = = = = =      =       =          = = = = =      = = = = =     = = = = =     = = = = =     ==    ==")
        print(
            "  =   =     =         =     =       =          =         =        =         =             =         =   ==    ==")
        print(
            "    =       =         =     =       =          =         =        =         = = =         =         =   ==    ==")
        print(
            "    =       =         =     =       =          =         =        =         =             =         =           ")
        print(
            "    =        = = = = =       = = = =           = = = = =      = = = = =     = = = = =     = = = = =     ==    ==")
        print()

        self.tui.styled_print(death_phrase, Fore.YELLOW, style = Style.BRIGHT)
        self.tui.section_title("Statistics")
        stats = {
            "Max Health":     f"{self.max_health} HP",
            "Money":          f"${self.money}",
            "Current Weapon": self.currentweapon,
            "Kills":          self.killcount
        }
        self.tui.key_value_display(stats)

        time.sleep(5)
        self.tui.styled_print("But by some magic from a village wizard, you live again!\n", Fore.CYAN)
        self.tui.styled_print("However, you lose all your weapons and money.", Fore.CYAN)

        input("\nPress Enter to continue...")

        self.reset_player_state()
        pygame.mixer.music.stop()
        self.home()

    def pre_battle(self):
        self.tui.clear()
        self.play_music("attack", loop = True, stop_previous = False)
        self.tui.decorative_header("Get Ready to Fight!", fore_color = Fore.RED)
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
            (96, 100, 12, 700, [100, 115, 125, 130, 140], [55, 70, 75, 80, 95]),
        ]

        for start, end, diff, max_hp, health_list, damage_list in difficulty_settings:
            if start <= self.killcount <= end:
                self.difficulty = diff
                self.max_health = max_hp
                base_health = health_list
                base_damage = damage_list
                break

        if self.killcount > 100:
            self.difficulty += 1
            base_health = [h + (i * 2) for i, h in enumerate(base_health)]
            base_damage = [d + (i + 1) for i, d in enumerate(base_damage)]

        base_health = [int(h / 1.5) for h in base_health]
        base_damage = [int(d / 1.5) for d in base_damage]

        self.monster = random.choice(self.monsters_list)
        article = "an" if self.monster[0].lower() in "aeiou" else "a"
        self.tui.styled_print(f"You encounter {article} {self.monster}!", Fore.YELLOW, style = Style.BRIGHT)

        setattr(self, f"monsterhealth{self.difficulty}", base_health[self.difficulty])
        setattr(self, f"monsterdamage{self.difficulty}", base_damage[self.difficulty])

        self.encounter()

    def treasure(self):
        self.tui.clear()
        self.play_music("treasure")
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
            Fore.YELLOW,
        )
        self.tui.styled_print("You open the treasure chest and find...", Fore.CYAN)
        time.sleep(2)

        treasure = random.choice(random.choices(population = self.treasure_list, weights = self.treasure_weights))
        self.tui.styled_print(f"{treasure}!", Fore.GREEN, style = Style.BRIGHT)

        if "Gold" in treasure:
            amount = int(treasure.replace("Gold", "").strip())
            self.money += amount
            self.money = max(self.money, 0)
            self.tui.styled_print(f"Ka-Ching! You found {amount} Gold!", Fore.YELLOW)
        elif treasure == "An old rusty sword":
            self.tui.styled_print("You equip the sword.", Fore.CYAN)
            self.rusty_sword = True
            self.currentweapon = "Rusty Sword"
        elif treasure in {"nothing", "some Dust"}:
            self.tui.styled_print("Damn, just your luck.", Fore.RED)
        elif treasure == "a Mystery Liquid":
            self.tui.styled_print("You found a Mystery Liquid. Drink it?", Fore.CYAN)
            c = input("(y/n) ").lower()
            while c not in ["y", "n"]:
                self.tui.styled_print("Please enter a valid option (y/n).", Fore.RED)
                c = input("(y/n) ").lower()

            if c == "y":
                self.tui.styled_print("You drink the Mystery Liquid...", Fore.YELLOW)
                time.sleep(1)
                random.choice(random.choices(
                    population = [self.mystery_liquid1, self.mystery_liquid2, self.mystery_liquid3,
                                  self.mystery_liquid4], weights = [0.3, 0.25, 0.2, 0.15]))()
            elif c == "n":
                self.tui.styled_print("You decide not to drink the liquid.", Fore.CYAN)
        elif treasure == "a healing potion":
            self.tui.styled_print("You drink the healing potion.", Fore.GREEN)
            self.health += 50
            self.health = min(self.health, self.max_health)
            self.tui.styled_print(f"You now have {self.health} health.", Fore.YELLOW)
        elif treasure == "a Colt Anaconda":
            self.tui.styled_print("Wow, that's rare!", Fore.YELLOW)
            self.tui.styled_print("You equip the Colt Anaconda.", Fore.CYAN)
            self.colt_anaconda = True
            self.currentweapon = "Colt Anaconda"

        pygame.mixer.music.stop()
        time.sleep(2)
        self.home()

    def mystery_liquid1(self):
        self.tui.styled_print("You feel very strong.", Fore.GREEN)
        time.sleep(2)
        self.health += 50
        self.health = min(self.health, self.max_health)

        self.tui.styled_print(f"You now have {self.health} health.", Fore.GREEN)
        time.sleep(1)

    def mystery_liquid2(self):
        self.tui.styled_print("You feel a bit dizzy.", Fore.GREEN)
        time.sleep(2)
        self.health -= 10
        if self.health <= 0:
            self.health = 5

        self.tui.styled_print(f"You now have {self.health} health.", Fore.GREEN)
        time.sleep(1)

    def mystery_liquid3(self):
        self.money = max(self.money, 0)
        self.tui.styled_print("You suddenly vomit some paper.", Fore.GREEN)
        time.sleep(2)
        self.tui.styled_print("Nope, it's cash!", Fore.GREEN)
        self.money += 100

        self.tui.styled_print(f"You now have {self.money} money.", Fore.GREEN)
        time.sleep(1)

    def mystery_liquid4(self):
        self.tui.styled_print("You feel nothing.", Fore.GREEN)
        time.sleep(1)
        self.tui.styled_print("You now feel a bit stronger, but nothing else.", Fore.GREEN)
        self.playerdamage += 10
        self.tui.styled_print("You go back to your village.", Fore.GREEN)

        time.sleep(2)
        self.home()

    def encounter(self, attacked=False):
        monster_health = getattr(self, f"monsterhealth{self.difficulty}")
        monster_damage = getattr(self, f"monsterdamage{self.difficulty}")

        self.tui.clear()
        if attacked:
            self.tui.styled_print(f"\n\n{random.choice(self.attack_phrases)}", Fore.CYAN)

        self.tui.decorative_header("Fight!", fore_color = Fore.RED)
        stats = [
            {
                "You (HP)":    f"{self.health} HP",
                "Money":       f"${self.money}",
                "Your Damage": f"{self.playerdamage}",
            },
            {
                f"{self.monster} (HP)": f"{monster_health} HP",
                "Enemy Damage":         f"{monster_damage}",
            }
        ]
        self.tui.list_display(stats)

        self.tui.section_title("What would you like to do?")
        options = ["Attack", "Retreat back to your village"]
        self.tui.render_menu(options)

        c = input("\nCHOOSE>> ")
        if c == "1":
            self.tui.clear()
            self.attack()
        elif c == "2":
            self.tui.styled_print("\nYou retreat back to your village.", Fore.YELLOW)
            time.sleep(1)
            self.home()
        else:
            self.tui.styled_print("Please enter a valid option.", Fore.RED)
            time.sleep(2)
            self.encounter()

    def attack(self):
        monster_health_attr = f"monsterhealth{self.difficulty}"
        monster_damage_attr = f"monsterdamage{self.difficulty}"

        monster_health = getattr(self, monster_health_attr)
        monster_damage = getattr(self, monster_damage_attr)

        self.play_attack_music()
        self.health -= monster_damage
        monster_health -= self.playerdamage

        if monster_health <= 0:
            setattr(self, monster_health_attr, 0)
            if self.health <= 0:
                self.die()

            self.tui.styled_print(f"\nYou killed the {self.monster}!", Fore.GREEN)
            self.killcount += 1

            reward = int(random.uniform(self.difficulty, self.difficulty * 5)) * 2
            self.money += reward
            self.tui.styled_print(f"You earned ${reward}!", Fore.YELLOW)

            time.sleep(2)
            self.continue_journey()
        elif self.health <= 0:
            self.die()
        else:
            setattr(self, monster_health_attr, monster_health)
            self.encounter(True)

    def continue_journey(self):
        self.tui.clear()
        self.tui.decorative_header("Continue Your Journey?")

        options = ["Yes", "No"]
        self.tui.render_menu(options)

        c = input("\nCHOOSE>> ")
        if c == "1":
            self.tui.styled_print("\nYou continue on your journey.", Fore.GREEN)
            time.sleep(1)
            random.choice(random.choices(population = self.journey_events, weights = self.journey_events_chances))()
        elif c == "2":
            self.tui.styled_print("\nYou go back to your village.", Fore.YELLOW)
            time.sleep(1)
            self.home()
        else:
            self.tui.styled_print("Please enter 1 or 2.", Fore.RED)
            time.sleep(1)
            self.continue_journey()

    def save_game(self):
        self.tui.clear()
        self.tui.decorative_header("Saving Game...", fore_color = Fore.CYAN)

        root = tkinter.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            defaultextension = ".sdoom",
            title = "Save Game As...",
            filetypes = [("ShadowDoom Save File", "*.sdoom")],
        )

        if not file_path:
            self.tui.styled_print("\nGame not saved.", Fore.RED)
            time.sleep(1)
            self.home()
            return

        game_data = {
            "difficulty":     self.difficulty,
            "health":         self.health,
            "money":          self.money,
            "killcount":      self.killcount,
            "current_weapon": self.currentweapon,
            "monsters":       [
                {"health": getattr(self, f"monsterhealth{i}", 0), "damage": getattr(self, f"monsterdamage{i}", 0)}
                for i in range(1, 6)
            ],
        }

        json_data = json.dumps(game_data)
        encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')

        try:
            with open(file_path, "w") as f:
                f.write(encoded_data)
            self.tui.styled_print("\nGame saved successfully!", Fore.GREEN)
        except Exception as e:
            self.tui.styled_print(f"\nFailed to save the game. Error: {e}", Fore.RED)
        finally:
            root.destroy()
            time.sleep(1)
            self.home()

    def load_game(self):
        self.tui.clear()
        self.tui.decorative_header("Loading Game...", fore_color = Fore.CYAN)

        root = tkinter.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title = "Select Save File",
            filetypes = [("ShadowDoom Save Files", "*.sdoom")],
        )

        if not file_path:
            self.tui.styled_print("\nNo file selected.", Fore.RED)
            time.sleep(1)
            self.home()

            return

        try:
            with open(file_path, "r") as f:
                encoded_data = f.read()

            json_data = base64.b64decode(encoded_data.encode('utf-8')).decode('utf-8')
            game_data = json.loads(json_data)

            self.difficulty = game_data["difficulty"]
            self.health = game_data["health"]
            self.money = game_data["money"]
            self.killcount = game_data["killcount"]
            self.currentweapon = game_data["current_weapon"]

            for i, monster in enumerate(game_data["monsters"], start = 1):
                setattr(self, f"monsterhealth{i}", monster["health"])
                setattr(self, f"monsterdamage{i}", monster["damage"])

            self.tui.styled_print("\nGame loaded successfully!", Fore.GREEN)
        except Exception as e:
            self.tui.styled_print(f"\nFailed to load the game. Error: {e}", Fore.RED)
        finally:
            root.destroy()
            time.sleep(1)
            self.home()

    def game_credits(self):
        width = 50

        self.tui.clear()
        self.tui.decorative_header("Credits", width = width, fore_color = Fore.CYAN)

        credits_text = [
            "Story: Siddharth",
            "Programming: Siddharth",
            "Playtesting: Krithik, Aditya",
            "Written in: Python",
            f"Version: {__version__}",
            "This Game was made possible by you.",
            "Keep ShadowDooming!!",
        ]

        border = "#" * width
        padding = "##" + " " * (width - 4) + "##"

        self.tui.styled_print(border, Fore.YELLOW)
        self.tui.styled_print(padding, Fore.YELLOW)
        for line in credits_text:
            content = f"{line.center(width - 4)}"
            self.tui.styled_print(f"##{content}##", Fore.YELLOW)

        self.tui.styled_print(padding, Fore.YELLOW)
        self.tui.styled_print(border, Fore.YELLOW)

        input("\nPress Enter to continue...")
        self.menu()

    def __init__(self, _tui):
        pygame.mixer.init()
        self.tui = _tui

        self.journey_events = [self.pre_battle, self.treasure]
        self.journey_events_chances = [0.7, 0.3]

        self.main_menu_music = [1, 2, 3]
        self.attack_phrases = ["Slash!", "Bang!", "Pow!", "Boom!", "Splat!", "Bish!", "Bash!", "Biff!", "Ouch!", "Ow!",
                               "Whoosh!", "Arghh!", "Paf!", "Slice!", "Wham!", "Bam!"]
        self.death_phrases = ["You failed!", "Game over!", "OOF!!", "Did you get that on camera?", "That was quick.",
                              "Well, you're dead. This place just doesn't seem very safe now, does it?",
                              "NOOOOO!!!!!!!", "You were killed.", "U NEED MORE PRACTICE!", "You're dead."]
        self.monsters_list = ["Ogre", "Orc", "Beast", "Demon", "Giant", "Golem", "Mummy", "Zombie", "Skeleton", "Witch",
                              "Dragon", "Pirate", "Vampire"]
        self.treasure_list = ["some Dust", "nothing", f"{random.randint(1, 200)} Gold", "An old rusty sword",
                              "a Mystery Liquid", "a healing potion", "a Colt Anaconda"]
        self.treasure_weights = [0.25, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05]
        self.reset_player_state()

        if not pygame.mixer.music.get_busy():
            self.play_music(f"menu/{random.choice(self.main_menu_music)}")

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
            f"                     .oyhhhhhhhys+-`       ./shhhyo/.         .+shhhy+:`      .+ss++/`          `/yhhs/.",
            f"\n                                                 Version: {__version__}                                                 \n\n",
        ]
        for line in art_lines:
            self.tui.styled_print(line, Fore.CYAN)

        input("Press Enter to start... ")
        self.menu()


if __name__ == "__main__":
    tui = TUI()

    if sys.version_info < (3, 6):
        tui.styled_print(
            "ShadowDoom requires Python 3.6 or higher. Please update your Python version.",
            Fore.RED
        )
        tui.styled_print("Exiting...", Fore.RED)
        sys.exit(1)

    try:
        Game(tui)
    except KeyboardInterrupt:
        tui.section_title("Game Interrupted!", fore_color = Fore.RED)
        tui.styled_print("Interrupted by Keyboard!", Fore.YELLOW)
        tui.styled_print("Exiting...", Fore.RED)

        try:
            Game.play_music("bye", loop = False, stop_previous = True)
            time.sleep(5)
        except KeyboardInterrupt:
            tui.styled_print("Okay, I'm exiting!! Jeez!", Fore.RED)

        print(f"{Fore.RESET}{Back.RESET}\n")
        sys.exit()
