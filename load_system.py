class LoadSystem:
    """Manages vehicle load weight and its impact on performance."""
    
    def __init__(self, max_load_capacity):
        self.max_load_capacity = max(0, max_load_capacity)
        self.current_load = 0

    def add_load(self, weight):
        """Adds load weight to the system."""
        if weight < 0:
            raise ValueError("Load weight cannot be negative.")
        if self.current_load + weight > self.max_load_capacity:
            print("Warning: Exceeding max load capacity.")
        self.current_load += weight

    def remove_load(self, weight):
        """Removes load weight from the system."""
        if weight < 0:
            raise ValueError("Load weight cannot be negative.")
        self.current_load = max(0, self.current_load - weight)

    def get_load_penalty(self):
        """Calculates load penalty as a fraction affecting fuel efficiency."""
        return min(0.1, self.current_load * 0.002)  

    def __str__(self):
        return f"Current Load: {self.current_load} kg / Max Capacity: {self.max_load_capacity} kg"


