import random
import time


class Planet:
    def __init__(self, name, resources):
        self.name = name
        self.resources = resources
        self.owner = None
        self.colony = False

    def show_requirements(self):
        sentence = "You need "
        for resource in self.resources:
            sentence += f"\033[1m{self.resources[resource]}\033[0m {resource}, "
        print(sentence + f"in order to establish a colony on {self.name}")


class Player:
    def __init__(self, name):
        self.name = name
        self.resources = {"energy": 0, "minerals": 0, "life_forms": 0}
        self.colonies = []
        self.galactic_points = 0
        weighted_resources = {"energy": 1, "minerals": 0.5, "life_forms": 2}
        self.power = sum(self.resources[resource] * weight for resource, weight in weighted_resources.items())

    def show_resources(self):
        sentence = ""
        for resource in self.resources:
            sentence += f"\033[1m{self.resources[resource]}\033[0m {resource}, "
        return sentence[:-2]


def explore_planet(player, planet):
    resource = random.choice(list(planet.resources.keys()))
    amount = planet.resources[resource]
    player.resources[resource] += amount
    player.power += amount
    print(f"\n\033[1m{player.name}\033[0m explored {planet.name} and found {amount} {resource}.")


def establish_colony(player, planet):
    count = 0
    for resource in planet.resources:
        if player.resources[resource] >= planet.resources[resource]:
            count += 1

    if count >= len(planet.resources):
        player.colonies.append(planet)
        player.galactic_points += 1
        planet.owner = player
        planet.colony = True
        for resource in planet.resources:
            player.resources[resource] -= planet.resources[resource]
            player.power -= planet.resources[resource]
        print(f"\033[1m{player.name}\033[0m established a colony on {planet.name}.")
    else:
        print(f"\033[1m{player.name}\033[0m doesn't have enough resources to establish a colony on {planet.name}.")


def attack_colony(attacker, defender, planet):
    print(f"{attacker.name}'s power: {attacker.power}")
    print(f"{defender.name}'s power: {defender.power}")
    if determine_attack_success(attacker, defender):
        transfer_colony(attacker, defender, planet)
        return f"{attacker.name} successfully took over {planet.name} from {defender.name}."
    else:
        return f"{attacker.name} failed to take over {planet.name} from {defender.name}."


def determine_attack_success(attacker, defender):
    if attacker.power > defender.power:
        return True
    else:
        return False


def transfer_colony(new_owner, old_owner, planet):
    planet.owner = new_owner
    new_owner.colonies.append(planet)
    old_owner.colonies.remove(planet)
    new_owner.galactic_points += 1
    old_owner.galactic_points -= 1


# obtains the amount of players and the name of the player entered from the user. If the number of players are not an
# integer, it asks the user to enter the amount of player again
def get_players(players, names):
    while True:
        try:
            amount = int(input("How many players (1-4)? "))
            if not 0 < amount < 5:
                raise ValueError
            for i in range(amount):
                while True:
                    try:
                        name = input(f"Player {i + 1}, name your civilization: ")
                        if name in names:
                            raise ValueError
                        players.append(Player(name))
                        names.append(name)
                        break
                    except ValueError:
                        print("Name in use. Enter another name.")
            return players
        except ValueError:
            print("Enter a valid number of players.")


def roll_die(player, planets):
    print("Rolling Die:")
    time.sleep(0.75)
    for i in range(1, 4):
        dots = ". " * i
        print(f"\r{dots}", flush=True, end="")
        time.sleep(0.5)
    roll = random.randrange(1, len(planets))
    print(f"\n\033[1m{player.name}\033[0m rolled a {roll}")
    return planets[roll - 1]


def main():
    planets = [Planet("Alderaan", {"energy": 2, "minerals": 1, "life_forms": 3}),
               Planet("Endor", {"energy": 1, "minerals": 3, "life_forms": 2}),
               Planet("Tatooine", {"energy": 3, "minerals": 2, "life_forms": 1}),
               Planet("Naboo", {"energy": 3, "minerals": 2, "life_forms": 1}),
               Planet("Hoth", {"energy": 2, "minerals": 0, "life_forms": 2}),
               Planet("Pluto", {"energy": 3, "minerals": 1, "life_forms": 2}),
               Planet("Mars", {"energy": 1, "minerals": 2, "life_forms": 0}),
               Planet("Nirvana", {"energy": 4, "minerals": 1, "life_forms": 1}),
               Planet("Earth", {"energy": 1, "minerals": 2, "life_forms": 4}),
               Planet("iPhone", {"energy": 4, "minerals": 3, "life_forms": 1})]
    # This code makes python print "Single-player Mode!" when user enters "1" for players and if it isn't 1 then it
    # will print multiplayer
    players = get_players([], [])
    if len(players) == 1:
        print("Single-player Mode!")
        players.append(Player("Bot"))
    else:
        print("Multiplayer Mode!")
    # This while loop asks user if the user wants to run a long or short game. If it's invalid, it makes the user to
    # re-enter option.
    while True:
        turns = input("Long or Short Game?: ").strip().lower()
        if turns == "long":
            turns = 30
            break
        elif turns == "short":
            turns = 10
            break
        print("Enter 'long' or 'short'.")

    for turn in range(1, turns + 1):
        print(f"\n\033[1m----- Turn {turn} -----\033[0m")
        for player in players:
            if player.name != "Bot":
                print(f"\n\033[1m{player.name}\033[0m's turn:")
                print(f"{player.name} has {player.show_resources()}")
                roll_count = 0
                while True:
                    exit_choice = 0
                    roll = input("Enter 'Roll' to roll die: ").strip().lower()
                    if roll == "roll":
                        current_planet = roll_die(player, planets)
                        while True:
                            current_planet.show_requirements()
                            action = input(
                                f"Explore {current_planet.name} or search other planet (Enter 'Explore' or 'Search')?: "
                            ).strip().lower()
                            if action == "explore":
                                explore_planet(player, current_planet)
                                break
                            elif action == "search":
                                if roll_count < 3:
                                    roll_count += 1
                                    exit_choice += 1
                                    break
                                print("No extra rolls allowed.")
                                explore_planet(player, current_planet)
                                break
                            else:
                                print("Enter 'Explore' or 'Search'.")
                        if exit_choice < 1:
                            break
                    else:
                        print("Enter 'Roll'.")

                if current_planet.colony:
                    if current_planet.owner == player:
                        print(f"\033[1m{player.name}\033[0m already owns this planet.")
                    else:
                        print("Already a colony on this planet!")
                        while True:
                            choice = input("Attack or Leave Planet?: ").strip().lower()
                            if choice == "attack":
                                print(attack_colony(player, current_planet.owner, current_planet))
                                break
                            elif choice == "leave":
                                break
                            print("Enter 'Attack' or 'Leave'.")
                else:
                    establish_colony(player, current_planet)
            else:
                print(f"\n\033[1mBot\033[0m's turn:")
                roll_count = 0
                while True:
                    exit_choice = 0
                    current_planet = roll_die(player, planets)
                    while True:
                        action = random.choice(["explore", "search"])
                        if action == "explore":
                            explore_planet(player, current_planet)
                            break
                        elif action == "search":
                            if roll_count < 3:
                                roll_count += 1
                                exit_choice += 1
                                break
                            explore_planet(player, current_planet)
                            break
                    if exit_choice < 1:
                        break

                if current_planet.colony:
                    if current_planet.owner == player:
                        print(f"\033[1mBot\033[0m owns this planet already.")
                    else:
                        print("Already a colony on this planet!")
                        while True:
                            choice = random.choice(["attack", "leave"])
                            if choice == "attack":
                                print(attack_colony(player, current_planet.owner, current_planet))
                                break
                            elif choice == "leave":
                                break
                else:
                    establish_colony(player, current_planet)

        print("\n\033[1m----- Galactic Status -----\033[0m")
        for planet in planets:
            if planet.colony:
                print(f"{planet.name} is owned by \033[1m{planet.owner.name}\033[0m")

    print("\n\033[1m----- Final Results -----\033[0m")
    players_final = []
    for player in players:
        print(f"\033[1m{player.name}\033[0m has {player.galactic_points} Galactic Points.")
        players_final.append([player.galactic_points, player.name])
    players_scores = [players_final[players_final.index(score)][0] for score in players_final]

    highest = max(players_scores)
    highest_indices = [index for index, num in enumerate(players_scores) if num == highest]
    if len(highest_indices) == 1:
        print(f"{players_final[highest_indices[0]][1]} won!")
    else:
        sentence = "Tie between "
        for i in range(len(highest_indices)):
            if i == len(highest_indices) - 1:
                sentence += f"and {players_final[highest_indices[i]][1]}!"
            else:
                sentence += f"{players_final[highest_indices[i]][1]}, "
        print(sentence)


main()
print("Game Finished!")
