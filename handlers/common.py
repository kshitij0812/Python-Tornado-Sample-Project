from tornado.web import RequestHandler


class Homepage(RequestHandler):
    async def get(self):    
        self.render("homepage.html")


class BookList(RequestHandler):
    async def get(self):    
        self.render("book_list.html")


class ActivityHistory(RequestHandler):
    async def get(self):    
        self.render("activity_history.html")
