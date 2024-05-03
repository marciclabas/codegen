# BEGIN
from typing import Literal

Rank = Literal[
  # LOOP RANK
  'RANK',
  # END
]

CLEARANCE_LEVEL = int # DELETE (just to make mypy happy)
# LOOP RANK CLEARANCE_LEVEL
class RANK:
  clearance_level: CLEARANCE_LEVEL

# END
# END