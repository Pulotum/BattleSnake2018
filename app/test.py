
map = [];

# init map
w = 5;
h = 5;
i = 0;
while(i < h):
	map.append(['0'] * w);
	i = i + 1;

		
me = [0,3];

snakes = [	[0,4],
			[0,0],
			[1,0],
			[2,0],
			[3,2],
			[3,3],
			[3,4]];
			
food = [[4,4]];

# add me to map
map[me[1]][me[0]] = "m";

# add snake to map
for s in snakes:
	map[s[1]][s[0]] = "s";

# add food to map
for f in food:
	map[f[1]][f[0]] = "f";

#print map
for pos in map:
	print(pos);

input("\nENTER TO END");
