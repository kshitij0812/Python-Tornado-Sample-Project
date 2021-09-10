from tornado.web import escape, RequestHandler


class ManageBook(RequestHandler):
    async def get(self):
        """
        This function is used to get the below mentioned data.
            1. book details
            2. activity hostory 
        """        

        action = self.get_argument('action')

        if action == 'get_book_details':
            book_id = int(self.get_argument('book_id'))

            async with self.settings['pool'].acquire() as connection:
                q = '''
                    SELECT ID, book_title, book_subtitle, book_lang, author, isbn, edition, orig_price::FLOAT, curr_price::FLOAT, book_volume 
                    FROM ks_book_details 
                    WHERE ID = $1;
                    '''
                db_result_book_details = await connection.fetchrow(q, book_id)

            response_ds = dict()
            if db_result_book_details:
                response_ds['status'] = True
                response_ds['data'] =  [db_result_book_details['id'], db_result_book_details['book_title'], db_result_book_details['book_subtitle'], db_result_book_details['book_lang'], db_result_book_details['author'], db_result_book_details['isbn'], db_result_book_details['edition'], db_result_book_details['orig_price'], db_result_book_details['curr_price'], db_result_book_details['book_volume']]
            else:
                response_ds['msg'] = 'Data not available'
            return self.write(escape.json_encode(response_ds))

        elif action == 'get_activity_history':
            async with self.settings['pool'].acquire() as connection:
                q = '''
                    SELECT KBD.ID, KBD.book_title, KBD.book_subtitle, KTBPA.activity_type, KTBPA.date_created::TEXT 
                    FROM ks_book_details AS KBD
                    INNER JOIN ks_tracking_book_project_activities AS KTBPA ON  KTBPA.book_id = KBD.ID
                    ORDER BY KTBPA.ID DESC;
                    '''
                db_result_activity_history = await connection.fetch(q)

            response_ds = dict()
            if db_result_activity_history:
                response_ds['status'] = True
                response_ds['data'] = [[_['id'], _['book_title'], _['book_subtitle'], _['activity_type'], _['date_created']] for _ in db_result_activity_history]
            else:
                response_ds['msg'] = 'Data not available'
            return self.write(escape.json_encode(response_ds))

    async def post(self):
        """
        This function is used to get the below mentioned data.
            1. delete the book using book id
        """

        action = self.get_argument('action')

        if action == 'delete_book':
            book_id = int(self.get_body_argument('book_id'))

            async with self.settings['pool'].acquire() as connection:
                async with connection.transaction():
                    q = "DELETE FROM ks_tracking_book_project_activities WHERE book_id = $1;"
                    await connection.execute(q, book_id)
                    q = "DELETE FROM ks_book_details WHERE ID = $1;"
                    await connection.execute(q, book_id)
            response_ds = {
                'status': True,
                'msg': 'Book deleted.'
            }
            return self.write(escape.json_encode(response_ds))
            

class BookList(RequestHandler):
    """
    This handler is used to get the list of various books.
    """
    async def get(self):
        response_ds = {
            'status': False
        }

        async with self.settings['pool'].acquire() as connection:
            q = '''
                SELECT ID, book_title, book_subtitle, book_lang, author, isbn, edition, orig_price::FLOAT, curr_price::FLOAT, book_volume, date_created::TEXT 
                FROM ks_book_details 
                ORDER BY ID;
                '''
            db_result_book_list = await connection.fetch(q)
        
        if db_result_book_list:
            data = list()
            for _ in db_result_book_list:
                data.append(
                    [_['id'], _['book_title'], _['book_subtitle'], _['book_lang'], _['author'], _['isbn'], _['edition'], _['orig_price'], _['curr_price'], _['book_volume'], _['date_created']]
                )
            response_ds['status'] = True
            response_ds['data'] = data
        else:
            response_ds['msg'] = 'Data not available'
        return self.write(escape.json_encode(response_ds))

class AddBook(RequestHandler):
    """
    This handler is used to add/edit the book details.
    If book is available in argument then we edit the book ID.
    Ptherwise we add a new book. 
    """

    async def post(self):
        book_id = self.get_argument('book_id', None)

        book_title = self.get_body_argument('book_title')
        book_subtitle = self.get_body_argument('book_subtitle')
        book_lang = self.get_body_argument('book_lang')
        author = self.get_body_argument('author')
        isbn = self.get_body_argument('isbn')
        edition = self.get_body_argument('edition')
        orig_price = float(self.get_body_argument('orig_price'))
        curr_price = float(self.get_body_argument('curr_price'))
        book_volume = int(self.get_body_argument('book_volume'))
        
        response_ds = {
            'status': False
        }

        async with self.settings['pool'].acquire() as connection:
            async with connection.transaction():
                if book_id is None:
                    q = '''
                        INSERT INTO ks_book_details
                            (book_title, book_subtitle, book_lang, author, isbn, edition, orig_price, curr_price, book_volume)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                        RETURNING ID;
                        '''
                    book_id = await connection.fetchval(q, book_title, book_subtitle, book_lang, author, isbn, edition, orig_price, curr_price, book_volume)
                    activity_code = 1
                else:
                    book_id = int(book_id)
                    q = '''
                        UPDATE ks_book_details 
                        SET book_title = $1, book_subtitle = $2, book_lang = $3, author = $4, isbn = $5, edition = $6, orig_price = $7, curr_price = $8, book_volume = $9
                        WHERE ID = $10;
                        '''
                    await connection.execute(q, book_title, book_subtitle, book_lang, author, isbn, edition, orig_price, curr_price, book_volume, book_id)
                    activity_code = 2

                q = "INSERT INTO ks_tracking_book_project_activities (book_id, activity_type) VALUES ($1, $2)"
                await connection.execute(q, book_id, activity_code)
        
        if book_id:
            response_ds['status'] = True
            response_ds['msg'] = "Book created successfully."
        else:
            response_ds['msg'] = "Something went wrong."

        return self.write(escape.json_encode(response_ds))
