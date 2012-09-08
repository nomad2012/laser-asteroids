# ADJUST THE LASER POWER
LASER_POWER_DENOM = 1.0

# POSITIONAL BOUNDARIES OF THE GALVOS
MAX_X = 30000
MIN_X = -30000
MAX_Y = 30000
MIN_Y = -30000

# MAX COLOR VALUE HARDWARE ALLOWS
CMAX = 65535

# POINT STREAM ALGORITHM VARIABLES
SHOW_BLANKING_PATH = False
BLANK_SAMPLE_PTS = 12

"""
ENTITY SPECIFIC
"""
BULLET_EDGE_SAMPLE_PTS = 20
SQUARE_EDGE_SAMPLE_PTS = 20

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



