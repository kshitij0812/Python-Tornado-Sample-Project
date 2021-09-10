from os.path import dirname, join
from os import getenv
from dotenv import load_dotenv
import asyncpg
import asyncio

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

ks_book_details = '''
CREATE TABLE ks_book_details(
    ID SERIAL NOT NULL,
    book_title VARCHAR(50) NOT NULL,
    book_subtitle VARCHAR(50) NOT NULL,
    book_lang VARCHAR(10) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(13) NOT NULL,
    edition VARCHAR(10) NOT NULL,
    orig_price NUMERIC(7,2) NOT NULL,
    curr_price NUMERIC(7,2) NOT NULL,
    book_volume INTEGER,
    date_created TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
    PRIMARY KEY (ID)
);
'''

'''
This table is used to track, at which book what type of activity was performed at which time.
    • book_id                   : ID of books at which any activity was performed by the user
    • activity_type             : Store which type of operation was performed. The following are the activity with their integer keys
                                    1. Add new book            : 1
                                    3. Update book             : 2
    • date_updated              : The time at which the user perform any activity at the book
'''

ks_tracking_book_project_activities = '''
    CREATE TABLE ks_tracking_book_project_activities (
        ID SERIAL NOT NULL,
        book_id INTEGER NOT NULL,
        activity_type INTEGER NOT NULL,
        date_created TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC') NOT NULL,
        PRIMARY KEY (ID),
        FOREIGN KEY (book_id) REFERENCES ks_book_details(ID)
    );
'''

async def addMainTables(pool):
    """
    This function is used to create the all mentioned table
    """
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(ks_book_details)
            await connection.execute(ks_tracking_book_project_activities)


async def main():
    PG_CONFIG = {
        'user': getenv('DB_USER'),
        'pass': getenv('DB_PASS'),
        'host': getenv('DB_HOST'),
        'database': getenv('DB_NAME'),
        'port': getenv('DB_PORT')
    }
    PG_CONFIG['dsn'] = "postgres://%s:%s@%s:%s/%s" % (PG_CONFIG['user'], PG_CONFIG['pass'], PG_CONFIG['host'], PG_CONFIG['port'], PG_CONFIG['database'])
    pool = await asyncpg.create_pool(PG_CONFIG['dsn'], min_size=1, max_size=2)
    await addMainTables(pool)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
