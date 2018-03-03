
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


map = [];

# init map
w = 5;
h = 5;
i = 0;
while(i < h):
	map.append([0] * w);
	i = i + 1;

		
me = [0,3];

snakes = [
        [0,4],
	[0,0],
	[1,0],
	[2,0],
        [3,1],
	[3,2],
	[3,3],
	[3,4]
];
			
food1 = [4,4];
food2 = [2,1];

# add snake to map
for s in snakes:
	map[s[1]][s[0]] = 1;

#define grid with map
grid = Grid(matrix=map)

#define start and end
start = grid.node(me[0], me[1]);
end = grid.node(food2[0], food2[1]); #this will be closest food? maybe will go through all possible foods and get closest

#define tracking algorithim
finder = AStarFinder()
path, runs = finder.find_path(start, end, grid)


print('operations:', runs, 'path length:', len(path));
print(path);
if len(path) == 0:
        print('No move exists');
else:        
        print('Next Move:', path[1][0], 'x', path[1][1]);
print(grid.grid_str(path=path, start=start, end=end));


#input("\n\nENTER TO END");
