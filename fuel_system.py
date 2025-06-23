class FuelSystem:
    def __init__(self, fuel_capacity=None, base_mpg=None, load_weight=0, tire_pressure=32, 
                 weather_factor=0, vehicle_type="electric", battery_capacity=50.0, 
                 energy_consumption=0.2, num_cells=3, full_voltage=4.2, empty_voltage=3.0):
        """Initialize fuel system."""
        self.fuel_capacity = fuel_capacity
        self.base_mpg = base_mpg
        self.load_weight = max(0, load_weight)
        self.tire_pressure = max(20, tire_pressure)
        self.weather_factor = min(1, max(0, weather_factor))
        self.vehicle_type = vehicle_type.lower()
        self.battery_capacity = battery_capacity
        self.energy_consumption = energy_consumption
        self.num_cells = num_cells
        self.full_voltage = full_voltage * num_cells
        self.empty_voltage = empty_voltage * num_cells

    def calculate_adjusted_range(self):
        """Calculates range based on penalties."""
        load_penalty = min(0.1, self.load_weight * 0.002)
        tire_penalty = 0.1 if self.tire_pressure < 30 else 0
        weather_penalty = self.weather_factor

        if self.vehicle_type == "gasoline":
            if not self.fuel_capacity or not self.base_mpg:
                raise ValueError("Fuel capacity and MPG required for gasoline vehicles.")
            return self.fuel_capacity * self.base_mpg * (1 - load_penalty - tire_penalty - weather_penalty)

        elif self.vehicle_type == "electric":
            adjusted_energy_consumption = self.energy_consumption * (1 + load_penalty + tire_penalty + weather_penalty)
            return (self.battery_capacity / adjusted_energy_consumption) * 100

        elif self.vehicle_type == "hybrid":
            gasoline_range = self.fuel_capacity * self.base_mpg * (1 - load_penalty - tire_penalty - weather_penalty)
            electric_range = (self.battery_capacity / self.energy_consumption) * (1 - load_penalty - tire_penalty - weather_penalty)
            return gasoline_range + electric_range

        else:
            raise ValueError("Invalid vehicle type.")

def get_battery_specs():
    """Returns battery specifications dynamically."""
    return {
        "num_cells": 3,
        "capacity": 50.0,
        "full_voltage": 12.6,
        "empty_voltage": 9.0
    }
