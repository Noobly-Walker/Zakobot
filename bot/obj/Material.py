from dataclasses import *

@dataclass
class MAT:
    name = None
    
    melting_point = 373.15 # in kelvins
    boiling_point = 473.15 # in kelvins
    
    solid_density = 5.00 # in ton per cubic meter
    liquid_density = 4.50 # in ton per cubic meter
    gas_density = 4.00 # in ton per cubic meter

    hardness = 2 # in mohs
    tenacity = 0 #0 is water, 5 is gold

    if hardness-tenacity >= 5 and melting_point > 1000:
        tool_grade = True
    else:
        tool_grade = False
