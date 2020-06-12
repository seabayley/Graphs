from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}


def reverse_direction(direction):
    directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    return directions[direction]


room_list = {player.current_room.id: {}}
for direction in player.current_room.get_exits():
    room_list[player.current_room.id][direction] = '?'

rooms_left = {}
rooms_left[player.current_room.id] = player.current_room.get_exits()


def has_unexplored_room(room):
    found_unexplored = False
    for v in room.values():
        if v == '?':
            found_unexplored = True
    return found_unexplored


def is_hallway(last_room, next_room):
    hallway = False
    num_exits = []
    for key in room_graph[next_room][1]:
        if room_graph[next_room][1][key] != last_room:
            num_exits.append(room_graph[next_room][1][key])

    if len(num_exits) == 0:
        return True
    elif len(num_exits) == 1:
        last_room = next_room
        next_room = num_exits[0]
        return is_hallway(last_room, next_room)
    else:
        return False


def get_next(room):
    available = [x for x in room_list[room] if room_list[room][x] == '?']
    for direction in available:
        next_room = room_graph[room][1][direction]
        num_exits = len(room_graph[next_room][1])
        if is_hallway(room, next_room):
            return direction
    if room_list[room].get('w') == '?':
        return 'w'
    elif room_list[room].get('n') == '?':
        return 'n'
    elif room_list[room].get('e') == '?':
        return 'e'
    elif room_list[room].get('s') == '?':
        return 's'


while len(rooms_left) > 0:
    if '?' in room_list[player.current_room.id].values():
        next_room = None
        current_room = player.current_room.id
        next_room = get_next(current_room)
        rooms_left[player.current_room.id].remove(next_room)
        if rooms_left[player.current_room.id] == []:
            del rooms_left[player.current_room.id]
        player.travel(next_room)
        new_room = player.current_room.id
        traversal_path.append(next_room)
        if new_room not in room_list:
            room_list[new_room] = {
                x: '?' for x in player.current_room.get_exits()}
        room_list[current_room][next_room] = new_room
        room_list[new_room][reverse_direction(next_room)] = current_room
        for direction, room in room_list[new_room].items():
            if room == '?':
                rooms_left.setdefault(new_room, []).append(direction)
        if new_room in rooms_left.keys() and reverse_direction(next_room) in rooms_left[new_room]:
            rooms_left[new_room].remove(reverse_direction(next_room))
            if rooms_left[new_room] == []:
                del rooms_left[new_room]
    else:
        starting_room = player.current_room.id
        queue = []
        for direction, room in room_list[starting_room].items():
            queue.append([[direction, room]])
        while len(queue) > 0:
            path = queue.pop(0)
            room = path[-1]
            if has_unexplored_room(room_list[room[1]]):
                for direction, room in path:
                    player.travel(direction)
                    traversal_path.append(direction)
                break
            else:
                for direction, room in room_list[room[1]].items():
                    if room is not starting_room and room not in [y for x, y in path]:
                        queue.append(list(path) + [[direction, room]])

    # TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


'''
#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
'''
