import bottle
import os
import random
import math

#takes data
#return [x,y] array of cords
def getClosestFood(data):
    
    meX = data.get('you').get('body').get('data')[0].get('x')
    meY = data.get('you').get('body').get('data')[0].get('y')
    
    closestCord = []
    closestDist = 1000
    
    for f in data.get('food').get('data'):
        print 'food',f.get('x'),f.get('y')
        
        curX = abs(meX - f.get('x'))
        curY = abs(meY - f.get('y'))
        curDist = curY + curX
        
        if curDist < closestDist:
            closestDist = curDist
            closestCord = [f.get('x'),f.get('y')]
    
    print closestCord
    return closestCord

#takes [meX,meY] and [foodX,foodY]
#return direction
def getDir(me, food):
    if me[0] > food[0]:
        dir = 'down'
    if me[0] < food[0]:
        dir = 'up'
    if me[1] > food[1]:
        dir = 'left'
    if me[1] < food[1]:
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
    meX = data.get('you').get('body').get('data')[0].get('x')
    meY = data.get('you').get('body').get('data')[0].get('y')
	
    print meX, meY
    
    closest = getClosestFood(data);
    dir = getDir([meX,meY],closest)
    
    # TODO: Do things with data
    
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    print dir
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
