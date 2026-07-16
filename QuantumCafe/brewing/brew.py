from dataclasses import dataclass

@dataclass(frozen=True)
class BrewProfile:
    """Stores the brewing parameters for a single coffee recipe"""
    name: str
    coffee_dose: float  #grams
    water_mass: float   #grams
    
    temperature: float  #degree C

    bloom_time: float   #seconds
    bloom_water: float  #grams

    total_brew_time: float #seconds

    pour_rate: float  #grams/second

    @property
    def brew_ratio(self) -> float:
        return self.water_mass / self.coffee_dose # water-coffee ratio
    
    def extraction_stage_duration(self) -> float:
        return self.total_brew_time - self.bloom_time #time after bloom

#Brew profiles
MORNING_V60 = BrewProfile(name="Morning V60",
                          coffee_dose=18.0,
                          water_mass=300.0,
                          temperature=92.0,
                          bloom_time=40.0,
                          bloom_water=45.0,
                          total_brew_time=180.0,
                          pour_rate=6.0,
                         )