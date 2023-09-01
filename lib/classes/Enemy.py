class Enemy:

    encountered = []

    def __init__(self, type, health, attack):
        self.type = type
        self.health = health
        self.attack = attack
        Enemy.encountered.append(self)

    def is_dead(self):
        return self.health <= 0