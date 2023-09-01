class Player:

    def __init__(self):
        self.health = 10
        self.attack = 4
        self.sword = "Rusty Sword"

    def get_new_sword(self, new_sword):
        """
        sword = {name: Iron Sword, attack: 5}
        """
        self.attack = new_sword["attack"]
        self.sword = new_sword["name"]

    def find_hearts(self, number_of_hearts):
        self.health += number_of_hearts

    def game_over(self):
        return self.health <= 0