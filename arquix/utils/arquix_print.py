from enum import Enum

class AqColors(Enum):
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def aq_print(msg: str, color: AqColors = AqColors.BLUE):
    print(color.value + AqColors.BOLD.value + msg + AqColors.END.value)

