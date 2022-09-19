from split_settings.tools import include
from dotenv import load_dotenv

load_dotenv()

base_settings = [
    'components/common.py',
    'components/database.py',
]

include(*base_settings)
