"""
Config options
"""

from boot import *

THE = o(
    char=o(sep=",",
           num="$",
           less="<",
           more=">",
           skip="?",
           klass="!",
           doomed=r'([\n\t\r ]|#.*)'),
    div=o(trivial=1.05,
          cohen=0.3,
          min=0.5,
          ),
    tree = o(minObs = 2,
             rnd = 1)
)
