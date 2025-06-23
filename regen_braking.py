class RegenBraking:
    """Simulates regenerative braking and energy recovery."""
    
    def __init__(self, efficiency=0.7):
        self.efficiency = max(0, min(1, efficiency))  
        self.recovered_energy = 0.0  

    def apply_brake(self, vehicle_speed, braking_force):
        """Calculates recovered energy based on braking force and speed."""
        if vehicle_speed <= 0 or braking_force <= 0:
            return 0.0  

        energy_recovered = 0.5 * braking_force * (vehicle_speed ** 2) * self.efficiency  
        self.recovered_energy += energy_recovered  

        return energy_recovered  

    def get_total_recovered_energy(self):
        """Returns the total recovered energy in joules."""
        return self.recovered_energy

    def reset(self):
        """Resets the recovered energy counter."""
        self.recovered_energy = 0.0

    def __str__(self):
        return f"Total Recovered Energy: {self.recovered_energy:.2f} J"

