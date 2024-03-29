import pygame
import time
from random import randint, choice, randrange


# Initialize Pygame
pygame.init()


# Constants
WIDTH, HEIGHT = 900, 600
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH/4, HEIGHT/8
FPS = 60
PLANET_RADIUS = 50  # 10-75
PLANET_COUNT = 20  # 1-20
PLAYER_COUNT = 4  # 1-4


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (75, 68, 83)
GREY = (176, 168, 185)
PLAYER_COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
PLANET_COLORS = [(randint(0, 255), randint(0, 255), randint(0, 255)) for i in range(PLANET_COUNT)]


# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Quest")


# Load starry background image
background_image = pygame.transform.scale(pygame.image.load("space_background.jpg"), (WIDTH, HEIGHT))


# Planet class
class Planet(pygame.sprite.Sprite):
    def __init__(self, name, x, y, color):
        super().__init__()
        self.name = name
        self.resources = {"Energy": randrange(0, 6), "Minerals": randrange(0, 6), "Life Forms": randrange(0, 6)}
        self.owner = None
        self.colony = False
        self.image = pygame.Surface((PLANET_RADIUS * 2, PLANET_RADIUS * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        pygame.draw.circle(self.image, color, (PLANET_RADIUS, PLANET_RADIUS), PLANET_RADIUS)


# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.resources = {"Energy": 0, "Minerals": 0, "Life Forms": 0}
        self.colonies = []
        self.galactic_points = 0
        weighted_resources = {"Energy": 1, "Minerals": 0.5, "Life Forms": 2}
        self.power = sum(self.resources[resource] * weight for resource, weight in weighted_resources.items())
        
    # This shows the resources in bold
    def show_resources(self):
        sentence = ""
        for resource in self.resources:
            sentence += f"\033[1m{self.resources[resource]}\033[0m {resource}, "
        return sentence[:-2]


# This makes the text 
def draw_text(text, color, x, y, font_size=24, label=False):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    if label:
        screen.blit(text_surface, (x, y))
    else:
        screen.blit(text_surface, text_surface.get_rect(center=(x, y)))


# This function creates a buttom to choose single-player or multiplayer
def create_button(x, y, text, color):
    button = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, color, button)
    draw_text(text, BLACK, x + BUTTON_WIDTH / 2, y + BUTTON_HEIGHT / 2)
    return button


# This makes the user roll the die gies a random number, and prints the number user has rolled
def roll_die(player, max_roll):
    roll = randrange(0, max_roll + 1)
    print("Rolling Die:")
    time.sleep(0.75)
    for i in range(1, 4):
        dots = ". " * i
        print(f"\r{dots}", flush=True, end="")
        time.sleep(0.5)
    print(f"\n\033[1m{player.name}\033[0m rolled a {roll}")
    return roll


#This function lets the user explore the planet based on the number they rolled.
def explore_planet(player, planet):
    resource = choice(list(planet.resources.keys()))
    try:
        amount = roll_die(player, planet.resources[resource])
        player.resources[resource] += amount
        player.power += amount
        
        # Prints how many resources were found on the planet
        if amount:
            print(f"\n\033[1m{player.name}\033[0m explored {planet.name} and found {amount} {resource}.")
        else:
            print(f"\n\033[1m{player.name}\033[0m explored {planet.name} but found no {resource}.")
    except ValueError:
        print(f"\n\033[1m{player.name}\033[0m explored {planet.name} but found no {resource}.")


# Checks if the player has sufficient resources to establish a colony on a planet.
def establish_colony(player, planet):
    count = 0
    for resource in planet.resources:
        if player.resources[resource] >= planet.resources[resource]:
            count += 1
            
    #This if statement checks to see if a user establiished a colony on a planet using the resources.
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


# Simulates an attack on a colony between two players.
def attack_colony(attacker, defender, planet):
    print(f"{attacker.name}'s power: {attacker.power}")
    print(f"{defender.name}'s power: {defender.power}")
    if determine_attack_success(attacker, defender):
        transfer_colony(attacker, defender, planet)
        return f"{attacker.name} successfully took over {planet.name} from {defender.name}."
    else:
        return f"{attacker.name} failed to take over {planet.name} from {defender.name}."


# This function checks if the user's attacks was successful 
def determine_attack_success(attacker, defender):
    if attacker.power > defender.power:
        return True
    else:
        return False


# This helps to transfer colony from a old owner to a new owner, making them lose points for the old owner and gain points for the new owner
def transfer_colony(new_owner, old_owner, planet):
    planet.owner = new_owner
    new_owner.colonies.append(planet)
    old_owner.colonies.remove(planet)
    new_owner.galactic_points += 1
    old_owner.galactic_points -= 1


# This makes buttons for the user to choose to choose between an option single_player or multiplayer
def get_players_amount():
    screen.fill(PURPLE)
    title = draw_text("GALACTIC QUEST", GREY, WIDTH / 2, HEIGHT / 6, 80)
    singleplayer = create_button(WIDTH / 2 - BUTTON_WIDTH / 2, HEIGHT / 3, "Single-Player", GREY)
    multiplayer = create_button(WIDTH / 2 - BUTTON_WIDTH / 2, HEIGHT / 2, "Multi-Player", GREY)
    
    # This while loop recieves the user's choice between single or multi player
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if singleplayer.collidepoint(x, y):
                    return 1  # Return 1 for single-player
                elif multiplayer.collidepoint(x, y):
                    pygame.display.flip()
                    return get_multiplayer()  # Return the number of players for multiplayer
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in (singleplayer, multiplayer):
                if button.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, WHITE, button, 2)  # Draw a border around the button
                else:
                    pygame.draw.rect(screen, GREY, button, 2)
                    
        pygame.display.flip()


# Function to ask the user how many players for multiplayer
def get_multiplayer():
    player_buttons = []
    screen.fill(PURPLE)
    title = draw_text("GALACTIC QUEST", GREY, WIDTH / 2, HEIGHT / 9, 80)
    for i in range(1, 4):
        button = create_button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT / 5 * i, f"{i + 1} Player Mode", GREY)
        player_buttons.append(button)
        
    # Game loop for handling user input and button interactions in a Pygame environment.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i, button in enumerate(player_buttons):
                    if button.collidepoint(x, y):
                        return i + 2  # Return the selected number of players
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in player_buttons:
                if button.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, WHITE, button, 2)  # Draw a border around the button
                else:
                    pygame.draw.rect(screen, GREY, button, 2)
                    
        pygame.display.flip()


# Displays the end screen with the winner's name.
def end_screen(winner):
    screen.fill(PURPLE)
    title = draw_text("GAME OVER!", GREY, WIDTH / 2, HEIGHT / 3, 100)
    subtitle = draw_text(f"{winner}", GREY, WIDTH / 2, HEIGHT / 2, 60)
    print(winner)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        pygame.display.flip()

# Checks and displays the final results to determine the winner among the players.
def check_winner(players):
    print("\n\033[1m----- Final Results -----\033[0m")
    players_final = []
    # This for loop shows the amount of points user has got during the game 
    for player in players:
        print(f"\033[1m{player.name}\033[0m has {player.galactic_points} Galactic Points.")
        players_final.append([player.galactic_points, player.name])
    players_scores = [players_final[players_final.index(score)][0] for score in players_final]
    highest = max(players_scores)  # This indicates the user with the highest score
    highest_indices = [index for index, num in enumerate(players_scores) if num == highest]
    
    # This if statement prints the winner with the highest point or if they have the same score it makes the sentence print "Tie between"
    if len(highest_indices) == 1:
        print(f"{players_final[highest_indices[0]][1]} won!")
    else:
        sentence = "Tie between "
        
        # This for loop  Constructs a sentence to announce the winner(s) based on their final standings.
        for i in range(len(highest_indices)):
            if i == len(highest_indices) - 1:
                sentence += f"and {players_final[highest_indices[i]][1]}!"
            else:
                sentence += f"{players_final[highest_indices[i]][1]}, "
        return sentence


# Uses a list of planet names for sprite creation.
def main():
    # Create planet sprites with no overlapping planets
    all_planets = pygame.sprite.Group()
    planet_names = [
        "Mercury", "Venus", "Earth", "Mars", "Jupiter", 
        "Saturn", "Uranus", "Neptune", "Pluto", "Sedna",
        "Eris", "Ceres", "Haumea", "Makemake", 
        "Europa", "Ganymede", "Callisto", 
        "Titan", "Enceladus", "Rhea", "Oberon",
        "Miranda", "Charon", "Phobos", "Deimos"
    ]
    
    # Generates random coordinates for the initial placement of planets within the game window.
    for i in range(PLANET_COUNT):
        while True:
            x = randint(PLANET_RADIUS, WIDTH - PLANET_RADIUS)
            y = randint(PLANET_RADIUS, HEIGHT - PLANET_RADIUS)
            # Check for collisions with existing planets
            overlapping = any(planet.rect.colliderect(pygame.Rect(x - PLANET_RADIUS, y - PLANET_RADIUS, PLANET_RADIUS * 2, PLANET_RADIUS * 2)) for planet in all_planets)
            if not overlapping:
                break
        planet = Planet(planet_names[i], x, y, PLANET_COLORS[i])
        all_planets.add(planet)

    # Creates players of the game
    num_players = get_players_amount()
    players = []
    names = ["Bot"]
    for i in range(num_players):
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
    if num_players == 1:
        players.append(Player("Bot"))
    # Allows the user to choose between a 'long' or 'short' game.
    player = 0
    while True:
        turns = input("Long or Short Game?: ").strip().lower()
        if turns == "long":
            turns = 30
            break
        elif turns == "short":
            turns = 10
            break
        #only for testing purposes
        elif turns == "test":
            turns = 1
            break
        print("Enter 'long' or 'short'.")
    game_length = len(players) * turns
    
    clock = pygame.time.Clock()
    current_turn = 1
    printed = 0
    
    # Prints the turn number, player's name, and resource status at the beginning of each player's turn.
    while current_turn <= game_length:
        if current_turn % 2 == 1 and not printed:
            print(f"Turn {current_turn} of {game_length} - {players[player].name}'s turn")
            print(f"{players[player].name} has {players[player].show_resources()}")
            printed = True
        elif current_turn % 2 == 0 and not printed:
            print(f"Turn {current_turn} of {game_length} - {players[player].name}'s turn")
            printed = True
            
        if players[player].name == "Bot":
            # Select a random planet name
            selected_planet_name = choice(all_planets.sprites()).name
            
            # Find the corresponding Planet object based on the selected name
            selected_planet = None
            for planet in all_planets:
                if planet.name == selected_planet_name:
                    selected_planet = planet
                    break

            if selected_planet.owner is not None and selected_planet.owner != players[player]:
                # If the selected planet is owned by another player, attempt an attack
                attack_colony(players[player], selected_planet.owner, selected_planet)
            else:
                # Explore the planet and attempt to establish a colony
                explore_planet(players[player], selected_planet)
                establish_colony(players[player], selected_planet)
            current_turn += 1
            player += 1
            printed = False 
            if player % len(players) == 0:
                # The for loop prints the status of the game, and if a colony is owned by a player, then it prints the user name in bold and the planet that is owneed by the user.  
                print("\n\033[1m----- Galactic Status -----\033[0m")
                colonies_total = 0
                for planet in all_planets:
                    if planet.colony:
                        print(f"{planet.name} is owned by \033[1m{planet.owner.name}\033[0m")
                if colonies_total == 0:
                    print("No colonies have been established yet.\n")
                player = 0  # Reset the turn counter
        else:
            #This for loop  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # Exit the loop on quit
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for planet in all_planets:
                            if planet.rect.collidepoint(event.pos):
                                color = PLAYER_COLORS[player]
                                if planet.owner is not None:
                                    # If the planet is owned, explore or establish colony based on the player's turn
                                    if players[player] == planet.owner:
                                        explore_planet(players[player], planet)
                                    else:
                                        attack_colony(players[player], players[players.index(planet.owner)], planet)
                                        if planet.owner == players[player]:
                                            pygame.draw.circle(planet.image, color, (PLANET_RADIUS, PLANET_RADIUS), PLANET_RADIUS)
                                else:
                                    # If the planet is unowned, establish colony
                                    explore_planet(players[player], planet)
                                    establish_colony(players[player], planet)
                                    if planet.owner == players[player]:
                                        pygame.draw.circle(planet.image, color, (PLANET_RADIUS, PLANET_RADIUS), PLANET_RADIUS)
                                current_turn += 1
                                player += 1
                                printed = False 
                                if player % len(players) == 0:
                                    # The for loop prints the status of the game, and if a colony is owned by a player, then it prints the user name in bold and the planet that is owneed by the user.  
                                    print("\n\033[1m----- Galactic Status -----\033[0m")
                                    colonies_total = 0
                                    for planet in all_planets:
                                        if planet.colony:
                                            print(f"{planet.name} is owned by \033[1m{planet.owner.name}\033[0m")
                                            colonies_total += 1 
                                    if colonies_total == 0:
                                        print("No colonies have been established yet.\n")
                                    player = 0  # Reset the turn counter
                                break
    
                # Get the mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
    
                # Check for collision with planets and display names
                screen.blit(background_image, (0, 0))
                for _ in all_planets:
                    all_planets.draw(screen)  # Draw all the planets
    
                # Checks for hovering cursor over planets and displays names
                for planet in all_planets:
                    if planet.rect.collidepoint(mouse_x, mouse_y):
                        x, y = planet.rect.center
                        draw_text(planet.name, WHITE, x + planet.rect.width/2, y - planet.rect.width/2, 24, True)
                        pygame.draw.rect(screen, WHITE, planet.rect, 2)  # Draw a border around the planet
                
                pygame.display.flip()
                clock.tick(FPS)
         # The game finishes  
        if current_turn >= game_length + 1:
            print("Game over! Turns limit reached.")
            break
    end_screen(check_winner(players))
    pygame.quit()

# Runs main game code
main()
