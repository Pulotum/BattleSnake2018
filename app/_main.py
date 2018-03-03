import bottle
import os
import random
import math

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

#define tracker variables
finder = AStarFinder();

# ---------- ---------- ----------
# - Make Map
# ----------
# return matrix of the field
#
# ---------- ---------- ----------
def makeMap(data):

     w = data['width'];
     h = data['height'];
     
     map = [];

     i = 0;
     while(i < h):
          map.append([0] * w);
          i = i + 1;

     for snek in data["snakes"]:
          for s in snek["body"]:
               map[s["x"]][s["y"]] = 1;
                    
     return Grid(matrix=map);

# ---------- ---------- ----------
# - Get closest food object
# ----------
# returns array of closest food item
#
# ---------- ---------- ----------
def getClosestFood(data, grid):

    #get my snake coords
    uid = data["you"];
    snakes = data["snakes"];
    for snek in snakes:
        if(snek["id"] == uid):
            me = snek;     
    meX = me["coords"][0][0];
    meY = me["coords"][0][1];

    #define top contender
    closestCord = [];
    closestDist = 100;

    #check each food in array
    for item in data["food"]:
        currentX = abs(meX - item[0]);
        currentY = abs(meY - item[1]);
          
        currentDist = currentX + currentY;

        #if current point is closer
        if(currentDist < closestDist):
            #check path exists
            path, runs = finder.find_path((meX,meY), (item[0], item[1]), grid);
               if len(path) > 0:
                    closestDist = currentDist;
                    closestCord = item;
          
    print ("me -", meX, meY);
    print ("closestCord -", closestCord);
     
    return closestCord;

@bottle.route('/')
def static():
    return "the server is running";               

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/');


@bottle.post('/start')
def start():
    '''
     data = bottle.request.json;
     game_id = data['game_id'];
     board_width = data['width'];
     board_height = data['height'];
     '''
     
     head_url = 'https://thumb1.shutterstock.com/display_pic_with_logo/88356/107460737/stock-photo-beautiful-expressive-adorable-happy-cute-laughing-smiling-baby-infant-face-showing-tongue-isolated-107460737.jpg';
     
     # TODO: Do things with data
     
     return {
          'color': '#ff6666',
          'taunt': 'BABY GUNNA WIN',
          'head_url': head_url,
          'name': 'Baby Face',
          'head_type': 'safe',
          'tail_type': 'pixel'
     };

# ---------- ---------- ----------
# - main movement function
# ----------
# this will be run every turn
#
# ---------- ---------- ----------
@bottle.post('/move')
def move():
     
     data = bottle.request.json;
     
     '''
     uid = data["you"];
     snakes = data["snakes"];
     
     for snek in snakes:
          if(snek["id"] == uid):
               me = snek;
          
     meX = me["coords"][0][0];
     meY = me["coords"][0][1];

     #grid = makeMap(data);
     
     #closestCord = getClosestFood(data, grid);
          
     if((closestCord[0] < meX)):
          movement = 'left';
          wantedSquare = [meX - 1, meY];
     elif((closestCord[0] > meX)):
          movement = 'right';
          wantedSquare = [meX + 1, meY];
     elif((closestCord[1] > meY)):
          movement = 'down';
          wantedSquare = [meX, meY + 1];
     elif((closestCord[1] < meY)):
          movement = 'up';
          wantedSquare = [meX, meY - 1];

     print ("wanted movement -", movement);
     
     '''     
     return {
          'move': 'up'
     };

# ---------- ---------- ----------
# - End Call
# ----------
# this will be called once the match has ended
#
# ---------- ---------- ----------     
@bottle.post('/end')
def end():
     data = bottle.request.json;

     # TODO: Do things with data

     return {
          'taunt': 'BABY FACE!'
     };


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app();
if __name__ == '__main__':
     bottle.run(
          application, 
          host=os.getenv('IP', '0.0.0.0'), 
          port=os.getenv('PORT', '8080'),
          debug = True);
