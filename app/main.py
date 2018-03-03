import bottle
import os
import random
import math

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def makeMap(data):
    w = data.get('width')
    h = data.get('height')
    
    map = []
    
    i = 0
    while i < h:
        print i
        map.append([0] * w)
        i = i + 1
        
    print map[0]
    
    for snek in data.get('snakes'):
        for snuk in snek.get('data'):
            map[snuk[0], snuk[1]] = 1
            
    return map

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

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#FF6666',
        'taunt': 'BABY FACE WILL WIN',
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    meX = data.get('you').get('body').get('data')[0]
    meY = data.get('you').get('body').get('data')[1]
	
    print makeMap()
    
    # TODO: Do things with data
    
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    print direction
    return {
        'move': direction,
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
