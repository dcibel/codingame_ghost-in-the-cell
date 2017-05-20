import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def log(message):
    print >> sys.stderr, message
    
from collections import namedtuple
Factory = namedtuple('Factory', ['id', 'owner', 'cyborgs_count', 'production'])
Troop = namedtuple('Troop', ['id', 'owner', 'origin', 'destination', 'count', 'turns_before_arrival'])
distances_by_couple = dict()
remaining_bombs = 2
troops = []
factories = []

def get_distance(factory_a, factory_b):
    return distances_by_couple[(factory_a, factory_b)]
    
def get_troop_balance_for_factory(factory_id):
    log(factory_id)
    factory = [f for f in factories if f.id == factory_id][0]
    balance = factory.cyborgs_count if factory.owner == 1 else -1 * factory.cyborgs_count
    
    for troop in [t for t in troops if t.destination == factory_id]:
        balance = balance + troop.owner * troop.count
    return balance    

factory_count = int(raw_input())  # the number of factories
link_count = int(raw_input())  # the number of links between factories
for i in xrange(link_count):
    factory_1, factory_2, distance = [int(j) for j in raw_input().split()]
    distances_by_couple[(factory_1, factory_2)] = distance
    distances_by_couple[(factory_2, factory_1)] = distance

# game loop
while True:
    factories = []
    troops = []
    im_sending_a_bomb = False
    entity_count = int(raw_input())  # the number of entities (e.g. factories and troops)
    for i in xrange(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = raw_input().split()
        entity_id = int(entity_id)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        arg_5 = int(arg_5)
        if entity_type == "FACTORY":
            factory = Factory(entity_id, arg_1, arg_2, arg_3)
            factories.append(factory)
            log("factory: {}".format(factory))
        elif entity_type == "TROOP":
            troop = Troop(entity_id, arg_1, arg_2, arg_3, arg_4, arg_5)
            troops.append(troop)
            log("troop")
        elif entity_type == "BOMB":
            owner = arg_1
            if owner == 1:
                im_sending_a_bomb = True
        else:
            raise Exception("Unknown entity type")

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."
    
    my_factories = [f for f in factories if f.owner == 1]
    his_factories = [f for f in factories if f.owner == -1]
    neutral_factories = [f for f in factories if f.owner == 0]
    
    target_factories = his_factories + [f for f in neutral_factories if f.production > 0]
    
    if len(target_factories) == 0:
        print "WAIT"
        continue
    
    if len(my_factories) == 0:
        print "WAIT"
        continue

    orders = []
    for source_factory in my_factories:
        reachable_targets = sorted(target_factories, key=lambda f: get_distance(source_factory.id, f.id))[:3]
        #ordered_targets = sorted(target_factories, key=lambda f: f.cyborgs_count)
        ordered_targets = sorted(reachable_targets, key=lambda f: get_troop_balance_for_factory(f.id))
        #ordered_targets = sorted(target_factories, key=lambda f: get_distance(source_factory.id, f.id))
        #for target_factory in ordered_targets[:3]:
        for target_factory in ordered_targets[:3]:
            #cyborgs = 2
            cyborgs = abs(get_troop_balance_for_factory(target_factory.id)) + 2
            orders.append("MOVE {} {} {}".format(source_factory.id, target_factory.id, cyborgs))
            
        if remaining_bombs > 0 and not im_sending_a_bomb:
            his_reachable_factories = [f for f in his_factories if get_distance(source_factory.id, f.id) < 3]
            if len(his_reachable_factories) > 0:
                most_dangerous_factory = max(his_reachable_factories, key=lambda f:f.cyborgs_count)
                orders.append("BOMB {} {}".format(source_factory.id,most_dangerous_factory.id))
        
    print "; ".join(orders)
