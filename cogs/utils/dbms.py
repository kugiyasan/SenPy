import sqlite3

def database(func):
    async def inner(*args):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        if len(args) == 1:
            answer = await func(args[0], c)
        else:
            answer = await func(args[0], c, *args)
        conn.commit()
        conn.close()
        print('database', answer)
        return answer
    return inner

class DB():
    def create_connection(self, db_file):
        return sqlite3.connect(db_file)

