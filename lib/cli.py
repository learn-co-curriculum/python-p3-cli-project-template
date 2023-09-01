from classes.player import Player
looping = True

player = Player()
high_score = 0
def mainGame():
    game_looping = True
    current_level = 0
    highest_level_reached = 0
    outcome = "defeat"

    while game_looping:
    
        print("""
-----------------------------------------------------------------------------
        You find yourself in a large, dark cave. 
        Ahead of you you see a tunnel branching off to the left, and one to the right. 
        Which do you choose? 
        (1) Left
        (2) Right
        (3) Stay here
        (x) Exit to main menu
                """)
        choice = input("Enter your choice: (1, 2, 3, or x): ")
        if choice in ("1", "2"):
            current_level +=1
            highest_level_reached = max(highest_level_reached, current_level)
            if current_level == 5:
                print("VICTORY! YOU'VE MADE IT OUT!")
                game_looping = False
                outcome = "victory"
        elif choice == "3":
            pass
        elif choice == "x":
            print("Thank you for playing!")
            print(f"You made it to level {highest_level_reached}")
            game_looping = False
        else:
            print("Not a valid input!")
    
    return (outcome, highest_level_reached)

while looping:
    # MAIN MENU
    print(f"""
        WELCOME TO CAVE CRAWLER!
        High Score: {high_score}
        To begin, press 'x'
        To exit, enter 'quit'
          """)
    choice = input("Begin your adventure? ")
    if choice == "x":
        (outcome, highest_level_reached) = mainGame()
        high_score = max(highest_level_reached, high_score)
    elif choice == "quit":
        looping = False
    else:
        print("Not a valid input!")
    
