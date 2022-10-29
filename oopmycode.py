import random

class Class:
    def __init__(self, name, health, attacklist):
        self.name = name
        self.health = health
        self.attacklist = attacklist


class Enemy:
    def __init__(self, name, health, attacklist):
        self.name = name
        self.health = health
        self.attacklist = attacklist


class Attack:
    def __init__(self, name, base_damage, max_damage, healing, stun, chance, reduce_chance, cooldown, on_cooldown):
        self.name = name
        self.base_damage = base_damage
        self.max_damage = max_damage
        self.healing = healing
        self.stun = stun
        self.chance = chance
        self.reduce_chance = reduce_chance
        self.cooldown = cooldown
        self.on_cooldown = on_cooldown


Punch = Attack("Punch", 50, 100, 0, "no_stun", 80, 0, 0, False)
Stunner = Attack("Stunner", 20, 30, 0, "stun", 70, 0, 0, False)
Bite = Attack("Bite", 30, 40, 0, "no_stun", 60, 0, 0, False)
Scratch = Attack("Scratch", 20, 30, 0, "no_stun", 70, 0, 0, False)
garbage_fling = Attack("Garbage Fling", 5, 10, 0, 0, 80, 20, 2, False)

fighter_attacklist = [Punch, Stunner]
vermen_dreg_attacklist = [Bite, Scratch]
vermen_scrounger_attacklist = [garbage_fling, Bite]

Fighter = Class("Fighter", 500, fighter_attacklist)
vermen_dreg = Enemy("Vermen Dreg", 100, vermen_dreg_attacklist)
vermen_scrounger = Enemy("Vermen Scrounger", 100, vermen_scrounger_attacklist)

enemy_list = [vermen_scrounger]

stun_cooldown = 0
enemy_cooldown = 0

while True:
    print("Choose your class: Fighter (1)")
    choice = input()
    if choice == "1":
        player_class = Fighter
        print("You have chosen:", player_class.name)
        enemy = random.choice(enemy_list)
        print("Your enemy is:", enemy.name)
    else:
        print("Error, invalid input!")
        continue

    while True:
        cooldown_list = []
        print(cooldown_list)
        enemy_stunned = False
        #Player Attack
        print("Your health:", player_class.health)
        print("Enemy health:", enemy.health)
        print("Attacks:", player_class.attacklist[0].name, "(1)", player_class.attacklist[1].name, "(2)")
        choice = input()
        if choice == "1":
                player_attack = player_class.attacklist[0]
        elif choice == "2":
                player_attack = player_class.attacklist[1]
        else:
            print("Please enter a valid number!")
            continue

        diceroll = random.randint(1, 100)
        if diceroll <= player_attack.chance:
            player_damage = random.randint(player_attack.base_damage, player_attack.max_damage)
            if player_damage > 0:
                enemy.health -= player_damage
                print("You hit", enemy.name, "for", player_damage)
            if player_attack.stun == "stun":
                if stun_cooldown > 0:
                    print("The enemy resisted your stun attempt!")
                if stun_cooldown == 0:
                    print("You stunned the enemy.")
                    enemy_stunned = True
                    stun_cooldown = 3
            player_healing = player_attack.healing
            player_class.health += player_healing
            if player_healing > 0:
                print("You healed for", player_healing)
        elif diceroll > player_attack.chance:
            print("You missed!")

        # Enemy Turn
        if enemy_stunned == False:
                enemy_move = random.choice(enemy.attacklist)
                diceroll = random.randint(1, 100)
                if diceroll <= enemy_move.chance:
                    enemy_damage = random.randint(enemy_move.base_damage, enemy_move.max_damage)
                    if enemy_damage > 0:
                        player_class.health -= enemy_damage
                        print(enemy.name, "hit you with", enemy_move.name, "for", enemy_damage)
                    reduce_chance = enemy_move.reduce_chance
                    for Attack in player_class.attacklist:
                        player_class.attacklist[0 - 2].chance -= reduce_chance
                        if player_class.attacklist[0 - 2].chance < 50:
                            player_class.attacklist[0 - 2].chance = 50
                    if reduce_chance > 0:
                        print("Your chance was reduced by", enemy_move.reduce_chance)
                    if enemy_move.cooldown > 0:
                        enemy.attacklist.remove(enemy_move)
                elif diceroll > enemy_move.chance:
                    print("The enemy attack missed!")
        elif enemy_stunned == True:
            print("The enemy was stunned and could not attack.")

        stun_cooldown -= 1
        enemy_cooldown -= 1
        if stun_cooldown < 0:
            stun_cooldown = 0