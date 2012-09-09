import math

# ADJUST THE LASER POWER
LASER_POWER_DENOM = 1.0

# POSITIONAL BOUNDARIES OF THE GALVOS
# XXX: Normally set to 28000 each. Changed for presentation. 
MAX_X = 13000
MIN_X = -20000
MAX_Y = 17000
MIN_Y = 0

# MAX COLOR VALUE HARDWARE ALLOWS
CMAX = 65535


"""
GAME PARAMETERS
"""
MAX_NUM_ENEMIES = 3 # XXX: 5, 8
MAX_NUM_BULLETS = 30

"""
ENTITY HEALTH
"""
SHIP_IS_INVINCIBLE = False
SHIP_HEALTH_MAX = 100
SHIP_HEALTH_ASTEROID_HIT = 10
ASTEROID_HEALTH_MAX = 30
ASTEROID_HEALTH_BULLET_HIT = 10

"""
BLANKING AND TRACKING
	- Point stream algorithm tweaks
"""
BLANK_SAMPLE_PTS = 30 # XXX: Blanking needs serious work
SHOW_TRACKING_PATH = False
TRACKING_SAMPLE_PTS = 12

"""
SIZES
"""
SHIP_SIZE = 800 # 2500/2 # FIXME: Bad 'size' calculation. 
ASTEROID_MIN_RADIUS = 1500 # 1400
ASTEROID_MAX_RADIUS = 3500 # 2500

"""
PARTICLE EFFECTS
"""
PARTICLE_SPAWN_MIN = 3
PARTICLE_SPAWN_MAX = 5
PARTICLE_LIFE_MIN = 15
PARTICLE_LIFE_MAX = 30

"""
SPEEDS AND VELOCITIES
"""
ASTEROID_VEL_MAG_MAX = 100
ASTEROID_VEL_MAG_MIN = 50
ASTEROID_SPIN_VEL_MAG_MAX = math.pi / 70
ASTEROID_SPIN_VEL_MAG_MIN = math.pi / 400
BULLET_SPEED = 3000
PARTICLE_MAX_X_VEL = 500
PARTICLE_MIN_X_VEL = -500
PARTICLE_MAX_Y_VEL = 500
PARTICLE_MIN_Y_VEL = -500

"""
ENTITY DRAWING SPECIFICS
"""
BULLET_DO_BLANKING = True
BULLET_EDGE_SAMPLE_PTS = 7
BULLET_LENGTH = 400
SHIP_EDGE_SAMPLE_PTS = 12
SHIP_VERTEX_SAMPLE_PTS = 2
SQUARE_EDGE_SAMPLE_PTS = 12
SQUARE_VERTEX_SAMPLE_PTS = 5

HEALTHBAR_X_POS = 20000
HEALTHBAR_Y_POS = 24000
HEALTHBAR_EDGE_SAMPLE_PTS = 7
HEALTHBAR_VERTEX_SAMPLE_PTS = 10

"""
PRESUMABLY UNUSED GLOBALS BLOW
-- REMOVE THESE WHEN REFACTOR TIME
-- REMOVE THESE WHEN REFACTOR TIME
-- REMOVE THESE WHEN REFACTOR TIME
-- REMOVE THESE WHEN REFACTOR TIME
"""


"""
NASTY GLOBALS
The gui will alter these.
"""

# XXX: Needs to increase proportionally to radius
BALL_SAMPLE_PTS = 20
TRIANGLE_EDGE_SAMPLE_PTS = 20

PAUSE_START_PTS = 9 # 8 seems optimum
PAUSE_END_PTS = 9 # 8 seems optimum
CIRCLE_ROTATIONS = 1
BOUNCE_VEL_MIN = 75
BOUNCE_VEL_MAX = 500

PADDLE_WIDTH = 1000
PADDLE_HEIGHT = 2000
BALL_RADIUS = 2500

balls = [] # TODO: REFACTOR
PLAYERS = []

SIMPLE_TRANSLATION_SPD = 800



