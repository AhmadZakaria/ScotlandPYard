from .humandetective import HumanDetective

class Game():
    def __init__(self, num_detectives=4):
        self.detectives = []
        for i in range(num_detectives):
            detective = HumanDetective()
            self.detectives.append(detective)
