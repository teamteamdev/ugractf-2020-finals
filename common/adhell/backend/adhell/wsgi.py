from adhell.server import create_app
from adhell.utils import get_config

app = create_app(get_config())
