import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd

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

SHIELD = 'shield'
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

DAMAGE_AP_SCALING = 'ap_dam'
DAMAGE_AD_SCALING = 'phys_dam'
SHIELD_AP_SCALING = 'shield'
HEAL_AP_SCALING = 'heal'
CAST_TIME = 'cast_time'


ON_AUTO_SCALING = 'auto'
ON_CAST_SCALING = 'cast'
ON_TIME_SCALING = 'time'
SCALE_TIME = 'scale_time'
PREVIOUS_SCALE = 'prev_scal_time'

ATTACK_SPEED_SCALING = 'as_scale'
ATTACK_DAMAGE_SCALING = 'ad_scale'
ABILITY_POWER_SCALING = 'ap_scale'
SCALE_AUTONUM = 'scale_autonum'

RAGEBLADE_AS = 0.1
RAGEBLADE_SCALING = 0.05
RAGEBLADE_AP = 10

DEATHBLADE_AD = 60

INFINITY_EDGE_AD = 25
INFINITY_EDGE_CRITCHANCE = 35

GIANT_SLAYER_AD = 30
GIANT_SLAYER_AP = 20
GIANT_SLAYER_AS = 0.1
GIANT_SLAYER_MULTIPLYER = 30
GIANT_SLAYER_THRESH = 1500

GUARDBREAKER_AD = 20
GUARDBREAKER_AP = 20
GUARDBREAKER_CRITCHANCE = 20
GUARDBREAKER_HEALTH = 150
GUARDBREAKER_MULTIPLYER = 30

DEFAULT_MANA_GAIN = 10
BLUEBUFF_MANA_RED = 10
BLUEBUFF_START_MANA = 40
BLUEBUFF_AP = 15

SHOJIN_MANA_GAIN = 20
SHOJIN_AUTO_NUM = 3
SHOJIN_START_MANA = 15
SHOJIN_AP = 15
SHOJIN_AD = 10

DEATHCAP_AP = 70
JEWELED_GAUNTLET_AP = 25
JEWELED_GAUNTLET_CRITCHANCE = 35

ARCHANGELS_AP = 20
ARCHANGELS_AP_SCALING = 20
ARCHANGELS_AP_SCALETIME = 5
ARCHANGELS_START_MANA = 15

START_AP = 100
START_CRITCHANCE = 25
START_CRITDAMAGE = 140

STAR_GUARDIAN = 'star_guardian'
STAR_GUARDIAN_MANA = {
    0: 0,
    3: 40,
    5: 70,
    7: 120,
}

RFC_AS = 0.5

MAX_AS = 5

class Champion:
    

    def __init__(self, base_stats, items = [], ability = None, traits = None, target=None, 
                            champion_name = None, champion_cost=None):
        self.champ_name = champion_name
        self.champion_cost = champion_cost
        self.scaling = self.init_scaling_dict()
        self.traits = self.apply_traits(traits)
        self.base_stats = base_stats 
        self.cur_stats = base_stats.copy()
        self.items = items 
        self.equip_items(self.items)
        self.ability = ability
        self.num_autos = 0
        self.num_seconds = 0
        self.num_casts = 0
        self.target = target
        

        
    def apply_traits(self, traits):
        return traits


    def init_scaling_dict(self):
        scaling_dict = {
            ON_AUTO_SCALING:{
                ATTACK_SPEED_SCALING: 0,
                ATTACK_DAMAGE_SCALING: 0,
                ABILITY_POWER_SCALING: 0,
                SCALE_AUTONUM: 1
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
                SCALE_TIME: 99,
                PREVIOUS_SCALE: 0 
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
            self.cur_stats[ABILITY_POWER] += DEATHCAP_AP
        if(item == INFINITY_EDGE):
            self.cur_stats[ATTACK_DAMAGE] += (INFINITY_EDGE_AD * 
                                            self.base_stats[ATTACK_DAMAGE]/100)
            
            self.add_crit(INFINITY_EDGE_CRITCHANCE)

        if(item == JEWELED_GAUNTLET):
            self.cur_stats[ABILITY_POWER] += JEWELED_GAUNTLET_AP  
            
            self.add_crit(JEWELED_GAUNTLET_CRITCHANCE)
        if(item == RUNNANS_HURRICANE):
            pass
        if(item == ARCHANGELS_STAFF):
            self.cur_stats[ABILITY_POWER] += ARCHANGELS_AP
            self.scaling[ON_TIME_SCALING][ABILITY_POWER_SCALING] = ARCHANGELS_AP_SCALING
            self.scaling[ON_TIME_SCALING][SCALE_TIME] = ARCHANGELS_AP_SCALETIME
            self.apply_start_mana( ARCHANGELS_START_MANA)

        if(item == GUINSOOS_RAGEBLADE):
            self.cur_stats[ATTACK_SPEED] += RAGEBLADE_AS*self.base_stats[ATTACK_SPEED]
            self.scaling[ON_AUTO_SCALING][ATTACK_SPEED_SCALING] += RAGEBLADE_SCALING
            self.cur_stats[ABILITY_POWER] += RAGEBLADE_AP
        if(item == RAPID_FIRE_CANNON):
            self.cur_stats[ATTACK_SPEED] += RFC_AS*self.base_stats[ATTACK_SPEED]
        if(item == BLUE_BUFF):
            self.cur_stats[MAX_MANA] = self.base_stats[MAX_MANA] - BLUEBUFF_MANA_RED
            self.apply_start_mana( BLUEBUFF_START_MANA)
            self.cur_stats[ABILITY_POWER] += BLUEBUFF_AP
        if(item == SPEAR_OF_SHOJIN):
            self.cur_stats[ATTACK_DAMAGE] += self.base_stats[ATTACK_DAMAGE] * SHOJIN_AD/100
            self.apply_start_mana( SHOJIN_START_MANA)
            self.cur_stats[ABILITY_POWER] += SHOJIN_AP
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
        try:
            star_guardian = self.traits[STAR_GUARDIAN]
        except TypeError:
            star_guardian = 0
        bonus = STAR_GUARDIAN_MANA[star_guardian]
        total_mana = DEFAULT_MANA_GAIN * (100+bonus)/100
        self.cur_stats[MANA] += total_mana
        if(SPEAR_OF_SHOJIN in self.items and self.num_autos%SHOJIN_AUTO_NUM == 0):
            self.cur_stats[MANA] += SHOJIN_MANA_GAIN * (100+bonus)/100

    def apply_start_mana(self, mana):
        star_guardian = self.traits[STAR_GUARDIAN]
        bonus = STAR_GUARDIAN_MANA[star_guardian]
        total_mana = mana * (100+bonus)/100
        self.cur_stats[MANA] += total_mana
        

    def apply_time_scaling(self):
        if(self.num_seconds - self.scaling[ON_TIME_SCALING][SCALE_TIME] > self.scaling[ON_TIME_SCALING][PREVIOUS_SCALE]):
            self.cur_stats[ABILITY_POWER] += self.scaling[ON_TIME_SCALING][ABILITY_POWER_SCALING]

            self.scaling[ON_TIME_SCALING][PREVIOUS_SCALE] += self.scaling[ON_TIME_SCALING][SCALE_TIME] 
        
    def perform_auto(self):
        self.num_autos += 1
        self.num_seconds += 1/self.cur_stats[ATTACK_SPEED]
        self.apply_mana()
        self.apply_as_stacks()
        min_damage = self.cur_stats[ATTACK_DAMAGE]
        max_damage = (self.cur_stats[ATTACK_DAMAGE]*
                        self.cur_stats[CRITICAL_DAMAGE]/100)
        

        if(GIANT_SLAYER in self.items and self.target.cur_stats[HEALTH] > GIANT_SLAYER_THRESH):
            max_damage *= 1+GIANT_SLAYER_MULTIPLYER/100
            min_damage *= 1+GIANT_SLAYER_MULTIPLYER/100


        if(GUARDBREAKER in self.items and self.target.cur_stats[SHIELD] > 0):
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
        self.num_seconds += self.ability[CAST_TIME]
        magic_damage = self.ability[DAMAGE_AP_SCALING]*self.cur_stats[ABILITY_POWER]/100 
        physical_damage = self.ability[DAMAGE_AD_SCALING]*self.cur_stats[ATTACK_DAMAGE]/100
        min_damage = magic_damage + physical_damage

        if(GIANT_SLAYER in self.items and self.target.cur_stats[HEALTH] > GIANT_SLAYER_THRESH):
            min_damage *= 1+GIANT_SLAYER_MULTIPLYER/100


        if(GUARDBREAKER in self.items and self.target.cur_stats[SHIELD] > 0):
            min_damage *= 1+GIANT_SLAYER_MULTIPLYER/100

        max_damage = min_damage
        if(JEWELED_GAUNTLET in self.items or INFINITY_EDGE in self.items):
            max_damage *= self.cur_stats[CRITICAL_DAMAGE]/100
        
        avg_damage = (min_damage * (100-self.cur_stats[CRITICAL_CHANCE])/100 +
                        max_damage * self.cur_stats[CRITICAL_CHANCE]/100)
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
            self.apply_time_scaling()
            if(self.cur_stats[MAX_MANA] < self.cur_stats[MANA]):
                min_damage, max_damage, avg_damage = self.cast_ability()
                min_damage_total.append(min_damage+min_damage_total[-1])
                max_damage_total.append(max_damage+max_damage_total[-1])
                avg_damage_total.append(avg_damage+avg_damage_total[-1])
                time_total.append(self.num_seconds)
            min_damage, max_damage, avg_damage = self.perform_auto()
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

def define_default_ability():
    ability = {
       DAMAGE_AP_SCALING : 100,
        DAMAGE_AD_SCALING : 100,
        SHIELD_AP_SCALING : 100,
        HEAL_AP_SCALING : 100,
        CAST_TIME : 2,
    }
    taliyah_ability = {
        DAMAGE_AP_SCALING : 400,
        DAMAGE_AD_SCALING : 0,
        SHIELD_AP_SCALING : 0,
        HEAL_AP_SCALING : 0,
        CAST_TIME : 2,
    }
    return taliyah_ability 

def define_default_stats():
    stats = {
        ATTACK_SPEED: 0.6,
        MAX_MANA: 100,
        MANA: 50,
        HEALTH: 1000,
        ATTACK_DAMAGE: 50,
        ABILITY_POWER:  100,
        ARMOR:  20,
        MAGIC_RESIST:  20,
        CRITICAL_CHANCE:  25,
        CRITICAL_DAMAGE:  140,
        OMNIVAMP: 0,
        SHIELD: 0
    }
    taliyah_stats = {
        ATTACK_SPEED: 0.75,
        MAX_MANA: 90,
        MANA: 0,
        HEALTH: 1700,
        ATTACK_DAMAGE: 68,
        ABILITY_POWER:  160,
        ARMOR:  30,
        MAGIC_RESIST:  30,
        CRITICAL_CHANCE:  25,
        CRITICAL_DAMAGE:  140,
        OMNIVAMP: 0,
        SHIELD: 1
    }
    return taliyah_stats

def graph_scenario(axes, champion, time, label):
    time_total, min_damage_total, max_damage_total, avg_damage_total = champion.simulate_fight(time)
    ax = graph_damage(time_total, min_damage_total, max_damage_total, avg_damage_total, axes, label)
    return ax, avg_damage_total[-1]

def graph_all_champs(champ_list):
    time=30
    
    for cost in range(5):
        fig, axes = plt.subplots(1,1)
        max_dmgs = []
        labels = []
        for champ in champ_list:
            
            if(champ.champion_cost == cost+1):
                label = 'champion:' + str(champ.champ_name)
                ax, max_dmg = graph_scenario(axes, champ, time, label=label)
                max_dmgs.append(max_dmg)
                labels.append(label)
        sorted_labels = [x for _, x in sorted(zip(max_dmgs, labels))]
        print(sorted_labels)
        order = np.argsort(-np.array(max_dmgs))
        h, l = plt.gca().get_legend_handles_labels()
        plt.legend(handles=list(np.array(h)[order]),labels=list(np.array(labels)[order]))
        plt.title('All Champions cost ' + str(cost+1))
        plt.show()

def interpret_scaling(string):
    if(isinstance(string, float) or isinstance(string, int)):
        return string 
    if('%' in string):
        string = string.split('%')[0]
    num = ""
    for c in string:
        if c.isdigit():
            num = num + c
    return float(num)
    
    


def read_csv_file(filename):
    df = pd.read_csv(filename, header = 1)
    champions = []
    for index, row in df.iterrows():
        champname = row['Champion']
        champcost = row['Cost']
        health = row['Health']
        armor = row['Armor']
        magic_resist = row['Armor']
        mana = row['Mana']
        try:
            start_mana = float(mana.split('/')[0])
            max_mana = float(mana.split('/')[1])
        except IndexError:
            start_mana = 0
            max_mana = 999
        except ValueError:
            start_mana = 0
            max_mana = 999
        attack_damage = row['Attack Damage']
        attack_speed = row['Attack Speed']

        stats = {
            ATTACK_SPEED: attack_speed,
            MAX_MANA: max_mana,
            MANA: start_mana,
            HEALTH: health,
            ATTACK_DAMAGE: attack_damage,
            ABILITY_POWER:  START_AP,
            ARMOR:  armor,
            MAGIC_RESIST:  magic_resist,
            CRITICAL_CHANCE: START_CRITCHANCE ,
            CRITICAL_DAMAGE: START_CRITDAMAGE,
            OMNIVAMP: 0,
            SHIELD: 0
        }
        if(isinstance(row['Ability AP Scaling'], str )):
            ability_ap_scaling = (row['Ability AP Scaling'].split('/')[0])
        else:
            ability_ap_scaling = 0

        if(isinstance(row['Ability AD Scaling'], str )):  
            ability_ad_scaling = (row['Ability AD Scaling'].split('/')[0])
        else:
            ability_ad_scaling = 0
        ability = {
            DAMAGE_AP_SCALING : interpret_scaling(ability_ap_scaling),
            DAMAGE_AD_SCALING : interpret_scaling(ability_ad_scaling),
            SHIELD_AP_SCALING : 100,
            HEAL_AP_SCALING : 100,
            CAST_TIME : 2,
        }

        champ = Champion(base_stats=stats, ability=ability, champion_name=champname, champion_cost=champcost)
        champions.append(champ)
    return champions


def item_test():
    time = 30
    fig, axes = plt.subplots(1,1)
    stats = define_default_stats()
    ability = define_default_ability()
    traits = {
        STAR_GUARDIAN: 3
    }
    '''
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
    '''
    
    item_combos=[
        [SPEAR_OF_SHOJIN, RABADONS_DEATHCAP, JEWELED_GAUNTLET],
        [SPEAR_OF_SHOJIN, GIANT_SLAYER, JEWELED_GAUNTLET],
        [GIANT_SLAYER, GUARDBREAKER, JEWELED_GAUNTLET],
        [SPEAR_OF_SHOJIN, GIANT_SLAYER, GUARDBREAKER],
        [BLUE_BUFF, GUINSOOS_RAGEBLADE, JEWELED_GAUNTLET],
        [BLUE_BUFF, JEWELED_GAUNTLET, GIANT_SLAYER],
        [BLUE_BUFF, RABADONS_DEATHCAP, JEWELED_GAUNTLET],
        [BLUE_BUFF, GIANT_SLAYER, GUARDBREAKER],
    ]
    '''
    item_combos=[
        [SPEAR_OF_SHOJIN, RABADONS_DEATHCAP, ],
        [SPEAR_OF_SHOJIN, GIANT_SLAYER, ],
        [SPEAR_OF_SHOJIN, GUARDBREAKER, ],
        [SPEAR_OF_SHOJIN, JEWELED_GAUNTLET, ],
        [SPEAR_OF_SHOJIN, ARCHANGELS_STAFF, ],
        [SPEAR_OF_SHOJIN, GUINSOOS_RAGEBLADE],
    ]
    '''
    targets= Champion(stats)
    is_shielded = (targets.cur_stats[SHIELD] > 0)
    is_big = (targets.cur_stats[HEALTH] > GIANT_SLAYER_THRESH)
    num_targts = 4
    ability[DAMAGE_AP_SCALING]*= num_targts
    
    for items in item_combos:
        print(items)
        test_champ = Champion(stats, items, ability, traits=traits, target=targets)

        ax = graph_scenario(axes, test_champ, time, label='Items:' + str(items))
    title_str = ('Taliyah 2 damage with 4 spellslinger,' + str(is_shielded)+' shielded target, ' +
                    str(is_big)+' above  1500 health, assuming ' +str(num_targts)+ ' targets, '+
                    str(traits[STAR_GUARDIAN])+' star guardian')
    plt.title(title_str)
    plt.show()

def main():
    filename = '/mnt/c/Users/tongt/Downloads/tft_Sheet4.csv'
    champ_list = read_csv_file(filename)
    graph_all_champs(champ_list)

if __name__ == '__main__':
    main()

        

        
