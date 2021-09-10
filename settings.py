import asyncpg
from dotenv import load_dotenv
from os import getenv
from os.path import dirname, join

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PG_CONFIG = {
    'user': getenv('DB_USER'),
    'pass': getenv('DB_PASS'),
    'host': getenv('DB_HOST'),
    'database': getenv('DB_NAME'),
    'port': getenv('DB_PORT')
}
PG_CONFIG['dsn'] = "postgres://%s:%s@%s:%s/%s" % (PG_CONFIG['user'], PG_CONFIG['pass'],
                                                  PG_CONFIG['host'], PG_CONFIG['port'], PG_CONFIG['database'])


async def get_config():
    config = {
        'template_path': 'template',
        'static_path': 'static',
        'debug': True,
        'pool': await asyncpg.create_pool(PG_CONFIG['dsn'])
    }
    return config
