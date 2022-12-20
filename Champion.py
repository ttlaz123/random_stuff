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

class Champion:
    

    def __init__(self, base_stats, items = []):
        self.base_stats = base_stats 
        self.cur_stats = base_stats.copy()
        self.items = items 
        self.scaling = self.init_scaling_dict()
        self.equip_items(self.items)
        
        self.num_autos = 0
        self.num_seconds = 0
        self.num_casts = 0

        

        

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


    def equip_items(self, items):
        if(not isinstance(items, list)):
            self.equip_item(items)
        else:
            for item in items:
                self.equip_item(item)

    def equip_item(self, item):
        if(item == DEATH_BLADE):
            pass
        if(item == RABADONS_DEATHCAP):
            pass
        if(item == INFINITY_EDGE):
            pass
        if(item == JEWELED_GAUNTLET):
            pass
        if(item == RUNNANS_HURRICANE):
            pass
        if(item == ARCHANGELS_STAFF):
            pass
        if(item == GUINSOOS_RAGEBLADE):
            self.cur_stats[ATTACK_SPEED] += RAGEBLADE_AS
            self.scaling[ON_AUTO_SCALING][ATTACK_SPEED_SCALING] += RAGEBLADE_SCALING
            self.cur_stats[ABILITY_POWER] += RAGEBLADE_AP
        if(item == RAPID_FIRE_CANNON):
            pass
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
            pass
        if(item == GUARDBREAKER):
            pass

    def perform_auto(self):
        self.num_autos += 1
        self.num_seconds += 1/self.cur_stats[ATTACK_SPEED]
        self.apply_as_stacks()
        min_damage = self.cur_stats[ATTACK_DAMAGE]
        max_damage = (self.cur_stats[ATTACK_DAMAGE]*
                        self.cur_stats[CRITICAL_DAMAGE]/100)
        avg_damage = (min_damage * (100-self.cur_stats[CRITICAL_CHANCE])/100 +
                        max_damage * self.cur_stats[CRITICAL_CHANCE]/100)
        return min_damage,max_damage,avg_damage
    
    def apply_as_stacks(self):
        self.cur_stats[ATTACK_SPEED] += (self.scaling[ON_AUTO_SCALING][ATTACK_SPEED_SCALING]*
                                            self.base_stats[ATTACK_SPEED])
        print(self.cur_stats[ATTACK_SPEED])

    def cast_ability(self):
        return 0,0,0 

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
    ax.fill_between(time_total, min_damage_total, max_damage_total, alpha=0.5)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Damage')
    ax.legend()
    return ax 

def define_default_stats():
    stats = {
        ATTACK_SPEED: 0.7,
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
    stats = define_default_stats()
    items = [GUINSOOS_RAGEBLADE]
    test_champ = Champion(stats, items)
    
    fig, axes = plt.subplots(1,1)
    ax = graph_scenario(axes, test_champ, time=30, label='Items:' + str(items))
    items = []
    test_champ2 = Champion(stats, items)
    ax = graph_scenario(axes, test_champ2, time=30, label='Items:' + str(items))

    plt.show()

if __name__ == '__main__':
    main()

        

        
