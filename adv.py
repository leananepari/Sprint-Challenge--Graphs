from room import Room
from player import Player
from world import World
from util import Stack, Queue
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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
print('------------_ROOMS----------')
print(world.rooms[0].get_exits())

player = Player(world.starting_room)
print('PLAYER-------')
print(player.current_room.id)



# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def player_can_move(player, direction, room_id):
  if player.current_room.get_room_in_direction(direction) is not None:
    room = player.current_room.get_room_in_direction(direction)
    if room.id == room_id:
      return True
    else:
      return False
  else:
    return False

def find_path(start, end):
  queue = Queue()
  queue.enqueue([start])
  visited = set()

  while queue.size() > 0:
    path = queue.dequeue()
    vertex = path[-1]

    if vertex not in visited:
      if vertex == end:
        return path
      visited.add(vertex)

      for next_vert in room_graph[vertex][1]:
        new_path = list(path) 
        new_path.append(room_graph[vertex][1][next_vert])
        queue.enqueue(new_path)

def walk_the_path(path, player):
  exits = player.current_room.get_exits()
  index = 0

  while index < len(path) - 1:
    for i in exits:
      room = player.current_room.get_room_in_direction(i)
      if room.id == path[index + 1]:
        player.travel(i)
        traversal_path.append(i)
        exits = player.current_room.get_exits()
        index += 1
        break

def build_traversal_path(player, room_graph):
  stack = Stack()
  stack.push((player.current_room.id, 'null'))
  visited = {}

  while stack.size() > 0:

    t = stack.pop()
    vertex = t[0]
    direction = t[1]
    
    if vertex not in visited:
      visited[vertex] = direction

      if direction != 'null':
        if player_can_move(player, direction, vertex) is not False:
          player.travel(direction)
          traversal_path.append(direction)
        else:
          path = find_path(player.current_room.id, vertex)
          walk_the_path(path, player)

      for i in room_graph[vertex][1]:
        stack.push((room_graph[vertex][1][i], i))


build_traversal_path(player, room_graph)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


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
