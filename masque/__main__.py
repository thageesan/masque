import argparse
from masque import create_app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev', help='spins up the environment in development mode', action='store_true')
    args = parser.parse_args()
    if args.dev:
        create_app('dev_config.ini')
    else:
        create_app('config.ini')
