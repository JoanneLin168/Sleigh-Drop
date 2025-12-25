from src.entities.snowparticle import SnowParticle

class SnowManager:
    def __init__(self, count, screen_width, screen_height):
        self.particles = [
            SnowParticle(screen_width, screen_height)
            for _ in range(count)
        ]

    def update(self):
        for p in self.particles:
            p.update()

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
