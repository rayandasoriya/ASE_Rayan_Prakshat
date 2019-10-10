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
    div=o(trivial=1.025,
          cohen=0.3,
          min=0.5)
)
