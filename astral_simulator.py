import copy
import math
import os
import time
import cProfile

from pycallgraph import PyCallGraph, Config, GlobbingFilter
from pycallgraph.output import GraphvizOutput
import sys

# skill : +20
# magick attack : 314 contre 324 => 2.5
# magick power : 296 contre 302 => 1.5
# crit hit : 260 contre 266 => 1.5
import webbrowser


class Stats:
    hp = 0
    mastery = 0
    magic_power = 0
    haste = 0
    magic_critical_hit = 0
    skill = 0
    perception = 0
    magical_attack = 0
    physical_defence = 0
    magical_defence = 0
    five_percent_twelve_meter = 0
    critical_damage_three_percent = 0
    perception_one_percent = 0
    haste_eight_percent = 0
    critical_hit_damage_percent = 0
    magical_attack_skill = 0
    magical_power_skill = 0
    magical_critical_hit_skill = 0

    def __copy__(self):
        stats = Stats()
        stats.magical_attack_skill = self.magical_attack_skill
        stats.magical_power_skill = self.magical_power_skill
        stats.magical_critical_hit_skill = self.magical_critical_hit_skill
        stats.hp = self.hp
        stats.mastery = self.mastery
        stats.magic_power = self.magic_power
        stats.haste = self.haste
        stats.magic_critical_hit = self.magic_critical_hit
        stats.skill = self.skill
        stats.perception = self.perception
        stats.magical_attack = self.magical_attack
        stats.physical_defence = self.physical_defence
        stats.magical_defence = self.magical_defence
        stats.five_percent_twelve_meter = self.five_percent_twelve_meter
        stats.critical_damage_three_percent = self.critical_damage_three_percent
        stats.perception_one_percent = self.perception_one_percent
        stats.haste_eight_percent = self.haste_eight_percent
        stats.critical_hit_damage_percent = self.critical_hit_damage_percent

        return stats

    def __deepcopy__(self, memodict={}):
        # no need to deepcopy, we only use integers
        stats = Stats()
        stats.magical_attack_skill = self.magical_attack_skill
        stats.magical_power_skill = self.magical_power_skill
        stats.magical_critical_hit_skill = self.magical_critical_hit_skill
        stats.hp = self.hp
        stats.mastery = self.mastery
        stats.magic_power = self.magic_power
        stats.haste = self.haste
        stats.magic_critical_hit = self.magic_critical_hit
        stats.skill = self.skill
        stats.perception = self.perception
        stats.magical_attack = self.magical_attack
        stats.physical_defence = self.physical_defence
        stats.magical_defence = self.magical_defence
        stats.five_percent_twelve_meter = self.five_percent_twelve_meter
        stats.critical_damage_three_percent = self.critical_damage_three_percent
        stats.perception_one_percent = self.perception_one_percent
        stats.haste_eight_percent = self.haste_eight_percent
        stats.critical_hit_damage_percent = self.critical_hit_damage_percent

        return stats

    def haste_percent(self):
        return self.haste * (1 + self.haste_eight_percent * 0.08) / 13.5 + 8

    def critical_percent(self):
        return (self.magic_critical_hit + self.magical_critical_hit_skill) * 0.0643 - 0.0171

    def perception_percent(self):
        return (self.perception / 16.5 + 80) + self.perception_one_percent

    def __add__(self, other):
        stats = Stats()
        stats.hp = self.hp + other.hp
        stats.magical_attack_skill = self.magical_attack_skill + other.magical_attack_skill
        stats.magical_power_skill = self.magical_power_skill + other.magical_power_skill
        stats.magical_critical_hit_skill = self.magical_critical_hit_skill + other.magical_critical_hit_skill
        stats.mastery = self.mastery + other.mastery
        stats.magic_power = self.magic_power + other.magic_power
        stats.haste = self.haste + other.haste
        stats.magic_critical_hit = self.magic_critical_hit + other.magic_critical_hit
        stats.skill = self.skill + other.skill
        stats.perception = self.perception + other.perception
        stats.magical_attack = self.magical_attack + other.magical_attack
        stats.physical_defence = self.physical_defence + other.physical_defence
        stats.magical_defence = self.magical_defence + other.magical_defence
        stats.five_percent_twelve_meter = self.five_percent_twelve_meter + other.five_percent_twelve_meter
        stats.critical_damage_three_percent = self.critical_damage_three_percent + other.critical_damage_three_percent
        stats.perception_one_percent = self.perception_one_percent + other.perception_one_percent
        stats.haste_eight_percent = self.haste_eight_percent + other.haste_eight_percent
        stats.critical_hit_damage_percent = self.critical_hit_damage_percent + other.critical_hit_damage_percent

        return stats    
    
    def __sub__(self, other):
        stats = Stats()
        stats.hp = self.hp - other.hp
        stats.magical_attack_skill = self.magical_attack_skill - other.magical_attack_skill
        stats.magical_power_skill = self.magical_power_skill - other.magical_power_skill
        stats.magical_critical_hit_skill = self.magical_critical_hit_skill - other.magical_critical_hit_skill
        stats.mastery = self.mastery - other.mastery
        stats.magic_power = self.magic_power - other.magic_power
        stats.haste = self.haste - other.haste
        stats.magic_critical_hit = self.magic_critical_hit - other.magic_critical_hit
        stats.skill = self.skill - other.skill
        stats.perception = self.perception - other.perception
        stats.magical_attack = self.magical_attack - other.magical_attack
        stats.physical_defence = self.physical_defence - other.physical_defence
        stats.magical_defence = self.magical_defence - other.magical_defence
        stats.five_percent_twelve_meter = self.five_percent_twelve_meter - other.five_percent_twelve_meter
        stats.critical_damage_three_percent = self.critical_damage_three_percent - other.critical_damage_three_percent
        stats.perception_one_percent = self.perception_one_percent - other.perception_one_percent
        stats.haste_eight_percent = self.haste_eight_percent - other.haste_eight_percent
        stats.critical_hit_damage_percent = self.critical_hit_damage_percent - other.critical_hit_damage_percent

        return stats

    def __neg__(self):
        stats = Stats()
        stats.magical_attack_skill = -self.magical_attack_skill
        stats.magical_power_skill = -self.magical_power_skill
        stats.magical_critical_hit_skill = -self.magical_critical_hit_skill
        stats.hp = -self.hp
        stats.mastery = -self.mastery
        stats.magic_power = -self.magic_power
        stats.haste = -self.haste
        stats.magic_critical_hit = -self.magic_critical_hit
        stats.skill = -self.skill
        stats.perception = -self.perception
        stats.magical_attack = -self.magical_attack
        stats.physical_defence = -self.physical_defence
        stats.magical_defence = -self.magical_defence
        stats.five_percent_twelve_meter = -self.five_percent_twelve_meter
        stats.critical_damage_three_percent = -self.critical_damage_three_percent
        stats.perception_one_percent = -self.perception_one_percent
        stats.haste_eight_percent = -self.haste_eight_percent
        stats.critical_hit_damage_percent = -self.critical_hit_damage_percent

        return stats

    def __str__(self):
        return "skill " + str(self.skill) + "\n" + \
               "magical_attack " + str(self.magical_attack) + "\n" + \
               "magical_attack_skill " + str(self.magical_attack_skill) + "\n" + \
               "magical_total " + str(self.magical_attack_skill + self.magical_attack) + "\n" + \
               "magic_power " + str(self.magic_power) + "\n" + \
               "magic_power_real " + str(self.magic_power + self.magical_power_skill) + "\n" + \
               "mastery " + str(self.mastery) + "\n" + \
               "critical_percent " + str(self.critical_percent()) + "\n" + \
               "perception_percent " + str(self.perception_percent()) + "\n" + \
               "haste_percent " + str(self.haste_percent()) + "\n" + \
               "magic_critical_hit " + str(self.magic_critical_hit) + "\n" + \
               "magic_critical_hit_real " + str(self.magic_critical_hit + self.magical_critical_hit_skill) + "\n" + \
               "perception " + str(self.perception) + "\n" + \
               "haste " + str(self.haste) + "\n" + \
               "physical_defence " + str(self.physical_defence) + "\n" + \
               "magical_defence " + str(self.magical_defence) + "\n" + \
               "five_percent_twelve_meter " + str(self.five_percent_twelve_meter) + "\n" + \
               "critical_damage_three_percent " + str(self.critical_damage_three_percent) + "\n" + \
               "haste_eight_percent " + str(self.haste_eight_percent) + "\n" + \
               "critical_hit_damage_percent " + str(self.critical_hit_damage_percent) + "\n" + \
               "hp " + str(self.hp) + "\n"

# 290 315
# 306 332
# +9, real + 17
# 293, 318 [308]
# skill + 5
# 296, 321 [311]

# 314 (299, 324)
# 316 (301, 326)

special_cost = {}

def node_0(stats: Stats):
    return stats


def node_1(stats: Stats):
    stats.hp += 108
    return stats


def node_2(stats: Stats):
    stats.haste += 13
    return stats


def node_3(stats: Stats):
    stats.perception += 13
    return stats


def node_4(stats: Stats):
    stats.magical_attack += 3
    return stats


def node_5(stats: Stats):
    stats.physical_defence += 7
    return stats


def node_6(stats: Stats):
    stats.skill += 5
    stats.magical_attack_skill += 2.5
    stats.magical_power_skill += 1.5
    stats.magical_critical_hit_skill += 1.5
    return stats


def node_7(stats: Stats):
    stats.mastery += 13
    return stats


def node_8(stats: Stats):
    stats.magic_critical_hit += 13
    return stats


def node_8_1_0(stats: Stats):
    stats.five_percent_twelve_meter += 1
    return stats


special_cost[node_8_1_0] = 2


def node_8_2_0(stats: Stats):
    stats.mastery += 13
    return stats


def node_8_2_1(stats: Stats):
    stats.magic_power += 13
    return stats


def node_8_2_2(stats: Stats):
    stats.magic_critical_hit += 13
    return stats


def node_8_2_3(stats: Stats):
    stats.hp += 108
    return stats


def node_8_2_3_1_0(stats: Stats):
    stats.hp += 108
    return stats


def node_8_2_3_1_1(stats: Stats):
    stats.magic_critical_hit += 13
    return stats


def node_8_2_3_1_2(stats: Stats):
    stats.haste += 13
    return stats


def node_8_2_3_1_3(stats: Stats):
    stats.magical_defence += 7
    return stats


def node_8_2_3_1_4(stats: Stats):
    stats.magical_attack += 3
    return stats


def node_8_2_3_1_5(stats: Stats):
    stats.perception += 13
    return stats


def node_8_2_3_1_6(stats: Stats):
    stats.skill += 5
    stats.magical_attack_skill += 2.5
    stats.magical_power_skill += 1.5
    stats.magical_critical_hit_skill += 1.5
    return stats


def node_8_2_3_1_7(stats: Stats):
    stats.magic_power += 13
    return stats


def node_8_2_3_1_7_1_0(stats: Stats):
    # reduction de dégats en aoe
    return stats


def node_8_2_3_1_7_2_0(stats: Stats):
    stats.mastery += 13
    return stats


def node_8_2_3_1_7_2_1(stats: Stats):
    stats.perception += 13
    return stats


def node_8_2_3_1_7_2_2(stats: Stats):
    stats.magic_power += 13
    return stats


def node_8_2_3_1_7_2_3(stats: Stats):
    stats.hp += 108
    return stats


def node_8_2_3_1_7_2_4(stats: Stats):
    stats.skill += 5
    stats.magical_attack_skill += 2.5
    stats.magical_power_skill += 1.5
    stats.magical_critical_hit_skill += 1.5
    return stats


def node_8_2_3_1_7_2_5(stats: Stats):
    stats.magic_critical_hit += 13
    return stats


def node_8_2_3_1_7_2_6(stats: Stats):
    stats.haste += 13
    return stats


def node_8_2_3_1_7_2_7(stats: Stats):
    stats.magical_defence += 7
    return stats


def node_8_2_3_1_7_2_8(stats: Stats):
    stats.haste_eight_percent += 1
    return stats


def node_8_2_3_1_7_2_9(stats: Stats):
    stats.haste_eight_percent += 1
    return stats


def node_8_2_3_1_7_2_10(stats: Stats):
    stats.haste_eight_percent += 1
    return stats


def node_8_2_3_2_0(stats: Stats):
    stats.magical_defence += 7
    return stats


def node_8_2_3_2_1(stats: Stats):
    stats.skill += 5
    stats.magical_attack_skill += 2.5
    stats.magical_power_skill += 1.5
    stats.magical_critical_hit_skill += 1.5
    return stats


def node_8_2_3_2_2(stats: Stats):
    stats.magical_attack += 3
    return stats


def node_8_2_3_2_2_1_0(stats: Stats):
    stats.physical_defence += 7
    return stats


def node_8_2_3_2_2_1_0_1_0(stats: Stats):
    # chance de root
    return stats


def node_8_2_3_2_2_1_0_2_0(stats: Stats):
    stats.hp += 108
    return stats


def node_8_2_3_2_2_1_0_2_1(stats: Stats):
    stats.mastery += 13
    return stats


def node_8_2_3_2_2_1_0_2_2(stats: Stats):
    stats.magic_critical_hit += 13
    return stats


def node_8_2_3_2_2_1_0_2_3(stats: Stats):
    stats.perception += 13
    return stats


def node_8_2_3_2_2_1_0_2_4(stats: Stats):
    stats.magic_power += 13
    return stats


def node_8_2_3_2_2_1_0_2_5(stats: Stats):
    stats.magical_defence += 7
    return stats


def node_8_2_3_2_2_1_0_2_6(stats: Stats):
    stats.magical_attack += 3
    return stats


def node_8_2_3_2_2_1_0_2_7(stats: Stats):
    stats.haste += 13
    return stats


def node_8_2_3_2_2_1_0_2_8(stats: Stats):
    stats.perception_one_percent += 1
    return stats


def node_8_2_3_2_2_1_0_2_9(stats: Stats):
    stats.perception_one_percent += 1
    return stats


def node_8_2_3_2_2_1_0_2_10(stats: Stats):
    stats.perception_one_percent += 1
    return stats


def node_8_2_3_2_2_1_0_2_11(stats: Stats):
    stats.perception_one_percent += 1
    return stats


def node_8_2_3_2_2_1_0_2_12(stats: Stats):
    stats.perception_one_percent += 1
    return stats


def node_8_2_3_2_2_2_0(stats: Stats):
    stats.magic_power += 13
    return stats


def node_8_2_3_2_2_2_1(stats: Stats):
    stats.skill += 5
    stats.magical_attack_skill += 2.5
    stats.magical_power_skill += 1.5
    stats.magical_critical_hit_skill += 1.5
    return stats


def node_8_2_3_2_2_2_2(stats: Stats):
    stats.haste += 13
    return stats


def node_8_2_3_2_2_2_3(stats: Stats):
    stats.perception += 13
    return stats


def node_8_2_3_2_2_2_4(stats: Stats):
    stats.hp += 108
    return stats


def node_8_2_3_2_2_2_4_1_0(stats: Stats):
    stats.magical_defence += 7
    return stats


def node_8_2_3_2_2_2_4_1_1(stats: Stats):
    stats.mastery += 13
    return stats


def node_8_2_3_2_2_2_4_1_2(stats: Stats):
    stats.magical_attack += 3
    return stats


def node_8_2_3_2_2_2_4_1_3(stats: Stats):
    stats.critical_hit_damage_percent += 1
    return stats


def node_8_2_3_2_2_2_4_1_4(stats: Stats):
    stats.critical_hit_damage_percent += 1
    return stats


def node_8_2_3_2_2_2_4_1_5(stats: Stats):
    stats.critical_hit_damage_percent += 1
    return stats


def node_8_2_3_2_2_2_4_2_0(stats: Stats):
    stats.haste += 13
    return stats


def node_8_2_3_2_2_2_4_2_1(stats: Stats):
    stats.skill += 5
    stats.magical_attack_skill += 2.5
    stats.magical_power_skill += 1.5
    stats.magical_critical_hit_skill += 1.5
    return stats


def node_8_2_3_2_2_2_4_2_2(stats: Stats):
    stats.magic_critical_hit += 13
    return stats


def node_8_2_3_2_2_2_4_2_3(stats: Stats):
    stats.perception += 13
    return stats


def node_8_2_3_2_2_2_4_2_4(stats: Stats):
    stats.physical_defence += 7
    return stats


def node_8_2_3_2_2_2_4_2_5(stats: Stats):
    stats.magical_attack += 3
    return stats


def node_8_2_3_2_2_2_4_2_6(stats: Stats):
    stats.magic_power += 13
    return stats


def node_8_2_3_2_2_2_4_2_7(stats: Stats):
    stats.mastery += 13
    return stats


def node_8_2_3_2_2_2_4_2_8(stats: Stats):
    stats.critical_damage_three_percent += 1
    return stats


def node_8_2_3_2_2_2_4_2_9(stats: Stats):
    stats.critical_damage_three_percent += 1
    return stats


def node_8_2_3_2_2_2_4_2_10(stats: Stats):
    stats.critical_damage_three_percent += 1
    return stats


final_trees = []
final_trees_signatures = []
all_signatures = set()
global_steps = 0


def signature(visited_nodes):
    return ' '.join(sorted(visited_nodes))


def test_opti_2(current_stats: Stats, tree, profondeur, max, heads, visited):

    # heads représente les noeuds possibles

    global global_steps
    global_steps += 1

    if len(heads) == 0:
        # on a tout visité
        print("Tout visité")
        visited = copy.copy(visited)
        current_stats = copy.deepcopy(current_stats)
        dps = calculate_dps(current_stats)
        print(len(visited))
        signa = signature(visited)

        if signa not in final_trees_signatures:
            final_trees.append((visited, dps, current_stats))
            final_trees_signatures.append(signa)

    # print("heads : " + ', '.join([head.__name__ for head in heads]))
    # print(str(max) + " len(visitesqsqdqdsdsqd)" + str(len(visited)))

    for head in heads:
        if head not in tree:
            # bout atteint, on va voir ailleurs
            print("Error : should not happen (all nodes have a child)")
            pass
        else:
            # print(visited, signature(visited))
            for head in heads:
                head_name = '_'.join(head.__name__.split("_")[1:])
                # print()
                # print("profondeur : " + str(profondeur))
                # print("visited : " + visited)

                # print(calculate_dps(current_stats))
                # print(str(max) + " len(visited)" + str(len(visited)))


                cost = 0
                if head in special_cost:
                    # noeuds vides pour reflèter les coûts
                    cost = special_cost[head] - 1

                # Si on a encore des points à dépenser
                # print(visited, max, head_name, len(visited) + cost, calculate_dps(new_stats))
                if len(visited) + cost <= max:
                    new_stats = head(copy.deepcopy(current_stats))

                    new_heads = copy.copy(heads)

                    if head in tree:
                        new_heads.extend(tree[head])
                    new_heads.remove(head)

                    new_visited = copy.copy(visited)
                    new_visited.append(head_name)
                    new_visited.extend('' for _ in range(cost))
                    if signature(new_visited) not in all_signatures:
                        # certains chemins peuvent être équivalents (ordre de parcours)

                        all_signatures.add(signature(new_visited))
                        test_opti_2(copy.deepcopy(new_stats), tree, profondeur + 1, max, new_heads, new_visited)
                else:
                    current_stats = copy.deepcopy(current_stats)
                    dps = calculate_dps(current_stats)
                    signa = signature(visited)

                    if signa not in final_trees_signatures:
                        final_trees.append((visited, dps, current_stats))
                        final_trees_signatures.append(signa)


def do_nothing(x):
    pass

temps = 300
attack_numbers_cache = {}
attack_numbers_total_calls = 0
attack_numbers_cached_calls = 0

brd_ds_nm_numbers_cache = {}
brd_ds_nm_numbers_total_calls = 0
brd_ds_nm_numbers_cached_calls = 0

calculate_aw_fs_atc_ts_emh_damage_numbers_cache = {}
calculate_aw_fs_atc_ts_emh_damage_total_calls = 0
calculate_aw_fs_atc_ts_emh_damage_cached_calls = 0

calculate_total_damage_numbers_cache = {}
calculate_total_damage_numbers_total_calls = 0
calculate_total_damage_numbers_cached_calls = 0

dps_cache = {}
dps_total_calls = 0
dps_cached_calls = 0

def calculate_freq(haste_percent, critical_percent):
    M4 = 2 # manual alignment
    N3 = haste_percent
    N12 = N3/100 + 1
    N6 = N12/0.95
    N9 = N12/0.95/0.95

    C3 = 1.5
    D3 = C3 / N6
    E3 = 0
    F3 = E3 / N12
    G3 = C3 / N9

    C4 = 3
    D4 = C4 / N6
    E4 = 0
    F4 = E4 / N12
    G4 = C4 / N9

    C5 = 0
    D5 = C5 / N6
    E5 = 0
    F5 = E5 / N12
    G5 = C5 / N9

    C6 = 0
    D6 = C6 / N6
    E6 = 15
    F6 = 15
    G6 = C6 / N9

    C7 = 0.8
    D7 = C7 / N6
    E7 = 60
    F7 = 60
    G7 = C7 / N9

    C8 = 0
    D8 = C8 / N6
    E8 = 0
    F8 = E8 / N12
    G8 = C8 / N9

    C9 = 0
    D9 = C9 / N6
    E9 = 120
    F9 = E9 / N12
    G9 = C9 / N9

    C10 = 1.50
    G10 = 1.50

    C11 = 1.5
    D11 = C11 / N6
    E11 = 18
    F11 = E11 / N12
    G11 = C11 / N9

    C12 = 1.5
    D12 = C12 / N6
    E12 = 18
    F12 = E12 / N12
    G12 = C12 / N9

    # EMH
    I9=math.floor((temps/F9+1))

    # ATC+IM
    K7=max(math.floor((temps-10)/F7)+1-M4, 0)
    L7=M4

    M8=20*(M4)
    M6 =max(math.floor(((temps-10)/F7)+1)*20-M8,0)
    M10 = max(I9*20-M8,0)
    M12 = temps-M6-M8-M10

    # NM FFULL7
    L12=K7
    K12=L7+1

    # NM Icy Melody
    I11=max(M12/(F11+D11)-(1*I9)-1*K7, 0)
    J11=max(math.floor(((M10)/(F11+D11)))+(1*(I9-M4)), 0)
    K11=max(math.floor(((M6-(K12*2))/(F11+G11))+(K12*3)-K12), 0)
    L11=math.floor(((M8-(L7*4))/(F11+G11))+(L7*3)-L12+(1*(M4)))+1



    # AW
    I3 = max(math.floor((M12-((I9-1)*0.5)-((I11)*D11))/D3), 0)
    J3 = math.floor((M10-((J11)*D11))/D3)
    K3 = math.floor((M6-(0.5*2*K7)-(K7*D7)-((K11+K12-(2*K7))*G11))/G3)
    L3 = math.floor((M8-(0.5*2*L7)-(L7*D7)-((L11+L12-(2*L7))*G11))/G3)

    # BRD
    I4 = max(math.floor((I3/2)-(2*((I9-M4)+K7+L7))), 0)
    J4 = max(J3+(2*(I9-M4)), 0)
    K4 = math.floor((K3/2)+(2*K7))
    L4 = L3+(2*L7)


    # FS
    I6=math.floor(M12/15+1)
    J6=math.floor(M10/F6)
    K6=M6/F6
    L6=math.floor(M8/15)

    # DS
    I5 =math.floor((I4+(I4-I4/(critical_percent/100+1.2))+(I6*2))/4)
    J5 =math.floor((J4+(J4-J4/(critical_percent/100+1.2))+(J6*2))/4)
    K5 =math.floor((K4+(K4-K4/(critical_percent/100+1.2))+(K6*2))/4)
    L5 =math.floor((L4+(L4-L4/(critical_percent/100+1.2))+(L6*2))/4)

    # TS
    K8=6*K7
    L8=6*L7


    # EMH Fire
    J10=math.floor(M10/C10)
    L10=math.floor(M8/C10)

    # BRD

    Rotation_H7 = 2
    Rotation_C15 = 0
    Rotation_D15 = 0
    Rotation_H15 = 0
    Rotation_I15 = 0

    aw_nb = [I3+K3, J3+L3]
    brd_nb = [0, I4+K4, Rotation_H7, J4+L4-Rotation_H7]
    ds_nb = [I5+K5, J5+L5]
    fs_nb = [I6+K6, J6+L6]
    atc_nb = [K7, M4]
    ts_nb = [K8, L8]
    emh_nb = [J10+L10]
    nm_nb = [Rotation_C15, Rotation_D15, I11 + K11, max(K12, 0), Rotation_H15, Rotation_I15, J11 + L11, L12]

    return [aw_nb, brd_nb, ds_nb, fs_nb, atc_nb, ts_nb, emh_nb, nm_nb]


def print_global(param):
    print(param)


def calculate_brd_ds_nm(m_total_attack, mastery_increase, damage_with_percent_pur, emh_total, brd_nb, ds_nb, nm_nb):
    brd_damage = ((58 + m_total_attack * 1.99 * mastery_increase * 1.2) * 1 * damage_with_percent_pur * 1.25 * brd_nb[
        0]) + \
                 ((58 + m_total_attack * 1.99 * mastery_increase * 1.2) * (
                         1 + 0.35) * damage_with_percent_pur * 1.25 * brd_nb[1]) + \
                 ((58 + emh_total * 1.99 * mastery_increase * 1.2) * 1 * damage_with_percent_pur * 1.25 * brd_nb[2]) + \
                 ((58 + emh_total * 1.99 * mastery_increase * 1.2) * (1 + 0.35) * damage_with_percent_pur * 1.25 *
                  brd_nb[3])

    dragonsong_damage = ((122 + m_total_attack * 4.2 * mastery_increase) * (0.35 + 1) * damage_with_percent_pur * ds_nb[
        0]) + \
                        ((122 + emh_total * 4.2 * mastery_increase) * (0.35 + 1) * damage_with_percent_pur * ds_nb[1])

    nm_ice = ((115 + m_total_attack * 8.57 * mastery_increase) * 1 * damage_with_percent_pur * nm_nb[0]) + \
             ((115 + m_total_attack * 8.57 * mastery_increase) * (1 + 0.35) * damage_with_percent_pur * nm_nb[1]) + \
             ((115 + m_total_attack * 8.57 * mastery_increase) * (1 + 0.35) * damage_with_percent_pur * 1.6 * nm_nb[
                 2]) + \
             ((115 + m_total_attack * 8.57 * mastery_increase) * (
                     1 + 0.35) * damage_with_percent_pur * 1.65 * 1.3 * nm_nb[3]) + \
             ((115 + emh_total * 8.57 * mastery_increase) * 1 * damage_with_percent_pur * nm_nb[4]) + \
             ((115 + emh_total * 8.57 * mastery_increase) * (1 + 0.35) * damage_with_percent_pur * nm_nb[5]) + \
             ((115 + emh_total * 8.57 * mastery_increase) * (1 + 0.35) * damage_with_percent_pur * 1.6 * nm_nb[6]) + \
             ((115 + emh_total * 8.57 * mastery_increase) * (1 + 0.35) * damage_with_percent_pur * 1.65 * 1.3 * nm_nb[
                 7])
    return [brd_damage, dragonsong_damage, nm_ice]


def calculate_aw_fs_atc_ts_emh_damage(m_total_attack, damage_with_percent_pur, aw_nb, emh_total, fs_nb, atc_nb, ts_nb, emh_nb, print):
    aw_damage = (((6 + m_total_attack * 0.21277) * 2) + (
            6 + m_total_attack * 0.273)) * 1 * damage_with_percent_pur * aw_nb[0] + (((6 + emh_total * 0.21277) * 2) + (
            6 + emh_total * 0.273)) * 1 * damage_with_percent_pur * aw_nb[1]
    print("")
    print("AW : " + str(aw_damage))

    fs_damage = ((26 + m_total_attack * 0.75) * 1 * damage_with_percent_pur * fs_nb[0]) + (
            (26 + emh_total * 0.75) * 1 * damage_with_percent_pur * fs_nb[1])
    print("FS : " + str(fs_damage))

    atc_damage = ((28 + m_total_attack * 1.25) * 1 * damage_with_percent_pur * atc_nb[0]) + \
                 ((28 + emh_total * 1.25) * 1 * damage_with_percent_pur * atc_nb[1])
    print("ATC : " + str(atc_damage))

    thundering_sky_damage = ((2 + m_total_attack * 0.3773) * 5 * 1 * damage_with_percent_pur * ts_nb[0]) + \
                            ((2 + emh_total * 0.3773) * 5 * 1 * damage_with_percent_pur * ts_nb[1])
    print("Thundering sky : " + str(thundering_sky_damage))

    emh_damage = ((15 + emh_total * 0.71) * 1 * damage_with_percent_pur * emh_nb[0])
    print("EMH : " + str(emh_damage))
    return [aw_damage, fs_damage, atc_damage, thundering_sky_damage, emh_damage]



def calculate_total_damage(aw_damage, brd_damage, dragonsong_damage, fs_damage, atc_damage, thundering_sky_damage, emh_damage, perception_percent, nm_ice, crit_damage, critical_percent):
    all_but_nm = aw_damage + brd_damage + dragonsong_damage + fs_damage + atc_damage + thundering_sky_damage + emh_damage
    all = all_but_nm + nm_ice
    total_damage = all_but_nm * (1 - perception_percent / 100) * 0.3 + \
                   nm_ice * (1.1 - perception_percent / 100) * 0.3 + \
                   all - (all_but_nm * (1 - perception_percent / 100) + nm_ice * (
            1.1 - perception_percent / 100))

    total_damage_with_crit = (((all_but_nm - brd_damage) - (all_but_nm - brd_damage) * (1 - perception_percent / 100)) * (crit_damage * ((critical_percent - (critical_percent*(1-perception_percent/100)))/100)/100 + 1)) +\
                             (((all_but_nm - brd_damage)*(1-perception_percent/100)*0.3)) +\
                             ((nm_ice - nm_ice * (0.9 - perception_percent/100))) * (crit_damage * ((critical_percent - (critical_percent*(1-perception_percent/100)))/100)/100 + 1) +\
                             (nm_ice * (0.9 - perception_percent / 100) * 0.3) +\
                             ((brd_damage - (brd_damage * (1 - perception_percent / 100) * 0.3)) * (crit_damage * ((critical_percent - (critical_percent*(1-perception_percent/100)))/100)/100 + 1)) +\
                             (brd_damage * (1 - perception_percent/100) * 0.3)
    return [total_damage, total_damage_with_crit]


def calculate_dps(stats: Stats, print = lambda x: None):
    global dps_total_calls
    global dps_cached_calls


    magical_attack = stats.magical_attack + stats.magical_attack_skill
    magic_power = stats.magic_power + stats.magical_power_skill

    m_total_attack = magical_attack * (magic_power / 13 / 100 + 1)
    mastery_increase = stats.mastery / 9.3 / 100 + 1
    emh_total = magical_attack * (magic_power / 13 / 100 + 1.2)
    perception_percent = stats.perception_percent() #(stats.perception / 16.5 + 80) + stats.perception_one_percent
    haste_percent = stats.haste_percent() #stats.haste * (1 + stats.haste_eight_percent * 0.08) / 13.5 + 8
    critical_percent = stats.critical_percent() #stats.magic_critical_hit * 0.0643 - 0.0171
    damage_with_percent_pur = 1 + stats.five_percent_twelve_meter * 0.05
    crit_damage = stats.critical_hit_damage_percent + stats.critical_damage_three_percent * 3


    dps_key = tuple([magical_attack, magic_power, m_total_attack, mastery_increase, emh_total, perception_percent, haste_percent, critical_percent, damage_with_percent_pur, crit_damage])
    if dps_key in dps_cache:
        dps_cached_calls += 1
        return dps_cache[dps_key]

    dps_total_calls += 1

    print("damage_with_percent_pur : " + str(damage_with_percent_pur))
    print("crit_damage : " + str(crit_damage))

    print("emh_total : " + str(emh_total))
    print("m_total_attack : " + str(m_total_attack))
    print("mastery_increase : " + str(mastery_increase))

    print("")

    print("Perception : " + str(perception_percent))
    print("Haste : " + str(haste_percent))
    print("Critical % : " + str(critical_percent))

    print("")

    global attack_numbers_total_calls
    global attack_numbers_cached_calls
    global brd_ds_nm_numbers_total_calls
    global brd_ds_nm_numbers_cached_calls
    global calculate_aw_fs_atc_ts_emh_damage_total_calls
    global calculate_aw_fs_atc_ts_emh_damage_cached_calls
    global calculate_total_damage_numbers_total_calls
    global calculate_total_damage_numbers_cached_calls

    # Sheet report
    # key = str(haste_percent) + ' ' + str(critical_percent)
    key = tuple([str(haste_percent), str(critical_percent)])
    if not key in attack_numbers_cache:
        attack_numbers_total_calls += 1
        attack_numbers_cache[key] = calculate_freq(haste_percent, critical_percent)
    else:
        attack_numbers_cached_calls += 1
    [aw_nb, brd_nb, ds_nb, fs_nb, atc_nb, ts_nb, emh_nb, nm_nb] = attack_numbers_cache[key]

    # key = ' '.join(map(lambda x:str(x), [m_total_attack, mastery_increase, damage_with_percent_pur, emh_total, brd_nb, ds_nb, nm_nb]))
    key = tuple([m_total_attack, mastery_increase, damage_with_percent_pur, emh_total, tuple(brd_nb), tuple(ds_nb), tuple(nm_nb)])
    if not key in brd_ds_nm_numbers_cache:
        brd_ds_nm_numbers_total_calls += 1
        brd_ds_nm_numbers_cache[key] = calculate_brd_ds_nm(m_total_attack, mastery_increase, damage_with_percent_pur, emh_total, brd_nb, ds_nb, nm_nb)
    else:
        brd_ds_nm_numbers_cached_calls += 1
    [brd_damage, dragonsong_damage, nm_ice] = brd_ds_nm_numbers_cache[key]

    print("BRD : " + str(brd_damage))
    print("Dragonsong : " + str(dragonsong_damage))
    print("NM Icy Melody : " + str(nm_ice))

    # key = ' '.join(map(lambda x:str(x), [m_total_attack, damage_with_percent_pur, aw_nb, emh_total, fs_nb, atc_nb, ts_nb, emh_nb]))
    key = tuple([m_total_attack, damage_with_percent_pur, tuple(aw_nb), emh_total, tuple(fs_nb), tuple(atc_nb), tuple(ts_nb), tuple(emh_nb)])
    if not key in calculate_aw_fs_atc_ts_emh_damage_numbers_cache:
        calculate_aw_fs_atc_ts_emh_damage_total_calls += 1
        calculate_aw_fs_atc_ts_emh_damage_numbers_cache[key] = calculate_aw_fs_atc_ts_emh_damage(m_total_attack, damage_with_percent_pur, aw_nb, emh_total, fs_nb, atc_nb, ts_nb, emh_nb, print)
    else:
        calculate_aw_fs_atc_ts_emh_damage_cached_calls += 1
    [aw_damage, fs_damage, atc_damage, thundering_sky_damage, emh_damage] = calculate_aw_fs_atc_ts_emh_damage_numbers_cache[key]

    # key = ' '.join(map(lambda x: str(x), [aw_damage, brd_damage, dragonsong_damage, fs_damage, atc_damage, thundering_sky_damage, emh_damage, perception_percent, nm_ice, crit_damage, critical_percent]))
    key = tuple([aw_damage, brd_damage, dragonsong_damage, fs_damage, atc_damage, thundering_sky_damage, emh_damage, perception_percent, nm_ice, crit_damage, critical_percent])
    if not key in calculate_total_damage_numbers_cache:
        calculate_total_damage_numbers_total_calls += 1
        calculate_total_damage_numbers_cache[key] = calculate_total_damage(aw_damage, brd_damage, dragonsong_damage, fs_damage, atc_damage, thundering_sky_damage, emh_damage, perception_percent, nm_ice, crit_damage, critical_percent)
    else:
        calculate_total_damage_numbers_cached_calls += 1
    [total_damage, total_damage_with_crit] = calculate_total_damage_numbers_cache[key]


    print("old " + """aw_nb = [175, 56]
brd_nb = [0, 79, 2, 62]
ds_nb = [31, 21]
fs_nb = [15, 4]
atc_nb = [3, 2]
ts_nb = [18, 12]
emh_nb = [52]
nm_nb = [0, 0, 12.03, 3, 0, 0, 12, 3]""")

    print("new")
    print("aw_nb = " + str(aw_nb))
    print("brd_nb = " + str(brd_nb))
    print("ds_nb = " + str(ds_nb))
    print("fs_nb = " + str(fs_nb))
    print("atc_nb = " + str(atc_nb))
    print("ts_nb = " + str(ts_nb))
    print("emh_nb = " + str(emh_nb))
    print("nm_nb = " + str(nm_nb))


    aw_damage = (((6 + m_total_attack * 0.21277) * 2) + (
            6 + m_total_attack * 0.273)) * 1 * damage_with_percent_pur * aw_nb[0] + (((6 + emh_total * 0.21277) * 2) + (
            6 + emh_total * 0.273)) * 1 * damage_with_percent_pur * aw_nb[1]
    print("")
    print("AW : " + str(aw_damage))



    fs_damage = ((26 + m_total_attack * 0.75) * 1 * damage_with_percent_pur * fs_nb[0]) + (
            (26 + emh_total * 0.75) * 1 * damage_with_percent_pur * fs_nb[1])
    print("FS : " + str(fs_damage))

    atc_damage = ((28 + m_total_attack * 1.25) * 1 * damage_with_percent_pur * atc_nb[0]) + \
                 ((28 + emh_total * 1.25) * 1 * damage_with_percent_pur * atc_nb[1])
    print("ATC : " + str(atc_damage))

    thundering_sky_damage = ((2 + m_total_attack * 0.3773) * 5 * 1 * damage_with_percent_pur * ts_nb[0]) + \
                            ((2 + emh_total * 0.3773) * 5 * 1 * damage_with_percent_pur * ts_nb[1])
    print("Thundering sky : " + str(thundering_sky_damage))

    emh_damage = ((15 + emh_total * 0.71) * 1 * damage_with_percent_pur * emh_nb[0])
    print("EMH : " + str(emh_damage))



    print("")

    all_but_nm = aw_damage + brd_damage + dragonsong_damage + fs_damage + atc_damage + thundering_sky_damage + emh_damage
    all = all_but_nm + nm_ice
    total_damage = all_but_nm * (1 - perception_percent / 100) * 0.3 + \
                   nm_ice * (1.1 - perception_percent / 100) * 0.3 + \
                   all - (all_but_nm * (1 - perception_percent / 100) + nm_ice * (
            1.1 - perception_percent / 100))

    total_damage_with_crit = (((all_but_nm - brd_damage) - (all_but_nm - brd_damage) * (1 - perception_percent / 100)) * (crit_damage * ((critical_percent - (critical_percent*(1-perception_percent/100)))/100)/100 + 1)) +\
                             (((all_but_nm - brd_damage)*(1-perception_percent/100)*0.3)) +\
                             ((nm_ice - nm_ice * (0.9 - perception_percent/100))) * (crit_damage * ((critical_percent - (critical_percent*(1-perception_percent/100)))/100)/100 + 1) +\
                             (nm_ice * (0.9 - perception_percent / 100) * 0.3) +\
                             ((brd_damage - (brd_damage * (1 - perception_percent / 100) * 0.3)) * (crit_damage * ((critical_percent - (critical_percent*(1-perception_percent/100)))/100)/100 + 1)) +\
                             (brd_damage * (1 - perception_percent/100) * 0.3)
    dps_cache[dps_key] = (total_damage, total_damage_with_crit)

    return dps_cache[dps_key]


def generate_svg(nodes, coord_map, astral_tree, txt_map, stats, points, after_stats, temps):
    circle_size = 10
    out = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1500" height="1100">\n'
    interline = 20
    start = [20, 20]
    out += '<text x="' + str(start[0]) + '" y="' + str(start[1]) + '">Optimized for : </text>\n'
    out += '<text x="' + str(start[0]) + '" y="' + str(start[1] + interline * 1) + '">Astral points : ' + str(points) + '</text>\n'
    out += '<text x="' + str(start[0]) + '" y="' + str(start[1] + interline * 3) + '">Stats : </text>\n'
    out += '<text x="' + str(start[0]) + '" y="' + str(start[1] + interline * 4) + '">Skill : ' + str(stats.skill) + '</text>\n'
    out += '<text x="' + str(start[0]) + '" y="' + str(start[1] + interline * 5) + '">Magic attack : ' + str(stats.magical_attack) + '</text>\n'
    out += '<text x="' + str(start[0]) + '" y="' + str(start[1] + interline * 6) + '">Magic power : ' + str(stats.magic_power) + '</text>\n'
    out += '<text x="' + str(start[0]) + '" y="' + str(start[1] + interline * 7) + '">Mastery : ' + str(stats.mastery) + '</text>\n'
    out += '<text x="' + str(start[0]) + '" y="' + str(start[1] + interline * 8) + '">Critical : ' + str(int(stats.critical_percent()*100)/100) + '%</text>\n'
    out += '<text x="' + str(start[0]) + '" y="' + str(start[1] + interline * 9) + '">Perception : ' + str(int(stats.perception_percent()*100)/100) + '%</text>\n'
    out += '<text x="' + str(start[0]) + '" y="' + str(start[1] + interline * 10) + '">Haste : ' + str(int(stats.haste_percent()*100)/100) + '%</text>\n'

    out += '<text x="' + str(start[0]) + '" y="' + str(start[1] + interline * 12) + '">DPS : ' + str(int(calculate_dps(after_stats)[1]/temps)) + '</text>\n'

    out += '<text x="' + str(start[0] + 150) + '" y="' + str(start[1] + interline * 3) + '">Stats after : </text>\n'
    out += '<text x="' + str(start[0] + 150) + '" y="' + str(start[1] + interline * 4) + '">Skill : ' + str(after_stats.skill) + '</text>\n'
    out += '<text x="' + str(start[0] + 150) + '" y="' + str(start[1] + interline * 5) + '">Magic attack : ' + str(after_stats.magical_attack + after_stats.magical_attack_skill) + '</text>\n'
    out += '<text x="' + str(start[0] + 150) + '" y="' + str(start[1] + interline * 6) + '">Magic power : ' + str(after_stats.magic_power + after_stats.magical_power_skill) + '</text>\n'
    out += '<text x="' + str(start[0] + 150) + '" y="' + str(start[1] + interline * 7) + '">Mastery : ' + str(after_stats.mastery) + '</text>\n'
    out += '<text x="' + str(start[0] + 150) + '" y="' + str(start[1] + interline * 8) + '">Critical : ' + str(int(after_stats.critical_percent()*100)/100) + '%</text>\n'
    out += '<text x="' + str(start[0] + 150) + '" y="' + str(start[1] + interline * 9) + '">Perception : ' + str(int(after_stats.perception_percent()*100)/100) + '%</text>\n'
    out += '<text x="' + str(start[0] + 150) + '" y="' + str(start[1] + interline * 10) + '">Haste : ' + str(int(after_stats.haste_percent()*100)/100) + '%</text>\n'
    circles = ''
    lines = ''
    for node in txt_map.keys():
        if node in coord_map:
            color = "black" if node in nodes else "lightgray"
            real_circle_size = circle_size if len(coord_map[node]) < 3 else circle_size/coord_map[node][2]
            circles += '<circle cx="' + str(coord_map[node][0]) + '" cy="' + str(coord_map[node][1]) + '" r="' + str(real_circle_size) + '" fill="' + color + '"/>\n'

            node_name = 'node_' + str(node)
            if node_name in globals():
                func_node = globals()[node_name]
                if func_node in astral_tree:
                    for second_node in astral_tree[func_node]:
                        second_node_name = second_node.__name__
                        second_node_name = second_node_name.replace('node_', '')
                        if second_node_name in coord_map:
                            color = "black" if second_node_name in nodes else "lightgray"
                            lines += '<line x1="' + str(coord_map[node][0]) + '" y1="' + str(coord_map[node][1]) + '" x2="' + str(coord_map[second_node_name][0]) + '" y2="' + str(coord_map[second_node_name][1]) + '" stroke="' + color + '"/>\n'
    out += lines + circles + '</svg>'

    return out


def main():
    l_stats = Stats()

    # Base stats 60 current
    # l_stats.skill = 303
    # l_stats.magical_attack = 305
    # l_stats.magic_power = 257
    # l_stats.mastery = 288
    # l_stats.magic_critical_hit = 221
    # l_stats.critical_hit_damage_percent = 60
    # l_stats.perception = 166
    # l_stats.haste = 186

    # skapoil
    # l_stats.skill = 321
    # l_stats.magical_attack = 321
    # l_stats.magic_power = 273
    # l_stats.mastery = 357
    # l_stats.magic_critical_hit = 211
    # l_stats.critical_hit_damage_percent = 60
    # l_stats.perception = 157
    # l_stats.haste = 207

    maxp = 0
    input_file = 'input_stats.txt'
    print('Reading ' + input_file)
    with open(input_file, 'r') as f:
        for line in f.readlines():
            print(line)
            line = line.replace('\n','').replace(' ', '').replace('  ', '').split('=')
            print(line)
            if line[0] in Stats.__dict__:
                l_stats.__dict__[line[0]] = int(line[1])
            elif line[0] == 'astral_points':
                maxp = int(line[1])

    # ska pas poil
    # l_stats.skill = 332
    # l_stats.magical_attack = 337
    # l_stats.magic_power = 281
    # l_stats.mastery = 406
    # l_stats.magic_critical_hit = 241
    # l_stats.critical_hit_damage_percent = 60
    # l_stats.perception = 177
    # l_stats.haste = 207
    # l_stats.five_percent_twelve_meter = 1

    # Base stats 75 current
    # l_stats.skill = 332
    # l_stats.magical_attack = 320
    # l_stats.magic_power = 268
    # l_stats.mastery = 300
    # l_stats.magic_critical_hit = 266
    # l_stats.critical_hit_damage_percent = 60
    # l_stats.perception = 256
    # l_stats.haste = 284

    # l_stats.five_percent_twelve_meter = 1

    print()
    print("avant0")
    print(l_stats)
    print()

    # Base dps
    (damage, damage_with_crit) = calculate_dps(l_stats, lambda x: print(x))
    print("damage : " + str(damage))
    print("damage with crit : " + str(damage_with_crit))
    print("dps : " + str(damage_with_crit / temps))

    # sys.exit(0)

    #astral_tree = [node_1, [[node_2, [[node_3, [[node_4, [[node_5, [[node_6, [[node_7, [[node_8, [[node_8_1_0, []], [node_8_2_0, []]]]]]]]]]]]]]]]]]

    # astral_tree_bis = {node_0: [node_1],
    #                    node_1: [node_2],
    #                    node_2: [node_3],
    #                    node_3: [node_4],
    #                    node_4: [node_5],
    #                    node_5: [node_6],
    #                    node_6: [node_7],
    #                    node_7: [node_8],
    #                    node_8: [node_8_1_0, node_8_2_0],
    #                    node_8_1_0: [],
    #                    node_8_2_0: [node_8_2_1],
    #                    }

    astral_tree_bis = {node_0: [node_1],
                       node_1: [node_2],
                       node_2: [node_3],
                       node_3: [node_4],
                       node_4: [node_5],
                       node_5: [node_6],
                       node_6: [node_7],
                       node_7: [node_8],
                       node_8: [node_8_1_0, node_8_2_0],
                       node_8_1_0: [],
                       node_8_2_0: [node_8_2_1],
                       node_8_2_1: [node_8_2_2],
                       node_8_2_2: [node_8_2_3],
                       node_8_2_3: [node_8_2_3_1_0, node_8_2_3_2_0],
                       node_8_2_3_1_0: [node_8_2_3_1_1],
                       node_8_2_3_1_1: [node_8_2_3_1_2],
                       node_8_2_3_1_2: [node_8_2_3_1_3],
                       node_8_2_3_1_3: [node_8_2_3_1_4],
                       node_8_2_3_1_4: [node_8_2_3_1_5],
                       node_8_2_3_1_5: [node_8_2_3_1_6],
                       node_8_2_3_1_6: [node_8_2_3_1_7],
                       node_8_2_3_1_7: [node_8_2_3_1_7_1_0, node_8_2_3_1_7_2_0],
                       node_8_2_3_1_7_1_0: [],
                       node_8_2_3_1_7_2_0: [node_8_2_3_1_7_2_1],
                       node_8_2_3_1_7_2_1: [node_8_2_3_1_7_2_2],
                       node_8_2_3_1_7_2_2: [node_8_2_3_1_7_2_3],
                       node_8_2_3_1_7_2_3: [node_8_2_3_1_7_2_4],
                       node_8_2_3_1_7_2_4: [node_8_2_3_1_7_2_5],
                       node_8_2_3_1_7_2_5: [node_8_2_3_1_7_2_6],
                       node_8_2_3_1_7_2_6: [node_8_2_3_1_7_2_7],
                       node_8_2_3_1_7_2_7: [node_8_2_3_1_7_2_8],
                       node_8_2_3_1_7_2_8: [node_8_2_3_1_7_2_9],
                       node_8_2_3_1_7_2_9: [node_8_2_3_1_7_2_10],
                       node_8_2_3_1_7_2_10: [],
                       node_8_2_3_2_0: [node_8_2_3_2_1],
                       node_8_2_3_2_1: [node_8_2_3_2_2],
                       node_8_2_3_2_2: [node_8_2_3_2_2_1_0, node_8_2_3_2_2_2_0],
                       node_8_2_3_2_2_1_0: [node_8_2_3_2_2_1_0_1_0, node_8_2_3_2_2_1_0_2_0],
                       node_8_2_3_2_2_1_0_1_0: [], # root
                       node_8_2_3_2_2_1_0_2_0: [node_8_2_3_2_2_1_0_2_1],
                       node_8_2_3_2_2_1_0_2_1: [node_8_2_3_2_2_1_0_2_2],
                       node_8_2_3_2_2_1_0_2_2: [node_8_2_3_2_2_1_0_2_3],
                       node_8_2_3_2_2_1_0_2_3: [node_8_2_3_2_2_1_0_2_4],
                       node_8_2_3_2_2_1_0_2_4: [node_8_2_3_2_2_1_0_2_5],
                       node_8_2_3_2_2_1_0_2_5: [node_8_2_3_2_2_1_0_2_6],
                       node_8_2_3_2_2_1_0_2_6: [node_8_2_3_2_2_1_0_2_7],
                       node_8_2_3_2_2_1_0_2_7: [node_8_2_3_2_2_1_0_2_8],
                       node_8_2_3_2_2_1_0_2_8: [node_8_2_3_2_2_1_0_2_9],
                       node_8_2_3_2_2_1_0_2_9: [node_8_2_3_2_2_1_0_2_10],
                       node_8_2_3_2_2_1_0_2_10: [node_8_2_3_2_2_1_0_2_11],
                       node_8_2_3_2_2_1_0_2_11: [node_8_2_3_2_2_1_0_2_12],
                       node_8_2_3_2_2_1_0_2_12: [],
                       node_8_2_3_2_2_2_0: [node_8_2_3_2_2_2_1],
                       node_8_2_3_2_2_2_1: [node_8_2_3_2_2_2_2],
                       node_8_2_3_2_2_2_2: [node_8_2_3_2_2_2_3],
                       node_8_2_3_2_2_2_3: [node_8_2_3_2_2_2_4],
                       node_8_2_3_2_2_2_4: [node_8_2_3_2_2_2_4_1_0, node_8_2_3_2_2_2_4_2_0],
                       node_8_2_3_2_2_2_4_1_0: [node_8_2_3_2_2_2_4_1_1],
                       node_8_2_3_2_2_2_4_1_1: [node_8_2_3_2_2_2_4_1_2],
                       node_8_2_3_2_2_2_4_1_2: [node_8_2_3_2_2_2_4_1_3],
                       node_8_2_3_2_2_2_4_1_3: [node_8_2_3_2_2_2_4_1_4],
                       node_8_2_3_2_2_2_4_1_4: [node_8_2_3_2_2_2_4_1_5],
                       node_8_2_3_2_2_2_4_1_5: [], # crit %
                       node_8_2_3_2_2_2_4_2_0: [node_8_2_3_2_2_2_4_2_1],
                       node_8_2_3_2_2_2_4_2_1: [node_8_2_3_2_2_2_4_2_2],
                       node_8_2_3_2_2_2_4_2_2: [node_8_2_3_2_2_2_4_2_3],
                       node_8_2_3_2_2_2_4_2_3: [node_8_2_3_2_2_2_4_2_4],
                       node_8_2_3_2_2_2_4_2_4: [node_8_2_3_2_2_2_4_2_5],
                       node_8_2_3_2_2_2_4_2_5: [node_8_2_3_2_2_2_4_2_6],
                       node_8_2_3_2_2_2_4_2_6: [node_8_2_3_2_2_2_4_2_7],
                       node_8_2_3_2_2_2_4_2_7: [node_8_2_3_2_2_2_4_2_8],
                       node_8_2_3_2_2_2_4_2_8: [node_8_2_3_2_2_2_4_2_9],
                       node_8_2_3_2_2_2_4_2_9: [node_8_2_3_2_2_2_4_2_10],
                       node_8_2_3_2_2_2_4_2_10: []
                       }

    txt_map = {"1": "hp : 108", "2": "haste : 13", "3": "perception : 13", "4": "magical_attack : 3", "5": "physical_defence : 7", "6": "skill : 5", "7": "mastery : 13", "8": "magic_critical_hit : 13", "8_1_0": "five_percent_twelve_meter : 1", "8_2_0": "mastery : 13", "8_2_1": "magic_power : 13", "8_2_2": "magic_critical_hit : 13", "8_2_3": "hp : 108", "8_2_3_1_0": "hp : 108", "8_2_3_1_1": "magic_critical_hit : 13", "8_2_3_1_2": "haste : 13", "8_2_3_1_3": "magical_defence : 7", "8_2_3_1_4": "magical_attack : 3", "8_2_3_1_5": "perception : 13", "8_2_3_1_6": "skill : 5", "8_2_3_1_7": "magic_power : 13", "8_2_3_1_7_1_0": "aoe reduc", "8_2_3_1_7_2_0": "mastery : 13", "8_2_3_1_7_2_1": "perception : 13", "8_2_3_1_7_2_2": "magic_power : 13", "8_2_3_1_7_2_3": "hp : 108", "8_2_3_1_7_2_4": "skill : 5", "8_2_3_1_7_2_5": "magic_critical_hit : 13", "8_2_3_1_7_2_6": "haste : 13", "8_2_3_1_7_2_7": "magical_defence : 7", "8_2_3_1_7_2_8": "haste_eight_percent : 1", "8_2_3_1_7_2_9": "haste_eight_percent : 1", "8_2_3_1_7_2_10": "haste_eight_percent : 1", "8_2_3_2_0": "magical_defence : 7", "8_2_3_2_1": "skill : 5", "8_2_3_2_2": "magical_attack : 3", "8_2_3_2_2_1_0": "physical_defence : 7", "8_2_3_2_2_1_0_1_0": "root chance", "8_2_3_2_2_1_0_2_0": "hp : 108", "8_2_3_2_2_1_0_2_1": "mastery : 13", "8_2_3_2_2_1_0_2_2": "magic_critical_hit : 13", "8_2_3_2_2_1_0_2_3": "perception : 13", "8_2_3_2_2_1_0_2_4": "magic_power : 13", "8_2_3_2_2_1_0_2_5": "magical_defence : 7", "8_2_3_2_2_1_0_2_6": "magical_attack : 3", "8_2_3_2_2_1_0_2_7": "haste : 13", "8_2_3_2_2_1_0_2_8": "perception_one_percent : 1", "8_2_3_2_2_1_0_2_9": "perception_one_percent : 1", "8_2_3_2_2_1_0_2_10": "perception_one_percent : 1", "8_2_3_2_2_1_0_2_11": "perception_one_percent : 1", "8_2_3_2_2_1_0_2_12": "perception_one_percent : 1", "8_2_3_2_2_2_0": "magic_power : 13", "8_2_3_2_2_2_1": "skill : 5", "8_2_3_2_2_2_2": "haste : 13", "8_2_3_2_2_2_3": "perception : 13", "8_2_3_2_2_2_4": "hp : 108", "8_2_3_2_2_2_4_1_0": "magical_defence : 7", "8_2_3_2_2_2_4_1_1": "mastery : 13", "8_2_3_2_2_2_4_1_2": "magical_attack : 3", "8_2_3_2_2_2_4_1_3": "critical_hit_damage_percent : 1", "8_2_3_2_2_2_4_1_4": "critical_hit_damage_percent : 1", "8_2_3_2_2_2_4_1_5": "critical_hit_damage_percent : 1", "8_2_3_2_2_2_4_2_0": "haste : 13", "8_2_3_2_2_2_4_2_1": "skill : 5", "8_2_3_2_2_2_4_2_2": "magic_critical_hit : 13", "8_2_3_2_2_2_4_2_3": "perception : 13", "8_2_3_2_2_2_4_2_4": "physical_defence : 7", "8_2_3_2_2_2_4_2_5": "magical_attack : 3", "8_2_3_2_2_2_4_2_6": "magic_power : 13", "8_2_3_2_2_2_4_2_7": "mastery : 13", "8_2_3_2_2_2_4_2_8": "critical_damage_three_percent : 1", "8_2_3_2_2_2_4_2_9": "critical_damage_three_percent : 1", "8_2_3_2_2_2_4_2_10": "critical_damage_three_percent : 1"}

    coord_map = {"1": [490, 99], "2": [544, 95], "3": [575, 41], "4": [604, 78], "5": [667, 21], "6": [699, 95], "7": [581, 172], "8": [549, 226], "8_1_0": [459, 190], "8_2_0": [574, 261], "8_2_1": [523, 297], "8_2_2": [589, 356], "8_2_3": [569, 437], "8_2_3_1_0": [352, 510], "8_2_3_1_1": [339, 575], "8_2_3_1_2": [267, 536], "8_2_3_1_3": [234, 714], "8_2_3_1_4": [295, 705], "8_2_3_1_5": [319, 767], "8_2_3_1_6": [217, 780], "8_2_3_1_7": [218, 867], "8_2_3_1_7_1_0": [327, 936], "8_2_3_1_7_2_0": [132, 827], "8_2_3_1_7_2_1": [109, 886], "8_2_3_1_7_2_2": [60, 788], "8_2_3_1_7_2_3": [105, 728], "8_2_3_1_7_2_4": [45, 687], "8_2_3_1_7_2_5": [108, 604], "8_2_3_1_7_2_6": [37, 565], "8_2_3_1_7_2_7": [87, 525], "8_2_3_1_7_2_8": [34, 401], "8_2_3_1_7_2_9": [9, 401, 2], "8_2_3_1_7_2_10": [34, 377, 2], "8_2_3_2_0": [689, 479], "8_2_3_2_1": [634, 520], "8_2_3_2_2": [668, 557], "8_2_3_2_2_2_0": [554, 642], "8_2_3_2_2_2_1": [596, 674], "8_2_3_2_2_2_2": [546, 702], "8_2_3_2_2_2_3": [609, 760], "8_2_3_2_2_2_4": [616, 841], "8_2_3_2_2_2_4_1_0": [580, 868], "8_2_3_2_2_2_4_1_1": [580, 920], "8_2_3_2_2_2_4_1_2": [563, 971], "8_2_3_2_2_2_4_1_3": [521, 1029], "8_2_3_2_2_2_4_1_4": [497, 1029, 2], "8_2_3_2_2_2_4_1_5": [521, 1053, 2], "8_2_3_2_2_2_4_2_0": [712, 700], "8_2_3_2_2_2_4_2_1": [777, 735], "8_2_3_2_2_2_4_2_2": [848, 683], "8_2_3_2_2_2_4_2_3": [899, 777], "8_2_3_2_2_2_4_2_4": [994, 800], "8_2_3_2_2_2_4_2_5": [1053, 759], "8_2_3_2_2_2_4_2_6": [1149, 859], "8_2_3_2_2_2_4_2_7": [1210, 868], "8_2_3_2_2_2_4_2_8": [1262, 997], "8_2_3_2_2_2_4_2_9": [1238, 997, 2], "8_2_3_2_2_2_4_2_10": [1262, 1021, 2], "8_2_3_2_2_1_0": [796, 562], "8_2_3_2_2_1_0_1_0": [787, 612], "8_2_3_2_2_1_0_2_0": [862, 500], "8_2_3_2_2_1_0_2_1": [913, 552], "8_2_3_2_2_1_0_2_2": [977, 577], "8_2_3_2_2_1_0_2_3": [1036, 550], "8_2_3_2_2_1_0_2_4": [1048, 500], "8_2_3_2_2_1_0_2_5": [1107, 533], "8_2_3_2_2_1_0_2_6": [1168, 502], "8_2_3_2_2_1_0_2_7": [1177, 447], "8_2_3_2_2_1_0_2_8": [1334, 471], "8_2_3_2_2_1_0_2_9": [1334, 447, 2], "8_2_3_2_2_1_0_2_10": [1358, 471, 2], "8_2_3_2_2_1_0_2_11": [1334, 495, 2], "8_2_3_2_2_1_0_2_12": [1310, 471, 2]}

    # test_opti(stats, astral_tree, 0, 29)
    # maxp = 15

    print()
    print("avant1")
    print(l_stats)
    print()

    # for maxp in range(0, 75):
    for maxp in range(maxp, maxp+1):
        start = time.time()
        global final_trees
        global final_trees_signatures
        global all_signatures
        global global_steps

        final_trees = []
        final_trees_signatures = []
        all_signatures = set()
        global_steps = 0

        test_opti_2(copy.deepcopy(l_stats), astral_tree_bis, 0, maxp, [node_0], [])

        print(global_steps, time.time() - start)


        # return

        sort_order = {}
        for tree in final_trees:
            sort_order[signature(tree[0])] = tree[1][1]

        final_trees.sort(key=lambda val: sort_order[signature(val[0])])

        ordered_trees = list(reversed(final_trees))

        # for tree in ordered_trees:
        #     print(tree[1][1]/temps, tree[0])

        print_all = True

        global attack_numbers_total_calls
        global attack_numbers_cached_calls
        global brd_ds_nm_numbers_total_calls
        global brd_ds_nm_numbers_cached_calls
        global calculate_aw_fs_atc_ts_emh_damage_total_calls
        global calculate_aw_fs_atc_ts_emh_damage_cached_calls
        global calculate_total_damage_numbers_total_calls
        global calculate_total_damage_numbers_cached_calls
        global dps_total_calls
        global dps_cached_calls

        print('attack_numbers', attack_numbers_total_calls, attack_numbers_cached_calls)
        print('brd_ds_nm_numbers', brd_ds_nm_numbers_total_calls, brd_ds_nm_numbers_cached_calls)
        print('aw_fs_atc_ts_emh_damage', calculate_aw_fs_atc_ts_emh_damage_total_calls, calculate_aw_fs_atc_ts_emh_damage_cached_calls)
        print('total_damage_numbers', calculate_total_damage_numbers_total_calls, calculate_total_damage_numbers_cached_calls)
        print('dps_calls', dps_total_calls, dps_cached_calls)

        if print_all:
            print()
            print(global_steps)
            print()
            print(ordered_trees[0][1][1]/temps)
            print(ordered_trees[0][0])
            print("apres")
            print(ordered_trees[0][2])
            # print("avant")
            # print(l_stats)
            print("diff")
            print(ordered_trees[0][2] - l_stats)
            print()

            for node in sorted(ordered_trees[0][0]):
                print(node + ' => ' + ('' if not node in txt_map else txt_map[node]))

            print()
            (damage, damage_with_crit) = calculate_dps(ordered_trees[0][2], lambda x: print(x))
            print("damage : " + str(damage))
            print("damage with crit : " + str(damage_with_crit))
            print("dps : " + str(damage_with_crit / temps))

            print()
            svg = generate_svg(ordered_trees[0][0], coord_map, astral_tree_bis, txt_map, l_stats, maxp, ordered_trees[0][2], temps)
            print(svg)

            out_file = str(maxp).zfill(2) + '_' + 'astral_tree.svg'
            with open(out_file, 'w') as f:
                f.write(svg)

            webbrowser.open('file://' + os.path.realpath(out_file))
            print()
            print("dps : " + str(damage_with_crit / temps))
            print("global_steps " + str(global_steps))

        else:
            print(maxp, len(ordered_trees))
            print(ordered_trees[0][1][1]/temps, ordered_trees[0])

    for node in txt_map.keys():
        if node not in coord_map:
            print(node)


if __name__ == '__main__':
    main()
