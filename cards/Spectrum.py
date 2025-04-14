from cards import Card

class Spectrum(Card):
    def __init__(self, ally, status):
        super().__init__(6, 7, "Spectrum", ally, status)
        self.description = "On Reveal: Give your Ongoing cards +2 Power"
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in locationlist["location1"].allies + locationlist["location2"].allies + locationlist["location3"].allies:
                if card.has_ongoing:
                    card.onreveal_buff += 2
        else:
            for card in locationlist["location1"].enemies + locationlist["location2"].enemies + locationlist["location3"].enemies:
                if card.has_ongoing:
                    card.onreveal_buff += 2