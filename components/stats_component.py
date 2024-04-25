from entities.entity import Entity
from entities.flying_num import FlyingNum
from constants import *
from entities.text import Text


class StatsComponent(Entity):
    def __init__(self, entity, stats):
        super().__init__(entity.game)
        self.stats = stats
        self.entity = entity

    def set_stat(self, stat_name, new_stat):
        stat_change = new_stat - self.stats[stat_name]
        if stat_change > 0: color = LIGHT_GREEN
        if stat_change < 0: color = LIGHT_RED
        if stat_change == 0: color = GREY

        FlyingNum(self.game, f'{stat_change} {stat_name}', self.entity.transform_component.position, color)
        self.stats[stat_name] = new_stat

        if stat_name not in self.entity.statsText:
            self.entity.statsText[stat_name] = Text(self.game)
        
        self.entity.statsText[stat_name].str = f'{stat_name} {self.stats[stat_name]}'