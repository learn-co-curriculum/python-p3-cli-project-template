from classes.player import Player


# print methods
def print_login_screen():
    print("                            ")
    print("+--------------------------+")
    print("| WELCOME TO CAVE CRAWLER! |")
    print("+--------------------------+")
    print("| Options:                 |")
    print("| 1. New Game              |")
    print("| 2. Load Game             |")
    print("| x: Exit Game             |")
    print("+--------------------------+")
    print("                            ")


def print_new_game_header():
    print("                            ")
    print("+--------------------------+")
    print("|         NEW GAME         |")
    print("+--------------------------+")
    print("                            ")


def print_load_game_header():
    print("                            ")
    print("+--------------------------+")
    print("|         LOAD GAME        |")
    print("+--------------------------+")
    print("                            ")


# menus
def view_new_game_menu():
    print_new_game_header()
    print("Create an account:")
    # print("\nUsername must be between 3 and 20 characters.")
    username = input("\nUsername: ")

    # print("\nPassword must be between 3 and 20 characters.")
    password = input("Password: ")

    # create account class?
    # account = Account(username, password)

    deciding = True

    while deciding:
        decision = input("\nCreate account? [y/n]: ")
        decision.lower()

        if decision == "y":
            # account.save()
            print(f"\nWelcome, {username.upper()}!")
            print("\nBeginning your adventure...")
            mainGame()
            deciding = False
        elif decision == "n":
            print("\nAccount creation canceled.")
            print("Returning to login screen...")
            deciding = False
        else:
            print("\nNot a valid input!")


def view_load_game_menu():
    print_load_game_header()
    print("Enter your account details:")

    # has to match info from database
    username = input("\nUsername: ")
    password = input("Password: ")

    # if it does match
    print(f"\nWelcome back, {username.upper()}!")
    print(f"\nHigh Score: {high_score}")
    print("\nBeginning your adventure...")
    mainGame()


def mainGame():
    game_looping = True
    current_level = 0
    highest_level_reached = 0
    outcome = "defeat"

    while game_looping:
        print(
            """
-----------------------------------------------------------------------------
        You find yourself in a large, dark cave.
        Ahead of you you see a tunnel branching off to the left, and one to the right.
        Which do you choose?
        (1) Left
        (2) Right
        (3) Stay here
        (x) Exit to main menu
                """
        )
        choice = input("Enter your choice: (1, 2, 3, or x): ")
        if choice in ("1", "2"):
            current_level += 1
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


# main method code
looping = True

player = Player()
high_score = 0

while looping:
    print_login_screen()
    choice = input("Input your choice: ")
    choice = choice.lower()

    if choice == "1":
        view_new_game_menu()
    elif choice == "2":
        view_load_game_menu()
    elif choice == "x":
        looping = False
        print("Exiting game...")
    else:
        print("Not a valid input!")
