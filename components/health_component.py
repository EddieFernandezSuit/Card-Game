class HealthComponent:
    def __init__(self, base_health, current_health=0):
        self.max_health = base_health
        self.current_health = current_health

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0
