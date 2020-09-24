from enum import Enum

token = "1162949489:AAE4Q8DLG_s_Kgz8xfrrWOhRRDyJBRiQ-T0"
admin_chat_id = 1266099533
name = "marketplaceby"
db_file = "database.vdb"
DATABASELINK = "postgres://usupsjjfwbzaex:2f6588fb27317944ea45665c5db330af993b86b029ef1fb3b297c85ad7055e91@ec2-54-247-89-181.eu-west-1.compute.amazonaws.com:5432/dcg3c38m5qoi9t"
remote_name = "announcement" 

class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_ENTER_CATEGORY = "1"
    S_ENTER_CITY = "2"
    S_SEND_TITLE = "3"
    S_SEND_DESCRIPTION = "4"
    S_SEND_PRICE = "5"
    S_SEND_PHOTO = "6"