from adhell.server import create_app
from adhell.utils import get_config


if __name__ == '__main__':
    create_app(get_config()).run(port=7000, debug=True)
