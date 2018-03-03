import bottle
import os
import random
import math

#takes data
#returns 2d array of map
#   [o,o,o]
#   [1,o,o]
#   [o,o,o]
def makeMap(data):
    
    w = data.get('width')
    h = data.get('height')
    
    map = []
    
    i = 0
    while i < h:
        map.append(['0'] * w)
        i = i + 1
      
    for snake in data.get('snakes').get('data'):
        for snek in snake.get('body').get('data'):
            map[snek.get('x')][snek.get('y')] = 's'

    for snake in data.get('you').get('body').get('data'):
        map[snek.get('x')][snek.get('y')] = 'm'
          
    return map

#takes data
#return [x,y] array of cords
def getClosestFood(data):
    
    meX = data.get('you').get('body').get('data')[0].get('x')
    meY = data.get('you').get('body').get('data')[0].get('y')
    
    closestCord = []
    closestDist = 1000
    
    for f in data.get('food').get('data'):
        curX = abs(meX - f.get('x'))
        curY = abs(meY - f.get('y'))
        curDist = curY + curX
        
        if curDist < closestDist:
            closestDist = curDist
            closestCord = [f.get('x'),f.get('y')]
    
    return closestCord

#takes map, [me], [food]
#return bool
def doesPathExist(map, me, food):
    return True

#takes [me] and [food]
#return direction
def getDir(me, food, last):

    if (me[1] > food[1]) and (last != 'up'):
        dir = 'up'
    elif (me[1] < food[1]) and (last != 'down'):
        dir = 'down'
    elif (me[0] > food[0]) and (last != 'left'):
        dir = 'left'
    elif (me[0] < food[0]) and (last != 'right'):
        dir = 'right'
        
    return dir

@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

    
@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = 'https://thumb1.shutterstock.com/display_pic_with_logo/88356/107460737/stock-photo-beautiful-expressive-adorable-happy-cute-laughing-smiling-baby-infant-face-showing-tongue-isolated-107460737.jpg'
    
    # TODO: Do things with data

    return {
        'color': '#FF6666',
        'taunt': 'BABY FACE WILL WIN',
        'head_url': head_url,
        '"head_type': 'pixel',
        'tail_type': 'pixel'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    me = [data.get('you').get('body').get('data')[0].get('x'),data.get('you').get('body').get('data')[0].get('y')]
    last = [data.get('you').get('body').get('data')[1].get('x'),data.get('you').get('body').get('data')[1].get('y')]
    
    last = getDir(last,me,'')
    
    print 'prev',last
    
    print 'me',me
    
    closest = getClosestFood(data);
    
    print 'close',closest
    
    dir = getDir(me,closest,last)
    
    print 'dir',dir
    
    map = makeMap(data)
    
    for m in map:
        print m
    
    # TODO: Do things with data
    
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    
    return {
        'move': dir,
        'taunt': 'BABY FACE'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
