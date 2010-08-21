from random import random

class Die:
    """
    Abstracts the random dice throw. Roll will produce the result.
    The die can be further parametrized by a multiplicator and/or
    a modifier, like 2 * Die(8) +4.
    """
    def __init__(self, number, multiplicator=1, modifier=0):
        self.number = number  
        self.multiplicator = multiplicator
        self.modifier = modifier
        
    def roll(self):
        return self.multiplicator * random.choice(range(1, self.number + 1)) + self.modifier
    
    def __rmul__(self, other):
        return Die(self.number, multiplicator=other, modifier=self.modifier)
    
    def __add__(self, other):
        return Die(self.number, multiplicator=self.multiplicator, modifier=other)
    
    def __call__(self):
        return self.roll()
    
    def __eq__(self, other):
        return (other.number       == self.number and 
               other.multiplicator == self.multiplicator and
               other.modifier      == self.modifier)
    
    @classmethod
    def parse(cls, text):
        return cls.__new__()
    
    def __repr__(self):
        base = "%sd%s" % (self.multiplicator, self.number)
        if self.modifier > 0:
            return base + ("+%s" % self.modifier)
        return base
    
        
    
d4 = Die(4)
d6 = Die(6)
d8 = Die(8)
d10 = Die(10)
d12 = Die(12)
d20 = Die(20)
d100 = Die(100)   