from classes.player import Player
looping = True

player = Player()
current_level = 0
highest_level_reached = 0
while looping:
    
    print("""
          You find yourself in a large, dark cave. 
          Ahead of you you see a tunnel branching off to the left, and one to the right. 
          Which do you choose? 
          (1) Left
          (2) Right
          (3) Stay here
          (x) Exit game
          """)
    choice = input("Enter your choice: (1, 2, 3, or x): ")
    if choice in ("1", "2"):
        current_level +=1
        highest_level_reached = max(highest_level_reached, current_level)
        if current_level == 5:
            print("VICTORY! YOU'VE MADE IT OUT!")
            looping = False
    elif choice == "3":
        pass
    elif choice == "x":
        print("Thank you for playing!")
        print(f"You made it to level {highest_level_reached}")
        looping = False
    pass