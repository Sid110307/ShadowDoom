#!/usr/bin/env python
__version__ = "1.0.0"

import sys
import os
from time import sleep
import tkinter
from tkinter import filedialog
import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

try:
    import colorama
    from colorama import Fore, Back
    import pygame
except ImportError:
    import subprocess
    print("Error: Missing dependencies!\nInstalling...")

    try:
        subprocess.call(["pip", "install", "colorama", "pygame"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        import colorama
        from colorama import Fore, Back
        import pygame
    except:
        print("Error: Failed to install dependencies!\nPlease install manually!")
        print("Dependencies: colorama, pygame")
        sys.exit()


class Game:
    @staticmethod
    def play_music(file: str, loop: bool = True, stop_previous: bool = False, volume: int = 100):
        if stop_previous:
            pygame.mixer.music.stop()
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(volume / 100)
        pygame.mixer.music.play(loops=-1 if loop else 0)
        while not pygame.mixer.music.get_busy():
            continue

    def play_attack_music(self):
        self.play_music(
            f"{os.path.dirname(__file__)}/audio/attack/{random.choice([1, 2, 3, 4, 5, 6])}.wav", False, False)

    def clear(self):
        return os.system("cls" if os.name == "nt" else "clear")

    def menu(self):
        self.clear()
        print("\n+---------------------+")
        print(": 1- Begin a New Game :")
        print(":---------------------:")
        print(": 2- Exit             :")
        print(":---------------------:")
        print(": 3- Credits          :")
        print("+---------------------+\n")

        c = input("CHOOSE>> ")

        if c == "1":
            self.new()
        elif c == "2":
            self.leave()
        elif c == "3":
            self.game_credits()
        else:
            print("Please enter 1, 2, or 3")
            self.menu()

    def leave(self):
        self.clear()
        print("\n                                            Thanks for Playing!                       ")
        print("                                              Keep ShadowDooming!                       ")
        print("\n                                         `o.                                          ")
        print("                 ````````                `osdys++/:-.`                                  ")
        print("             `````..........`              `mmd+hhyssso+:.`                             ")
        print("          `````....-.                       hNmdNMMNmdhyssso/.`                         ")
        print("        ``  `..` `:do   `:       -`         hMmNNdNMMMMMNmhyyhho-`                      ")
        print("      ``  `.`     -N/  .ys       :h`       .NMyNNNhdNNMMMMMNmhshddo-`                   ")
        print("     .`  `.`      sN: `dMh       +Ny       sMMsNMMNhomMMMMMMMm@REMymNNh/`               ")
        print("    -`  `-        dd+ .Nmm/`  ``-dmm      /NMNsMMMMMhyNMMMMMMN/NmhsydNdo.               ")
        print("  ..   -`       `Nhh  /`sNdhhhdNo`/     :NMNohMMMMMd/hMMMMMMMsyMMNmyyhmmo.              ")
        print("   :    :        .Ndm:   yyhMNMyhs     `+NMNy:dMMMMMdodNMMMMMMN/NMMNMMmhhmm+`           ")
        print("   -    :        .Nmhh  `sdhNsNhmo`   .yNNNssmhMMMMMNodMMMMMMMMdoNMMMMMNmyodh:          ")
        print("   .    :        .NdyN:-/oosdodoo+/-`omMNdodMMNNNNNMMm+MMMMNMMMMhhNMMMMMMMmssmo`        ")
        print("   .`   -`       `Nymyd`.mMNmmdNMd-smNNh//mNMNh+--:omN+NNh+/+smNMhmNMNdsshmNNyhh.       ")
        print("    -   `-       `dhmsd+yNMMMMMMMMyNNNdmh/sNd-      .dym+     `/dNmNN:    `:odmhd:      ")
        print("    `-   `.       yhdN+myNMMMMMMMMhNMMMMMyNd`        -dy         +mNy         :hdm/     ")
        print("     `.`  `.`     /h/ddomhMMMMMMMNyNms/+hmN-          h.          `sd`          :dN:    ")
        print("       .`   ..`   `msNNsymdNMMMNddm/    `do           /             ./`          `om-   ")
        print("         ```  `..` odmm:.smdMNh-dN-      /`                                        /d`  ")
        print("           ````` `-:mNN:ysNNmN/ yh                                                  /o  ")
        print("               ```..+NM+ddshm+/``+`                                                  +. ")
        print("                     sNdoNNhsd+`                                                      . ")
        print("                     `yNomNMNyys.                                                       ")
        print("                      `yNoNMMNhos:                                                      ")
        print("                       `ymyNMNhy+o+`                                                    ")
        print("                        `odhNN.`-+ss-                                                   ")
        print("                          :hdNo   .oho`                                                 ")
        print("                           .odN+    -yh/`                                               ")
        print("                             -sms`    .+s:                                              ")
        print("                               .+s-     .++-                                            ")
        print("                                 `-/.     `::`                                          ")
        print("                                   `-.       `                                          ")
        sleep(5)
        print(
            f"\n\n                                         Bye!				       {Fore.RESET}{Back.RESET}")
        sys.exit()

    def new(self):
        self.health = 100
        self.money = 0
        self.playerdamage = 7
        self.killcount = 0
        self.currentweapon = "Bare Hands"
        self.possession = False

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

        self.home()

    def home(self):
        if not pygame.mixer.music.get_busy():
            self.play_music(
                f"{os.path.dirname(__file__)}/audio/menu/mainmenu{random.choice(self.main_menu_music)}.wav")
        self.clear()

        if self.health >= self.max_health:
            self.health = self.max_health
        self.money = max(self.money, 0)

        print("\n  +--------------------------------------+")
        print("  : Welcome to the Village of ShadowDoom :")
        print("  +--------------------------------------+\n")
        print(" +-----------------------------------------+")
        print(" :               Statistics                :")
        print(" +-----------------------------------------+")
        print(f"               Health: {self.health} HP	   ")
        print(f"                Money: ${self.money}	   ")
        print(f"       Current Weapon: {self.currentweapon}")
        print(f"        Weapon Damage: {self.playerdamage} ")
        print(f"                Kills: {self.killcount}	   ")
        print(" +-----------------------------------------+\n")
        print(" +-----------------------------------------+")
        print(" :       What would you like to do?        :")
        print(" :-----------------------------------------:")
        print(" : 1 : Go out of your Village and Fight!   :")
        print(" : 2 : Go to Shop                          :")
        print(" : 3 : View Inventory                      :")
        print(" :-----------------------------------------:")
        print(" : 4 : Save Game                           :")
        print(" : 5 : Load Game                           :")
        print(" :-----------------------------------------:")
        print(" : 6 : Exit to Home Screen                 :")
        print(" +-----------------------------------------+\n")

        c = input("CHOOSE>> ")

        if c == "1":
            self.prebattle()
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
            print("Please enter 1, 2, 3, 4, 5 or 6.")
            sleep(3)
            self.home()

    def inventory(self):
        self.is_inventory = True
        self.play_music(f"{os.path.dirname(__file__)}/audio/shop.wav")
        self.clear()
        print("         +----------------+")
        print("         : Your Inventory :")
        print("         +----------------+\n")
        print(" +---------------------------------+")
        print(f" Current Weapon: {self.currentweapon}	  ")
        print(" +---------------------------------+")
        print("            Other Weapons:		  ")

        if self.stick and self.currentweapon != "Stick":
            print("Stick (5 Damage)")
            self.possession = True

        if self.club and self.currentweapon != "Club":
            print("Old Club (10 Damage)")
            self.possession = True

        if self.spiked_mace and self.currentweapon != "Spiked Mace":
            print("Spiked Mace(15 Damage)")
            self.possession = True

        if self.fire_axe and self.currentweapon != "Fire Axe":
            print("Fire Axe (20 Damage)")
            self.possession = True

        if self.spear and self.currentweapon != "Spear":
            print("Spear (35 Damage)")
            self.possession = True

        if self.double_axe and self.currentweapon != "Double Axe":
            print("Double Axe (40 Damage)")
            self.possession = True

        if self.katana and self.currentweapon != "Katana":
            print("Katana(50 Damage)")
            self.possession = True

        if self.shotgun and self.currentweapon != "Shotgun":
            print("Shotgun (70 Damage)")
            self.possession = True

        if self.magic_scythe and self.currentweapon != "Magic Scythe":
            print("Magic Scythe (90 Damage)")
            self.possession = True

        if self.rusty_sword and self.currentweapon != "Rusty Sword":
            print("Rusty Sword (15 Damage)")
            self.possession = True

        if self.colt_anaconda and self.currentweapon != "Colt Anaconda":
            print("Colt Anaconda (50 Damage)")
            self.possession = True

        if self.possession == False:
            print("You don't have any Weapons. Buy them in the Shop!")
            sleep(3)
            pygame.mixer.music.stop()
            self.home()

        if self.possession:
            print(" +---------------------------------+\n\nPress one of the below keys to equip a weapon, or type 'q' to quit: ")
            if self.stick:
                print("S - Stick")
            if self.club:
                print("C - Old Club")
            if self.spiked_mace:
                print("P - Spiked Mace")
            if self.fire_axe:
                print("F - Fire Axe")
            if self.spear:
                print("R - Spear")
            if self.double_axe:
                print("D - Double Axe")
            if self.katana:
                print("K - Katana")
            if self.shotgun:
                print("G - Shotgun")
            if self.magic_scythe:
                print("M - Magic Scythe")
            if self.rusty_sword:
                print("T - Rusty Sword")
            if self.colt_anaconda:
                print("A - Colt Anaconda")

            c = input("\n\nCHOOSE>> ")

            if c.lower() == "s" and self.stick:
                self.currentweapon = "Stick"
                self.playerdamage = 5
                self.stick = False
                print(
                    f"\n{Fore.GREEN}You have equipped the Stick!{Fore.LIGHTBLUE_EX}")
                sleep(1)
                self.inventory()
            elif c.lower() == "c" and self.club:
                self.currentweapon = "Old Club"
                self.playerdamage = 10
                self.club = False
                print(
                    f"\n{Fore.GREEN}You have equipped the Old Club!{Fore.LIGHTBLUE_EX}")
                sleep(1)
                self.inventory()
            elif c.lower() == "p" and self.spiked_mace:
                self.currentweapon = "Spiked Mace"
                self.playerdamage = 15
                self.spiked_mace = False
                print(
                    f"\n{Fore.GREEN}You have equipped the Spiked Mace!{Fore.LIGHTBLUE_EX}")
                sleep(1)
                self.inventory()
            elif c.lower() == "f" and self.fire_axe:
                self.currentweapon = "Fire Axe"
                self.playerdamage = 20
                self.fire_axe = False
                print(
                    f"\n{Fore.GREEN}You have equipped the Fire Axe!{Fore.LIGHTBLUE_EX}")
                sleep(1)
                self.inventory()
            elif c.lower() == "r" and self.spear:
                self.currentweapon = "Spear"
                self.playerdamage = 35
                self.spear = False
                print(
                    f"\n{Fore.GREEN}You have equipped the Spear!{Fore.LIGHTBLUE_EX}")
                sleep(1)
                self.inventory()
            elif c.lower() == "d" and self.double_axe:
                self.currentweapon = "Double Axe"
                self.playerdamage = 40
                self.double_axe = False
                print(
                    f"\n{Fore.GREEN}You have equipped the Double Axe!{Fore.LIGHTBLUE_EX}")
                sleep(1)
                self.inventory()
            elif c.lower() == "k" and self.katana:
                self.currentweapon = "Katana"
                self.playerdamage = 50
                self.katana = False
                print(
                    f"\n{Fore.GREEN}You have equipped the Katana!{Fore.LIGHTBLUE_EX}")
                sleep(1)
                self.inventory()
            elif c.lower() == "g" and self.shotgun:
                self.currentweapon = "Shotgun"
                self.playerdamage = 70
                self.shotgun = False
                print(
                    f"\n{Fore.GREEN}You have equipped the Shotgun!{Fore.LIGHTBLUE_EX}")
                sleep(1)
                self.inventory()
            elif c.lower() == "m" and self.magic_scythe:
                self.currentweapon = "Magic Scythe"
                self.playerdamage = 90
                self.magic_scythe = False
                print(
                    f"\n{Fore.GREEN}You have equipped the Magic Scythe!{Fore.LIGHTBLUE_EX}")
                sleep(1)
                self.inventory()
            elif c.lower() == "t" and self.rusty_sword:
                self.currentweapon = "Rusty Sword"
                self.playerdamage = 15
                self.rusty_sword = False
                print(
                    f"\n{Fore.GREEN}You have equipped the Rusty Sword!{Fore.LIGHTBLUE_EX}")
                sleep(1)
                self.inventory()
            elif c.lower() == "a" and self.colt_anaconda:
                self.currentweapon = "Colt Anaconda"
                self.playerdamage = 50
                self.colt_anaconda = False
                print(
                    f"\n{Fore.GREEN}You have equipped the Colt Anaconda!{Fore.LIGHTBLUE_EX}")
                sleep(1)
                self.inventory()
            elif "quit" in c.lower():
                pygame.mixer.music.stop()
                self.home()
            else:
                print("\nPlease choose a valid option!")
                sleep(1)
                self.inventory()

    def shop(self):
        if not pygame.mixer.music.get_busy():
            self.play_music(f"{os.path.dirname(__file__)}/audio/shop.wav")
        self.money = max(self.money, 0)
        self.clear()
        print(" +--------------------------------------------------------------------+")
        print(" :              Welcome to the Shop! What would you like?              ")
        print(" :--------------------------------------------------------------------+")
        print(
            f" Your Money: ${self.money}         Tip: Kill monsters to earn more money.  \n")

        if self.money == 0:
            print(
                " You have no money to spend.         Go kill Monsters and earn more!   ")
            sleep(3)
            self.home()
        else:
            print(" +-----------------------------------------------------------------------------------------------------+")
            print(" :                                                                                                     :")
            print(
                " : 1- Stick: Naturally crafted from an Oak Tree.                                [$5]      (10 Damage)  :")
            print(" :                                                                                                     :")
            print(
                " : 2- Old Club: This ol' bird still has a lot of strength in it.               [$10]      (13 Damage)  :")
            print(" :                                                                                                     :")
            print(
                " : 3- Spiked Mace: Ouch!! It Hurts too much!                                   [$20]      (15 Damage)  :")
            print(" :                                                                                                     :")
            print(
                " : 4- Fire Axe: Hit it to ring an alarm inside your enemy.                     [$35]      (20 Damage)  :")
            print(" :                                                                                                     :")
            print(
                " : 5- Spear: Pierce or Stab. The choice is yours.                              [$50]      (35 Damage)  :")
            print(" :                                                                                                     :")
            print(
                " : 6- Double Axe: Enough to kill 2 people at once.                             [$60]      (40 Damage)  :")
            print(" :                                                                                                     :")
            print(
                " : 7- Katana: Slice them in half!                                             [$100]      (50 Damage)  :")
            print(" :                                                                                                     :")
            print(
                " : 8- Shotgun: Boom!                                                          [$200]      (70 Damage)  :")
            print(" :                                                                                                     :")
            print(
                " : 9- Magic Scythe: You will have power beyond that of a God!!                [$250]      (90 Damage)  :")
            print(" :                                                                                                     :")
            print(" :-----------------------------------------------------------------------------------------------------+")
            print(" :                                                                                                     :")
            print(
                " : 10- Healing Pill: A small boost.                                             [$5]      (+10 HP)     :")
            print(" :                                                                                                     :")
            print(
                " : 11- Health Potion: Use this to get back on your feet.                       [$20]      (+50 HP)     :")
            print(" +-----------------------------------------------------------------------------------------------------+")

            c = input("Choose Item or type 'quit' to go back home: ")

            if c == "1":
                if self.stick:
                    print("You already have this item!")
                elif self.money >= 5:
                    self.money -= 5
                    self.playerdamage = 10
                    self.currentweapon = "Stick"
                    self.stick = True

                    print("You bought the Stick!")
                else:
                    print("You don't have enough money to buy the Stick!")

                sleep(2)
                self.shop()
            elif c == "2":
                if self.club:
                    print("You already have this item!")
                elif self.money >= 10:
                    self.money -= 10
                    self.playerdamage = 13
                    self.currentweapon = "Old Club"
                    self.club = True

                    print("You bought the Old Club!")
                else:
                    print("You don't have enough money to buy the Old Club!")

                sleep(2)
                self.shop()
            elif c == "3":
                if self.spiked_mace:
                    print("You already have this item!")
                elif self.money >= 20:
                    self.money -= 20
                    self.playerdamage = 15
                    self.currentweapon = "Spiked Mace"
                    self.spiked_mace = True

                    print("You bought the Spiked Mace!")
                else:
                    print("You don't have enough money to buy the Spiked Mace!")

                sleep(2)
                self.shop()
            elif c == "4":
                if self.fire_axe:
                    print("You already have this item!")
                elif self.money >= 35:
                    self.money -= 35
                    self.playerdamage = 20
                    self.currentweapon = "Fire Axe"
                    self.fire_axe = True

                    print("You bought the Fire Axe!")
                else:
                    print("You don't have enough money to buy the Fire Axe!")

                sleep(2)
                self.shop()
            elif c == "5":
                if self.spear:
                    print("You already have this item!")
                elif self.money >= 50:
                    self.money -= 50
                    self.playerdamage = 35
                    self.currentweapon = "Spear"
                    self.spear = True

                    print("You bought the Spear!")
                else:
                    print("You don't have enough money to buy the Spear!")

                sleep(2)
                self.shop()
            elif c == "6":
                if self.double_axe:
                    print("You already have this item!")
                elif self.money >= 60:
                    self.money -= 60
                    self.playerdamage = 40
                    self.currentweapon = "Double Axe"
                    self.double_axe = True

                    print("You bought the Double Axe!")
                else:
                    print("You don't have enough money to buy the Double Axe!")

                sleep(2)
                self.shop()
            elif c == "7":
                if self.katana:
                    print("You already have this item!")
                elif self.money >= 100:
                    self.money -= 100
                    self.playerdamage = 50
                    self.currentweapon = "Katana"
                    self.katana = True

                    print("You bought the Katana!")
                else:
                    print("You don't have enough money to buy the Katana!")

                sleep(2)
                self.shop()
            elif c == "8":
                if self.shotgun:
                    print("You already have this item!")
                elif self.money >= 200:
                    self.money -= 200
                    self.playerdamage = 70
                    self.currentweapon = "Shotgun"
                    self.shotgun = True

                    print("You bought the Shotgun!")
                else:
                    print("You don't have enough money to buy the Shotgun!")

                sleep(2)
                self.shop()
            elif c == "9":
                if self.magic_scythe:
                    print("You already have this item!")
                elif self.money >= 250:
                    self.money -= 250
                    self.playerdamage = 90
                    self.currentweapon = "Magic Scythe"
                    self.magic_scythe = True

                    print("You bought the Magic Scythe!")
                else:
                    print("You don't have enough money to buy the Magic Scythe!")

                sleep(2)
                self.shop()
            elif c == "10":
                if self.health >= self.max_health:
                    print("You already have full health!")
                elif self.money >= 5:
                    self.money -= 5
                    self.health += 10

                    print("Replenished 10 HP!")
                else:
                    print("You don't have enough money to buy the Healing Pill!")

                sleep(2)
                self.shop()
            elif c == "11":
                if self.health >= self.max_health:
                    print("You already have full health!")
                elif self.money >= 5:
                    self.money -= 20
                    self.health += 50

                    print("Replenished 50 HP!")
                else:
                    print("You don't have enough money to buy the Health Potion!")

                sleep(2)
                self.shop()
            elif "quit" in c.lower():
                print("Going back home...")
                sleep(2)
                pygame.mixer.music.stop()
                self.home()
            else:
                print("Please enter a valid number!")
                sleep(2)
                self.shop()

    def die(self):
        self.play_music(
            f'{os.path.dirname(__file__)}/audio/heartbeat.wav', True, False, 200)
        self.play_music(
            f'{os.path.dirname(__file__)}/audio/die.wav', False, False, 50)
        self.money = max(self.money, 0)
        death_phrase = random.choice(self.death_phrases)
        self.clear()
        print("\n =     =     = = = = =      =       =          = = = = =      = = = = =     = = = = =     = = = = =     ==    ==")
        print("  =   =     =         =     =       =          =         =        =         =             =         =   ==    ==")
        print("   = =      =         =     =       =          =         =        =         = = =         =         =   ==    ==")
        print("    =       =         =     =       =          =         =        =         = = =         =         =   ==    ==")
        print("    =       =         =     =       =          =         =        =         =             =         =   		  ")
        print("    =        = = = = =       = = = =           = = = = =      = = = = =     = = = = =     = = = = =     ==    ==")
        print()
        print(f"					{death_phrase}															         			  \n")
        print(" +-----------------------------------------+")
        print(" :               Statistics                :")
        print(" +-----------------------------------------+")
        print(f"                Money: ${self.money}			  ")
        print(f"       Current Weapon: {self.currentweapon}	  ")
        print(f"                Kills: {self.killcount}		  ")
        print(" +-----------------------------------------+")
        sleep(5)
        print("\nBut by some magic from a village wizard, you live again! But lose all your weapons and money somehow.\n")
        input("Press enter to start a new game...")
        sleep(1)

        self.health = 100
        self.money = 0
        self.playerdamage = 7
        self.currentweapon = "Bare Hands"
        self.possession = False

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

        pygame.mixer.music.stop()
        self.home()

    def prebattle(self):
        self.clear()
        self.play_music(
            f'{os.path.dirname(__file__)}/audio/attack.wav', True, False)
        print("\nGet Ready to Fight!")
        sleep(2)

        self.monsterhealth = 30
        self.monsterhealth2 = 60
        self.monsterhealth3 = 60
        self.monsterhealth4 = 60
        self.monsterhealth5 = 60

        self.monsterdamage = 4
        self.monsterdamage2 = 8
        self.monsterdamage3 = 15
        self.monsterdamage4 = 20
        self.monsterdamage5 = 35

        if self.killcount >= 0 and self.killcount <= 5:
            self.difficulty = 1
            self.monsterhealth = 30
            self.monsterhealth2 = 60
            self.monsterhealth3 = 70
            self.monsterhealth4 = 75
            self.monsterhealth5 = 80

            self.monsterdamage = 4
            self.monsterdamage2 = 8
            self.monsterdamage3 = 15
            self.monsterdamage4 = 20
            self.monsterdamage5 = 35
        elif self.killcount >= 6 and self.killcount <= 10:
            self.difficulty = 2
            self.max_health = 200
            self.monsterhealth = 35
            self.monsterhealth2 = 65
            self.monsterhealth3 = 75
            self.monsterhealth4 = 80
            self.monsterhealth5 = 85

            self.monsterdamage = 5
            self.monsterdamage2 = 10
            self.monsterdamage3 = 15
            self.monsterdamage4 = 20
            self.monsterdamage5 = 35
        elif self.killcount >= 11 and self.killcount <= 16:
            self.difficulty = 3
            self.monsterhealth = 45
            self.monsterhealth2 = 70
            self.monsterhealth3 = 80
            self.monsterhealth4 = 85
            self.monsterhealth5 = 95

            self.monsterdamage = 7
            self.monsterdamage2 = 15
            self.monsterdamage3 = 20
            self.monsterdamage4 = 25
            self.monsterdamage5 = 40
        elif self.killcount >= 17 and self.killcount <= 25:
            self.difficulty = 4
            self.max_health = 300
            self.monsterhealth = 50
            self.monsterhealth2 = 75
            self.monsterhealth3 = 85
            self.monsterhealth4 = 90
            self.monsterhealth5 = 100

            self.monsterdamage = 8
            self.monsterdamage2 = 20
            self.monsterdamage3 = 25
            self.monsterdamage4 = 30
            self.monsterdamage5 = 40
        elif self.killcount >= 26 and self.killcount <= 35:
            self.difficulty = 5
            self.monsterhealth = 55
            self.monsterhealth2 = 80
            self.monsterhealth3 = 90
            self.monsterhealth4 = 95
            self.monsterhealth5 = 105

            self.monsterdamage = 10
            self.monsterdamage2 = 25
            self.monsterdamage3 = 30
            self.monsterdamage4 = 35
            self.monsterdamage5 = 50
        elif self.killcount >= 36 and self.killcount <= 45:
            self.difficulty = 6
            self.max_health = 400
            self.monsterhealth = 60
            self.monsterhealth2 = 85
            self.monsterhealth3 = 95
            self.monsterhealth4 = 100
            self.monsterhealth5 = 110

            self.monsterdamage = 15
            self.monsterdamage2 = 30
            self.monsterdamage3 = 35
            self.monsterdamage4 = 40
            self.monsterdamage5 = 50
        elif self.killcount >= 46 and self.killcount <= 55:
            self.difficulty = 7
            self.monsterhealth = 65
            self.monsterhealth2 = 90
            self.monsterhealth3 = 100
            self.monsterhealth4 = 105
            self.monsterhealth5 = 115

            self.monsterdamage = 20
            self.monsterdamage2 = 35
            self.monsterdamage3 = 40
            self.monsterdamage4 = 45
            self.monsterdamage5 = 60
        elif self.killcount >= 56 and self.killcount <= 65:
            self.difficulty = 8
            self.max_health = 500
            self.monsterhealth = 70
            self.monsterhealth2 = 95
            self.monsterhealth3 = 105
            self.monsterhealth4 = 110
            self.monsterhealth5 = 120

            self.monsterdamage = 25
            self.monsterdamage2 = 40
            self.monsterdamage3 = 45
            self.monsterdamage4 = 50
            self.monsterdamage5 = 65
        elif self.killcount >= 66 and self.killcount <= 75:
            self.difficulty = 9
            self.monsterhealth = 75
            self.monsterhealth2 = 100
            self.monsterhealth3 = 110
            self.monsterhealth4 = 115
            self.monsterhealth5 = 125

            self.monsterdamage = 35
            self.monsterdamage2 = 50
            self.monsterdamage3 = 55
            self.monsterdamage4 = 60
            self.monsterdamage5 = 75
        elif self.killcount >= 76 and self.killcount <= 85:
            self.difficulty = 10
            self.max_health = 600
            self.monsterhealth = 90
            self.monsterhealth2 = 105
            self.monsterhealth3 = 115
            self.monsterhealth4 = 120
            self.monsterhealth5 = 130

            self.monsterdamage = 40
            self.monsterdamage2 = 55
            self.monsterdamage3 = 60
            self.monsterdamage4 = 65
            self.monsterdamage5 = 80
        elif self.killcount >= 86 and self.killcount <= 95:
            self.difficulty = 11
            self.monsterhealth = 95
            self.monsterhealth2 = 110
            self.monsterhealth3 = 120
            self.monsterhealth4 = 125
            self.monsterhealth5 = 135

            self.monsterdamage = 50
            self.monsterdamage2 = 65
            self.monsterdamage3 = 70
            self.monsterdamage4 = 75
            self.monsterdamage5 = 90
        elif self.killcount >= 96 and self.killcount <= 100:
            self.difficulty = 12
            self.max_health = 700
            self.monsterhealth = 100
            self.monsterhealth2 = 115
            self.monsterhealth3 = 125
            self.monsterhealth4 = 130
            self.monsterhealth5 = 140

            self.monsterdamage = 55
            self.monsterdamage2 = 70
            self.monsterdamage3 = 75
            self.monsterdamage4 = 80
            self.monsterdamage5 = 95
        elif self.killcount > 100:
            self.difficulty += 0.1
            self.monsterhealth += 2
            self.monsterhealth2 += 4
            self.monsterhealth3 += 6
            self.monsterhealth4 += 8
            self.monsterhealth5 += 10

            self.monsterdamage += 1
            self.monsterdamage2 += 2
            self.monsterdamage3 += 3
            self.monsterdamage4 += 4
            self.monsterdamage5 += 5

        self.monsterhealth = int(self.monsterhealth / 1.5)
        self.monsterhealth2 = int(self.monsterhealth2 / 1.5)
        self.monsterhealth3 = int(self.monsterhealth3 / 1.5)
        self.monsterhealth4 = int(self.monsterhealth4 / 1.5)
        self.monsterhealth5 = int(self.monsterhealth5 / 1.5)

        self.monsterdamage = int(self.monsterdamage / 1.5)
        self.monsterdamage2 = int(self.monsterdamage2 / 1.5)
        self.monsterdamage3 = int(self.monsterdamage3 / 1.5)
        self.monsterdamage4 = int(self.monsterdamage4 / 1.5)
        self.monsterdamage5 = int(self.monsterdamage5 / 1.5)

        self.monster = random.choice(self.monsters_list)
        print()

        if self.monster[0].lower() in ["A", "E", "I", "O", "U", "a", "e", "i", "o", "u"]:
            print(f"You encounter an {self.monster}!")
        else:
            print(f"You encounter a {self.monster}!")

        random.choice(random.choices(
            population=[self.encounter1, self.encounter2,
                        self.encounter3, self.encounter4, self.encounter5],
            weights=[0.3, 0.25, 0.2, 0.15, 0.1]))()

    def treasure(self):
        self.clear()
        self.play_music(f'{os.path.dirname(__file__)}/audio/treasure.wav')
        print("\nYou found a treasure chest!\n")
        print("                 _.--.          ")
        print("             _.-'_:-'||         ")
        print("         _.-'_.-::::'||         ")
        print("    _.-:'_.-::::::'  ||         ")
        print("  .'`-.-:::::::'     ||         ")
        print(" /.'`;|:::::::'      ||_        ")
        print("||   ||::::::'     _.;._'-._    ")
        print("||   ||:::::'  _.-!oo @.!-._'-. ")
        print("\\'.  ||:::::.-!()oo @!()@.-'_.|")
        print(" '.'-;|:.-'.&$@.& ()$%-'o.'\\U||")
        print("   `>'-.!@%()@'@_%-'_.-o _.|'|| ")
        print("    ||-._'-.@.-'_.-' _.-o  |'|| ")
        print("    ||=[ '-._.-\\U/.-'    o |'||")
        print("    || '-.]=|| |'|      o  |'|| ")
        print("    ||      || |'|        _| '; ")
        print("    ||      || |'|    _.-'_.-'  ")
        print("    |'-._   || |'|_.-'_.-'      ")
        print("     '-._'-.|| |' `_.-'         ")
        print("         '-.||_/.-'             ")
        print("            '-.__.              ")
        print("                                ")
        print("You open the treasure chest and find...", end=" ")

        sleep(2)
        treasure = random.choice(random.choices(
            population=self.treasure_list, weights=self.treasure_weights))
        print(f"{treasure}!")
        if treasure == r"\d* Gold":
            print(
                f"\nKa-Ching! You found {int(treasure.replace('Gold', ''))} Gold!")
            self.money += int(treasure.replace("Gold", ""))
            self.money = max(self.money, 0)
        elif treasure == "An old rusty sword":
            print("You equip the sword.")
            self.rusty_sword = True
            self.weapon = treasure
        elif treasure in {"nothing", "some Dust"}:
            print("Damn, just your luck.")
        elif treasure == "a Mystery Liquid":
            print("Drink the liquid?")

            c = input("(y/n) ")

            while c.lower() not in ["y", "n"]:
                if c.lower() == "y":
                    print("You drink the Mystery Liquid.")
                    sleep(1)
                    random.choice(random.choices(population=[self.mystery_liquid1, self.mystery_liquid2, self.mystery_liquid3,
                                                             self.mystery_liquid4], weights=[0.3, 0.25, 0.2, 0.15]))()
                elif c.lower() == "n":
                    print("You decide to not drink the liquid.")
                else:
                    print("Please enter a valid option.")
        elif treasure == "a healing potion":
            print("You drink the healing potion.")
            self.health += 50
            if self.health >= self.max_health:
                self.health = self.max_health
            print(f"You now have {self.health} health.")
        elif treasure == "a Colt Anaconda":
            print("Wow, that's rare!")
            print("You equip the Colt Anaconda.")
            self.colt_anaconda = True
            self.weapon = treasure

        pygame.mixer.music.stop()
        sleep(2)
        self.home()

    def mystery_liquid1(self):
        print("You feel a bit dizzy.")
        sleep(2)
        self.health -= 10
        if self.health <= 0:
            self.health = 5
        print(f"You now have {self.health} health.")
        sleep(1)

    def mystery_liquid2(self):
        print("You feel very strong.")
        sleep(2)
        self.health += 50
        if self.health >= self.max_health:
            self.health = self.max_health
        print(f"You now have {self.health} health.")
        sleep(1)

    def mystery_liquid3(self):
        self.money = max(self.money, 0)
        print("You suddenly vomit some paper.")
        sleep(2)
        print("Nope, it's cash!")
        self.money += 100
        print(f"You now have {self.money} money.")
        sleep(1)

    def mystery_liquid4(self):
        print("You feel nothing.")
        sleep(1)
        print("You now feel a bit stronger, but nothing else.")
        self.playerdamage += 10
        print("You go back to your village.")
        sleep(2)
        self.home()

    def encounter1(self):
        print(" +---------------------------------------------+")
        print(f"   You: {self.health} HP   Money: ${self.money}")
        print(
            f"   Enemy: {self.monsterhealth} HP     Damage: {self.monsterdamage}")
        print(" +---------------------------------------------+\n")
        print("1 - Attack")
        print("2 - Run back to your village like a coward\n")

        c = input("CHOOSE>> ")

        if c == "1":
            self.clear()
            self.attack1()
        elif c == "2":
            print("\nYou run back to your village like a coward.")
            sleep(1)
            self.home()
        else:
            print("Please enter a valid option.")
            sleep(2)
            self.clear()
            self.encounter1()

    def attack1(self):
        self.play_attack_music()
        self.health -= self.monsterdamage
        self.monsterhealth -= self.playerdamage

        if self.monsterhealth <= 0:
            if self.health <= 0:
                self.die()

            print(f"\nYou killed the {self.monster}!")
            self.killcount += 1
            self.money += int(random.uniform(self.difficulty,
                              self.difficulty * 5)) * 2
            sleep(2)
            self.continue1()
        elif self.health <= 0:
            self.die()
        else:
            print(f"\n\n{random.choice(self.attack_phrases)}")
            self.encounter1()

    def continue1(self):
        self.clear()
        print("Do you want to continue on your journey?\n")
        c = input("1 - Yes\n2 - No\n\nCHOOSE>> ")

        if c == "1":
            print("\nYou continue on your journey.")
            sleep(1)
            random.choice(random.choices(
                population=self.journey_events, weights=self.journey_events_chances))()
        elif c == "2":
            print("\nYou go back to your village like a coward.")
            sleep(1)
            self.home()
        else:
            print("Please enter 1 or 2.")
            sleep(1)
            self.continue1()

    def encounter2(self):
        print(" +---------------------------------------------+")
        print(f"   You: {self.health} HP   Money: ${self.money}")
        print(
            f"   Enemy: {self.monsterhealth2} HP     Damage: {self.monsterdamage2}")
        print(" +---------------------------------------------+\n")
        print("1 - Attack")
        print("2 - Run back to your village like a coward\n")

        c = input("CHOOSE>> ")

        if c == "1":
            self.clear()
            self.attack2()
        elif c == "2":
            print("\nYou run back to your village like a coward.")
            sleep(1)
            self.home()
        else:
            print("Please enter a valid option.")
            sleep(2)
            self.clear()
            self.encounter2()

    def attack2(self):
        self.play_attack_music()
        self.health -= self.monsterdamage2
        self.monsterhealth2 -= self.playerdamage

        if self.monsterhealth2 <= 0:
            if self.health <= 0:
                self.die()

            print(f"\nYou killed the {self.monster}!")
            self.killcount += 1
            self.money += int(random.uniform(self.difficulty,
                              self.difficulty * 5)) * 2
            sleep(2)
            self.continue2()
        elif self.health <= 0:
            self.die()
        else:
            print(f"\n\n{random.choice(self.attack_phrases)}")
            self.encounter2()

    def continue2(self):
        self.clear()
        print("Do you want to continue on your journey?\n")
        c = input("1 - Yes\n2 - No\n\nCHOOSE>> ")

        if c == "1":
            print("\nYou continue on your journey.")
            sleep(1)
            random.choice(random.choices(
                population=self.journey_events, weights=self.journey_events_chances))()
        elif c == "2":
            print("\nYou go back to your village like a coward.")
            sleep(1)
            self.home()
        else:
            print("Please enter 1 or 2.")
            sleep(1)
            self.continue2()

    def encounter3(self):
        print(" +---------------------------------------------+")
        print(f"   You: {self.health} HP   Money: ${self.money}")
        print(
            f"   Enemy: {self.monsterhealth3} HP     Damage: {self.monsterdamage3}")
        print(" +---------------------------------------------+\n")
        print("1 - Attack")
        print("2 - Run back to your village like a coward\n")

        c = input("CHOOSE>> ")

        if c == "1":
            self.clear()
            self.attack3()
        elif c == "2":
            print("\nYou run back to your village like a coward.")
            sleep(1)
            self.home()
        else:
            print("Please enter a valid option.")
            sleep(2)
            self.clear()
            self.encounter3()

    def attack3(self):
        self.play_attack_music()
        self.health -= self.monsterdamage3
        self.monsterhealth3 -= self.playerdamage

        if self.monsterhealth3 <= 0:
            if self.health <= 0:
                self.die()

            print(f"\nYou killed the {self.monster}!")
            self.killcount += 1
            self.money += int(random.uniform(self.difficulty,
                              self.difficulty * 5)) * 2
            sleep(2)
            self.continue3()
        elif self.health <= 0:
            self.die()
        else:
            print(f"\n\n{random.choice(self.attack_phrases)}")
            self.encounter3()

    def continue3(self):
        self.clear()
        print("Do you want to continue on your journey?\n")
        c = input("1 - Yes\n2 - No\n\nCHOOSE>> ")

        if c == "1":
            print("\nYou continue on your journey.")
            sleep(1)
            random.choice(random.choices(
                population=self.journey_events, weights=self.journey_events_chances))()
        elif c == "2":
            print("\nYou go back to your village like a coward.")
            sleep(1)
            self.home()
        else:
            print("Please enter 1 or 2.")
            sleep(1)
            self.continue3()

    def encounter4(self):
        print(" +---------------------------------------------+")
        print(f"   You: {self.health} HP   Money: ${self.money}")
        print(
            f"   Enemy: {self.monsterhealth4} HP     Damage: {self.monsterdamage4}")
        print(" +---------------------------------------------+\n")
        print("1 - Attack")
        print("2 - Run back to your village like a coward\n")

        c = input("CHOOSE>> ")

        if c == "1":
            self.clear()
            self.attack4()
        elif c == "2":
            print("\nYou run back to your village like a coward.")
            sleep(1)
            self.home()
        else:
            print("Please enter a valid option.")
            sleep(2)
            self.clear()
            self.encounter4()

    def attack4(self):
        self.play_attack_music()
        self.health -= self.monsterdamage4
        self.monsterhealth4 -= self.playerdamage

        if self.monsterhealth4 <= 0:
            if self.health <= 0:
                self.die()

            print(f"\nYou killed the {self.monster}!")
            self.killcount += 1
            self.money += int(random.uniform(self.difficulty,
                              self.difficulty * 5)) * 2
            sleep(2)
            self.continue4()
        elif self.health <= 0:
            self.die()
        else:
            print(f"\n\n{random.choice(self.attack_phrases)}")
            self.encounter4()

    def continue4(self):
        self.clear()
        print("Do you want to continue on your journey?\n")
        c = input("1 - Yes\n2 - No\n\nCHOOSE>> ")

        if c == "1":
            print("\nYou continue on your journey.")
            sleep(1)
            random.choice(random.choices(
                population=self.journey_events, weights=self.journey_events_chances))()
        elif c == "2":
            print("\nYou go back to your village like a coward.")
            sleep(1)
            self.home()
        else:
            print("Please enter 1 or 2.")
            sleep(1)
            self.continue4()

    def encounter5(self):
        print(" +---------------------------------------------+")
        print(f"   You: {self.health} HP   Money: ${self.money}")
        print(
            f"   Enemy: {self.monsterhealth5} HP     Damage: {self.monsterdamage5}")
        print(" +---------------------------------------------+\n")
        print("1 - Attack")
        print("2 - Run back to your village like a coward\n")

        c = input("CHOOSE>> ")

        if c == "1":
            self.clear()
            self.attack5()
        elif c == "2":
            print("\nYou run back to your village like a coward.")
            sleep(1)
            self.home()
        else:
            print("Please enter 1 or 2.")
            sleep(1)
            self.encounter5()

    def attack5(self):
        self.play_attack_music()
        self.health -= self.monsterdamage5
        self.monsterhealth5 -= self.playerdamage

        if self.monsterhealth5 <= 0:
            if self.health <= 0:
                self.die()

            print(f"\nYou killed the {self.monster}!")
            self.killcount += 1
            self.money += int(random.uniform(self.difficulty,
                              self.difficulty * 5)) * 2
            sleep(2)
            self.continue5()
        elif self.health <= 0:
            self.die()
        else:
            print(f"\n\n{random.choice(self.attack_phrases)}")
            self.encounter5()

    def continue5(self):
        self.clear()
        print("Do you want to continue on your journey?\n")
        c = input("1 - Yes\n2 - No\n\nCHOOSE>> ")

        if c == "1":
            print("\nYou continue on your journey.")
            sleep(1)
            random.choice(random.choices(
                population=self.journey_events, weights=self.journey_events_chances))()
        elif c == "2":
            print("\nYou go back to your village like a coward.")
            sleep(1)
            self.home()
        else:
            print("Please enter 1 or 2.")
            sleep(1)
            self.continue5()

    def save_game(self):
        self.clear()
        print("\nSaving game...")

        root = tkinter.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".sdoom",
            title="Save game as...",
            filetypes=[("ShadowDoom Save File", "*.sdoom")])

        if file_path == "":
            print("\nGame not saved.")
            sleep(1)
            self.home()

        with open(file_path, "w") as f:
            f.write(f"{self.difficulty}\n{self.health}\n{self.money}\n{self.killcount}\n{self.monsterhealth}\n{self.monsterdamage}\n{self.monsterhealth2}\n{self.monsterdamage2}\n{self.monsterhealth3}\n{self.monsterdamage3}\n{self.monsterhealth4}\n{self.monsterdamage4}\n{self.monsterhealth5}\n{self.monsterdamage5}\n{self.currentweapon}")
        root.destroy()
        print("\nGame saved!")
        sleep(1)
        self.home()

    def load_game(self):
        self.clear()
        print("\nLoading game...")

        root = tkinter.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select save file",
            filetypes=[("ShadowDoom Save files", "*.sdoom")],
        )

        if file_path == "":
            print("\nNo file selected.")
            sleep(1)
            self.home()

        with open(file_path, "r") as f:
            self.difficulty = float(f.readline())
            self.health = int(f.readline())
            self.money = int(f.readline())
            self.killcount = int(f.readline())
            self.monsterhealth = int(f.readline())
            self.monsterdamage = int(f.readline())
            self.monsterhealth2 = int(f.readline())
            self.monsterdamage2 = int(f.readline())
            self.monsterhealth3 = int(f.readline())
            self.monsterdamage3 = int(f.readline())
            self.monsterhealth4 = int(f.readline())
            self.monsterdamage4 = int(f.readline())
            self.monsterhealth5 = int(f.readline())
            self.monsterdamage5 = int(f.readline())
            self.currentweapon = f.readline()

        root.destroy()
        print("\nGame loaded!")
        sleep(1)
        self.home()

    def game_credits(self):
        self.clear()
        print("\n##############################")
        print("########## Credits ###########")
        print("##############################")
        print("##                          ##")
        print("##     Story: Siddharth     ##")
        print("##  Programming: Siddharth  ##")
        print("##   Playtesting: Krithik   ##")
        print("## Written in: Python, Bash ##")
        print(f"##      Version: {__version__}      ##")
        print("##                          ##")
        print("##    This Game was made    ##")
        print("##     possible by you.     ##")
        print("##                          ##")
        print("##   Keep ShadowDooming!!   ##")
        print("##                          ##")
        print("##############################")
        sleep(10)
        self.menu()

    def __init__(self):
        colorama.init()
        pygame.mixer.init()

        self.journey_events = [self.prebattle, self.treasure]
        self.journey_events_chances = [0.7, 0.2]
        self.main_menu_music = [1, 2, 3]

        self.attack_phrases = [
            "Slash!",
            "Bang!",
            "Pow!",
            "Boom!",
            "Splat!",
            "Bish!",
            "Bash!",
            "Biff!",
            "Ouch!",
            "Ow!",
            "Whoosh!",
            "Arghh!",
            "Paf!",
            "Slice!",
            "Wham!",
            "Bam!",
        ]

        self.death_phrases = [
            "You failed!",
            "Game over!",
            "OOF!!",
            "Did you get that on Camera?",
            "That was quick.",
            "Well, you're dead. This place just doesn't seem very safe now, does it?",
            "NOOOOO!!!!!!!",
            "You were killed.",
            "U NEED MORE PRACTICE!",
            "You're dead.",
        ]

        self.monsters_list = [
            "Ogre",
            "Orc",
            "Beast",
            "Demon",
            "Giant",
            "Golem",
            "Mummy",
            "Zombie",
            "Skeleton",
            "Witch",
            "Dragon",
            "Drunkard",
            "Ugly Fat Guy",
        ]

        self.treasure_list = [
            "some Dust",
            "nothing",
            f"{random.randint(1, 200)} Gold",
            "An old rusty sword",
            "a Mystery Liquid",
            "a healing potion",
            "a Colt Anaconda"
        ]

        self.treasure_weights = [
            0.25,
            0.25,
            0.2,
            0.2,
            0.05,
            0.04,
            0.01
        ]

        self.max_health = 100
        self.health = 0
        self.money = 0
        self.playerdamage = 0
        self.killcount = 0
        self.difficulty = 0
        self.currentweapon = ""
        self.possession = False
        self.monster = ""
        self.is_inventory = False

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

        self.monsterhealth = 0
        self.monsterhealth2 = 0
        self.monsterhealth3 = 0
        self.monsterhealth4 = 0
        self.monsterhealth5 = 0

        self.monsterdamage = 0
        self.monsterdamage2 = 0
        self.monsterdamage3 = 0
        self.monsterdamage4 = 0
        self.monsterdamage5 = 0

        if not pygame.mixer.music.get_busy():
            self.play_music(
                f"{os.path.dirname(__file__)}/audio/menu/mainmenu{random.choice(self.main_menu_music)}.wav")

        print(f"\n{Fore.CYAN}{Back.MAGENTA}\n")
        sleep(1)
        self.clear()

        print("\n       .:+sss+:`    `-/ossss/`    `:+++o/.               `-:+oss:    .:+osssssso/-.          ````:+sso:`  `-+sso:`  .:oss+-   `:+ss+.  	")
        print("     `ohy+//shh+` `/yy///ydd/`  `:ydo``/o:`            -+o+:odmh: `-sy+//sdmy++shdh+.      .+o/:sy++hmd+``///odmh+ .+//smmy- `:+/omds`	    ")
        print("    `+mmo`  `--`  :dd/  :hmy-   :hmd-   `             /ho.`.smmo` .yds` .ymd/` `-ommy.   `/hy/`-s+``+mmd. `  -smmy` `  /dmm/`   `/md+.	    ")
        print("     +mmdo-`      `/-` `ymmo.``.omms`               `/d+`  /hmh/  `    .odms-    -ymm/  `odd+`  `` `+mmd.    .ommy.   `smmm/`  `:yh+` 	    ")
        print("    `.+hdmds:`         :dmmhyyyhdmd:          ```  `/dd+///ymms.       .hmm/`    .smm/  :dmy-      `smmo`    `ommy.  .symmm/` `/yy:   	    ")
        print("  ./++o+/sdmdo.       `smms:---ommy`       `:/+o+.`:ddsssshmmh/        +dmy-     -ymh-  odms.     `/mmy.     `ommy``:y+:dmm/`.oy+.    	    ")
        print(" .sd: `` `+dms-       -dmd:`  -ymd+       .sh+````:hd:   `smms.       .hmh:`    .odh:   odmy-    `/hmy.      `omms-os- .dmd//so-      	    ")
        print(" .ymy:..-/ydy:` `-/-  omd/`   /dmd+-:/    -ymy/.-+hy:    .ymms-:/.   .smh/-..-:oyy+.    -ymms:.-/sdy/`       .smmds/`  .dmmho:`       	    ")
        print("  ./shhhys+-`   `:oso+s/.     .+yhyo:`     -oyhhyo:`      :shhs+-  .oyhhhhhhhys+-`       `:oyhhys/-          .oyo:.    -ys+-`         	    ")
        sleep(0.5)
        print("\n                     `.:+osssssso/-.          `` .:oss+-`        `` -/oss/.      `./osso:`        `-/o++o+-` 								")
        print("                     :sy+//sdmy++ohdh+.     `-+o:-yy/+dmd/`    `:oo./do/sdmy:     -o//ommds-     .+ydmy.`:+/. 							    ")
        print("                     hdo` -smd/  `.ommy.   .+hy:`:y/ `ymms.   -ohs.`+s- -hmm+`     ` `sddmm+`  `/sydmm: 									    ")
        print("                     /:. `odmy-    .hmm:` .odh/   `   smms.  -ymy-  ``  -hmm+`       :ds+hmy- .+y+/mmy`									    ")
        print("                         -ymd+`    `smm/` +dms-      .hmm/` .omdo`      /dmh:        sd:.smd/-os:.smm/ 									    ")
        print("                         +dmy-     .hmh- `smmo.      +mms.  :ymd+      .ymd+`       .dy. +dmyys-`:dmd.   									")
        print("                        -ymh/`    .omh:  `smms.    `/mdo.   -ymdo     .sdh/`        +m/` -hmdo. .omms    									")
        print("                       .sdh/-..-:oyh+.    :ymdo-.-/ydy:`    `/dmh+-.-ohho.    .:/` .hy`  `os/`  -hmmo.:/`									")
        print(
            f"                     .oyhhhhhhhys+-`       ./shhhyo/.         .+shhhy+:`      .+ss++/`          `/yhhs/.     Version {__version__} 		\n\n")

        input("Press enter to start... ")
        print(f"{Fore.LIGHTBLUE_EX}{Back.RESET}")
        self.menu()


if __name__ == "__main__":
    if sys.version_info < (3, 6):
        print(f"{Fore.RED}ShadowDoom requires {Fore.RESET}{Fore.BLUE}Python 3.6{Fore.RESET}{Fore.RED} or higher. Please update your Python version.{Fore.RESET}")
        print(f"{Fore.RED}Exiting...{Fore.RESET}")
        sys.exit(1)

    try:
        Game()
    except KeyboardInterrupt:
        print(f"{Fore.RESET}{Back.RESET}")
        print(f"{Fore.RED}Interrupted by Keyboard!")
        print(f"{Fore.RED}Exiting...")
        Game.play_music(
            f'{os.path.dirname(__file__)}/audio/bye.wav', True, False)
        try:
            sleep(5)
        except KeyboardInterrupt:
            print("Okay, I'm exiting!! Jeez!")
        print(f"{Fore.RESET}{Back.RESET}")
        sys.exit()
