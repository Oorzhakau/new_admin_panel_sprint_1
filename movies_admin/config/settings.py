from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

base_settings = [
    "components/common.py",
    "components/database.py",
]

include(*base_settings)
