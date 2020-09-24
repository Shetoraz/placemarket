import config
import dj_database_url
import psycopg2

db_info = dj_database_url.config(default=config.DATABASELINK)
connection = psycopg2.connect(database=db_info.get('NAME'),
		    		user=db_info.get('USER'),
		    		password=db_info.get('PASSWORD'),
		    		host=db_info.get('HOST'),
		    		port=db_info.get('PORT'))

def update_data(user_id, column, value):
    with connection:
        with connection.cursor() as cur:
            sql = "insert into {0} (user_id) values ({1}) on conflict (user_id) do update set {2} = '{3}'".format(config.remote_name, user_id, column, value)
            cur.execute(sql)

def fetch(user_id):
    with connection:
        with connection.cursor() as cur:
            cur.execute("SELECT category, city, title, description, price, photo, contacts FROM {} where user_id={}".format(config.remote_name, user_id))
            return cur.fetchone()

def get_current_state(user_id):
        with connection:
            with connection.cursor() as cur:
                cur.execute("select state from {} where user_id={}".format(config.remote_name, user_id))
                return cur.fetchone()[0]

def set_state(user_id, state_value):
    with connection:
        with connection.cursor() as cur:
            sql = "insert into {0} (user_id, state) values ({1}, '{2}') on conflict (user_id) do update set state='{2}'".format(config.remote_name, user_id, state_value)
            cur.execute(sql)