import matplotlib.pyplot as plt 
import numpy as np 

DEATH_BLADE = 'db'
RABADONS_DEATHCAP = 'dcap'
INFINITY_EDGE = 'ie'
JEWELED_GAUNTLET = 'jg'
RUNNANS_HURRICANE = 'hurricane'
ARCHANGELS_STAFF = 'aa'
GUINSOOS_RAGEBLADE = 'grb'
RAPID_FIRE_CANNON = 'rfc'
BLUE_BUFF = 'bb'
SPEAR_OF_SHOJIN = 'shojin'
HAND_OF_JUSTICE = 'hoj'
HEXTECH_GUNBLADE = 'gunblade'
BLOOD_THIRSTER = 'bt'
GIANT_SLAYER = 'gs'
GUARDBREAKER = 'guardbreaker'


HEALTH = 'cur_hp'
ATTACK_DAMAGE = 'cur_ad'
ABILITY_POWER = 'cur_ap'
ARMOR = 'cur_armor'
MAGIC_RESIST = 'cur_mr'
CRITICAL_CHANCE = 'cur_crit'
CRITICAL_DAMAGE = 'cur_critd'
ATTACK_SPEED = 'cur_as'
MAX_MANA = 'cur_max_mana'
MANA = 'cur_mana'
OMNIVAMP = 'cur_omnivamp'


ON_AUTO_SCALING = 'auto'
ON_CAST_SCALING = 'cast'
ON_TIME_SCALING = 'time'

ATTACK_SPEED_SCALING = 'as_scale'
ATTACK_DAMAGE_SCALING = 'ad_scale'
ABILITY_POWER_SCALING = 'ap_scale'

RAGEBLADE_AS = 0.1
RAGEBLADE_SCALING = 0.05
RAGEBLADE_AP = 10

DEATHBLADE_AD = 60

INFINITY_EDGE_AD = 25
INFINITY_EDGE_CRITCHANCE = 35

GIANT_SLAYER_AD = 30
GIANT_SLAYER_AP = 20
GIANT_SLAYER_AS = 0.1
GIANT_SLAYER_MULTIPLYER = 0

GUARDBREAKER_AD = 20
GUARDBREAKER_AP = 20
GUARDBREAKER_CRITCHANCE = 20
GUARDBREAKER_HEALTH = 150
GUARDBREAKER_MULTIPLYER = 0

RFC_AS = 0.5

MAX_AS = 5

class Champion:
    

    def __init__(self, base_stats, items = [], target=None):
        self.base_stats = base_stats 
        self.cur_stats = base_stats.copy()
        self.items = items 
        self.scaling = self.init_scaling_dict()
        self.equip_items(self.items)
        self.ability = {'something something'}
        self.num_autos = 0
        self.num_seconds = 0
        self.num_casts = 0
        self.target = target
        

        

    def init_scaling_dict(self):
        scaling_dict = {
            ON_AUTO_SCALING:{
                ATTACK_SPEED_SCALING: 0,
                ATTACK_DAMAGE_SCALING: 0,
                ABILITY_POWER_SCALING: 0,
            },
            ON_CAST_SCALING:{
                ATTACK_SPEED_SCALING: 0,
                ATTACK_DAMAGE_SCALING: 0,
                ABILITY_POWER_SCALING: 0,
            },
            ON_TIME_SCALING:{
                ATTACK_SPEED_SCALING: 0,
                ATTACK_DAMAGE_SCALING: 0,
                ABILITY_POWER_SCALING: 0,
            },

        }
        return scaling_dict

    def add_crit(self, crit_chance):
        self.cur_stats[CRITICAL_CHANCE] += crit_chance
        if(self.cur_stats[CRITICAL_CHANCE] > 100):
            self.cur_stats[CRITICAL_DAMAGE] += (self.cur_stats[CRITICAL_CHANCE]-100)/2
            self.cur_stats[CRITICAL_CHANCE] = 100

    def equip_items(self, items):
        if(not isinstance(items, list)):
            self.equip_item(items)
        else:
            for item in items:
                self.equip_item(item)

    def equip_item(self, item):
        if(item == DEATH_BLADE):
            self.cur_stats[ATTACK_DAMAGE] += (DEATHBLADE_AD * 
                                            self.base_stats[ATTACK_DAMAGE]/100)
            
        if(item == RABADONS_DEATHCAP):
            pass
        if(item == INFINITY_EDGE):
            self.cur_stats[ATTACK_DAMAGE] += (INFINITY_EDGE_AD * 
                                            self.base_stats[ATTACK_DAMAGE]/100)
            
            self.add_crit(INFINITY_EDGE_CRITCHANCE)

        if(item == JEWELED_GAUNTLET):
            pass
        if(item == RUNNANS_HURRICANE):
            pass
        if(item == ARCHANGELS_STAFF):
            pass
        if(item == GUINSOOS_RAGEBLADE):
            self.cur_stats[ATTACK_SPEED] += RAGEBLADE_AS*self.base_stats[ATTACK_SPEED]
            self.scaling[ON_AUTO_SCALING][ATTACK_SPEED_SCALING] += RAGEBLADE_SCALING
            self.cur_stats[ABILITY_POWER] += RAGEBLADE_AP
        if(item == RAPID_FIRE_CANNON):
            self.cur_stats[ATTACK_SPEED] += RFC_AS*self.base_stats[ATTACK_SPEED]
        if(item == BLUE_BUFF):
            pass
        if(item == SPEAR_OF_SHOJIN):
            pass
        if(item == HAND_OF_JUSTICE):
            pass
        if(item == HEXTECH_GUNBLADE):
            pass
        if(item == BLOOD_THIRSTER):
            pass
        if(item == GIANT_SLAYER):
            self.cur_stats[ATTACK_SPEED] += GIANT_SLAYER_AS*self.base_stats[ATTACK_SPEED]
            self.cur_stats[ATTACK_DAMAGE] += GIANT_SLAYER_AD*self.base_stats[ATTACK_DAMAGE]/100
            self.cur_stats[ABILITY_POWER] += GIANT_SLAYER_AP
        if(item == GUARDBREAKER):
            self.cur_stats[ATTACK_DAMAGE] += GUARDBREAKER_AD*self.base_stats[ATTACK_DAMAGE]/100
            self.cur_stats[ABILITY_POWER] += GUARDBREAKER_AP
            self.cur_stats[HEALTH] += GUARDBREAKER_HEALTH
            self.add_crit(GUARDBREAKER_CRITCHANCE)

    def apply_mana(self):
        self.cur_stats[MANA] += 10
        if(SPEAR_OF_SHOJIN in self.items and self.num_autos%3 == 0):
            self.cur_stats[MANA] += 20


    def perform_auto(self):
        self.num_autos += 1
        self.num_seconds += 1/self.cur_stats[ATTACK_SPEED]
        self.apply_mana()
        self.apply_as_stacks()
        min_damage = self.cur_stats[ATTACK_DAMAGE]
        max_damage = (self.cur_stats[ATTACK_DAMAGE]*
                        self.cur_stats[CRITICAL_DAMAGE]/100)
        

        if(GIANT_SLAYER in self.items):
            max_damage *= 1+GIANT_SLAYER_MULTIPLYER/100
            min_damage *= 1+GIANT_SLAYER_MULTIPLYER/100


        if(GUARDBREAKER in self.items):
            max_damage *= 1+GUARDBREAKER_MULTIPLYER/100
            min_damage *= 1+GIANT_SLAYER_MULTIPLYER/100

        
        avg_damage = (min_damage * (100-self.cur_stats[CRITICAL_CHANCE])/100 +
                        max_damage * self.cur_stats[CRITICAL_CHANCE]/100)
        return min_damage,max_damage,avg_damage
    
    def apply_as_stacks(self):
        self.cur_stats[ATTACK_SPEED] += (self.scaling[ON_AUTO_SCALING][ATTACK_SPEED_SCALING]*
                                            self.base_stats[ATTACK_SPEED])
        self.cur_stats[ATTACK_SPEED] = min(MAX_AS, self.cur_stats[ATTACK_SPEED])
  

    def cast_ability(self):
        self.cur_stats[MANA] = 0
        min_damage = self.ability['something']
        max_damage = self.ability['something']
        avg_damage = self.ability['something']
        return min_damage,max_damage,avg_damage 

    def initilize_fight(self):
        self.num_seconds = 0

    def simulate_fight(self, max_seconds):
        self.initilize_fight()
        min_damage_total = [0]
        max_damage_total = [0]
        avg_damage_total = [0]
        time_total = [0]
        while(self.num_seconds < max_seconds):
            min_damage, max_damage, avg_damage = self.perform_auto()
            min_damage_total.append(min_damage+min_damage_total[-1])
            max_damage_total.append(max_damage+max_damage_total[-1])
            avg_damage_total.append(avg_damage+avg_damage_total[-1])
            time_total.append(self.num_seconds)

            if(self.cur_stats[MAX_MANA] < self.cur_stats[MANA]):
                min_damage, max_damage, avg_damage = self.cast_ability()
                min_damage_total.append(min_damage+min_damage_total[-1])
                max_damage_total.append(max_damage+max_damage_total[-1])
                avg_damage_total.append(avg_damage+avg_damage_total[-1])
                time_total.append(self.num_seconds)

        return time_total, min_damage_total, max_damage_total, avg_damage_total

def graph_damage(time_total, min_damage_total, max_damage_total, avg_damage_total, ax, label='Damage'):
    ax.plot(time_total, avg_damage_total, label=label)
    ax.fill_between(time_total, min_damage_total, max_damage_total, alpha=0.2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Damage')
    ax.legend(loc='best')
    return ax 

def define_default_stats():
    stats = {
        ATTACK_SPEED: 0.6,
        MAX_MANA: 100,
        MANA: 0,
        HEALTH: 1000,
        ATTACK_DAMAGE: 50,
        ABILITY_POWER:  100,
        ARMOR:  20,
        MAGIC_RESIST:  20,
        CRITICAL_CHANCE:  25,
        CRITICAL_DAMAGE:  140,
        OMNIVAMP: 0,
    }
    return stats

def graph_scenario(axes, champion, time, label):
    time_total, min_damage_total, max_damage_total, avg_damage_total = champion.simulate_fight(time)
    ax = graph_damage(time_total, min_damage_total, max_damage_total, avg_damage_total, axes, label)
    return ax

def main():
    time = 30
    fig, axes = plt.subplots(1,1)
    stats = define_default_stats()
    item_combos = [
        [GUINSOOS_RAGEBLADE, GUINSOOS_RAGEBLADE, GIANT_SLAYER],
        [GUINSOOS_RAGEBLADE, INFINITY_EDGE, GIANT_SLAYER],
        [GUINSOOS_RAGEBLADE, DEATH_BLADE, GIANT_SLAYER],
        [INFINITY_EDGE, DEATH_BLADE, GIANT_SLAYER],
        [INFINITY_EDGE, INFINITY_EDGE, DEATH_BLADE],
        [DEATH_BLADE, DEATH_BLADE, DEATH_BLADE],
        [RAPID_FIRE_CANNON, RAPID_FIRE_CANNON, DEATH_BLADE],
        [RAPID_FIRE_CANNON, GUINSOOS_RAGEBLADE, DEATH_BLADE],

    ]

    for items in item_combos:
        test_champ = Champion(stats, items)
        ax = graph_scenario(axes, test_champ, time, label='Items:' + str(items))
    
    plt.show()

if __name__ == '__main__':
    main()

        

        
