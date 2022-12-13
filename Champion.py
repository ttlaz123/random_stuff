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

BASE_HEALTH = 'base_hp'
BASE_ATTACK_DAMAGE = 'base_ad'
BASE_ABILITY_POWER = 'base_ap'
BASE_ARMOR = 'base_armor'
BASE_MAGIC_RESIST = 'base_mr'
BASE_CRITICAL_CHANCE = 'base_crit'
BASE_ATTACK_SPEED = 'base_as'
BASE_MAX_MANA = 'base_max_mana'
BASE_OMNIVAMP = 'base_omnivamp'

CURRENT_HEALTH = 'cur_hp'
CURRENT_ATTACK_DAMAGE = 'cur_ad'
CURRENT_ABILITY_POWER = 'cur_ap'
CURRENT_ARMOR = 'cur_armor'
CURRENT_MAGIC_RESIST = 'cur_mr'
CURRENT_CRITICAL_CHANCE = 'cur_crit'
CURRENT_ATTACK_SPEED = 'cur_as'
CURRENT_MAX_MANA = 'cur_max_mana'
CURRENT_MANA = 'cur_mana'
CURRENT_OMNIVAMP = 'cur_omnivamp'


ON_AUTO_SCALING = 'auto'
ON_CAST_SCALING = 'cast'
ON_TIME_SCALING = 'time'

ATTACK_SPEED_SCALING = 'as_scale'
ATTACK_DAMAGE_SCALING = 'ad_scale'
ABILITY_POWER_SCALING = 'ap_scale'
class Champion:
    

    def __init__(self, base_stats, items = []):
        self.base_stats = base_stats 
        self.cur_stats = base_stats
        self.items = items 
        
        self.num_autos = 0
        self.num_seconds = 0
        self.num_casts = 0

        self.scaling = self.init_scaling_dict

        self.equip_items(self.items)

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
        if(isinstance(items, list)):
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
            pass
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
        self.num_seconds += 1/self.base_stats[CURRENT_ATTACK_SPEED]
        return 0,2,1

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

            if(self.cur_stats[CURRENT_MAX_MANA] < self.cur_stats[CURRENT_MANA]):
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
    
def main():
    stats = {
        CURRENT_ATTACK_SPEED: 1,
        CURRENT_MAX_MANA: 100,
        CURRENT_MANA: 0
    }
    test_champ = Champion(stats)
    time_total, min_damage_total, max_damage_total, avg_damage_total = test_champ.simulate_fight(30)
    fig, axes = plt.subplots(1,1)
    ax = graph_damage(time_total, min_damage_total, max_damage_total, avg_damage_total, axes)
    plt.show()

if __name__ == '__main__':
    main()

        

        
