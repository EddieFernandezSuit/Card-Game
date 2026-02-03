from entities.entity import Entity
from entities.flying_num import FlyingNum
from constants import *
from entities.text import Text
from Timer import Timer


class StatsComponent(Entity):
    def __init__(self, entity, stats):
        super().__init__(entity.game)
        self.stats = stats
        self.entity = entity
        self.timers = []
        self.stats_to_create = []

        # FlyingNum(self.game, str, position, color)

    def set_stat(self, stat_name, new_stat, delay=0):
        stat_change = new_stat - self.stats[stat_name]
        if stat_change > 0: color = LIGHT_GREEN
        if stat_change < 0: color = LIGHT_RED
        if stat_change == 0: color = GREY

        stat_change_text = f'+{stat_change}' if stat_change > 0 else str(stat_change)
        
        def create_flying_num():
            FlyingNum(self.game, f'{stat_change_text} {stat_name}', self.entity.transform_component.position, color)
            self.timers.pop(0)
        
        delay = (25 * (len(self.timers))) + 4
        self.timers.append(Timer(delay, create_flying_num))

        self.stats[stat_name] = new_stat

        if stat_name not in self.entity.statsText:
            self.entity.statsText[stat_name] = Text(self.game)
        
        self.entity.statsText[stat_name].str = f'{self.stats[stat_name]} {stat_name}'
    
    def update(self):
        for timer in self.timers:
            timer.update()