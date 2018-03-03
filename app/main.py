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

#takes [me] and [point] "last dir" "method" ['dir']
#return direction
def getDir(me, food, last, method, old):
    
    dir = 'up'
    
    #get next direction towards point
    if (me[1] > food[1]) and (last != 'down') and ('up' not in old):
        print 'up nit in old'
        dir = 'up'
    elif (me[1] < food[1]) and (last != 'up') and ('down' not in old):
        print 'down nit in old'
        dir = 'down'
    elif (me[0] > food[0]) and (last != 'right') and ('left' not in old):
        print 'left not in old'
        dir = 'left'
    elif (me[0] < food[0]) and (last != 'left') and ('right' not in old):
        print 'right not in old'
        dir = 'right'
    
    return dir

#takes [me] 'dir'
#return [new]
def nextPoint(me, dir):
    new = []
    
    if dir == 'up':
        new = [me[0],me[1]-1]
    elif dir == 'down':
        new = [me[0],me[1]+1]
    elif dir == 'left':
        new = [me[0]-1,me[1]]
    elif dir == 'right':
        new = [me[0]+1,me[1]]

    return new
    
#takes [point], ["past"]
#return bool for safety
def isSafe(data, point, old):

    safe = True
    #check if point is in snakes or me
    for snake in data.get('snakes').get('data'):
        for snek in snake.get('body').get('data'):
            if (point[0] == snek.get('x')) and (point[1] == snek.get('y')):
                safe = False

    for snake in data.get('you').get('body').get('data'):
        if (point[0] == snek.get('x')) and (point[1] == snek.get('y')):
            safe = False
    
    if len(old) > 3:
        return True
    
    if safe == False:
        return False
    else:
        return True;

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

    print '--------------------'
    print 'New Move'
    print '--------------------'

    data = bottle.request.json
    me = [data.get('you').get('body').get('data')[0].get('x'),data.get('you').get('body').get('data')[0].get('y')]
    last = [data.get('you').get('body').get('data')[1].get('x'),data.get('you').get('body').get('data')[1].get('y')]

    print 'prev - ',last
    print 'current - ',me
    
    closest = getClosestFood(data);
    print 'close food - ',closest
    
    last = getDir(last,me,'','old',[])
    print 'coming from - ',last
    
    dir = getDir(me,closest,last,'new',[])
    print 'going to - ',dir
    next = nextPoint(me, dir)
    print 'next - ',next
    
    result = isSafe(data, next, [])
    print 'is safe - ',result
    
    notSafe = []
    
    while result != True:
        print '--not safe--'
        
        notSafe.append(dir)
        print 'not safes - ', notSafe
        
        dir = getDir(me,closest,last,'new',notSafe)
        print 'new dir - ',dir
        
        next = nextPoint(me, dir)
        print 'new next - ',next
        
        result = isSafe(data, next, notSafe)
        print 'new result - ',result
    
    map = makeMap(data)
    
    '''
    for m in map:
        print m
    '''
    
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
