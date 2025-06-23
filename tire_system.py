class TireSystem:
    def __init__(self, pressure, health):
        self.pressure = pressure
        self.health = health

    def calculate_penalty(self):
        rolling_resistance = 0.02 if self.pressure < 30 else 0.01
        wear_penalty = 0.05 if self.health < 0.8 else 0
        if self.pressure < 30:
            penalty += 0.1
        if self.health < 0.8:
            penalty += 0.2
        return rolling_resistance + wear_penalty + penalty