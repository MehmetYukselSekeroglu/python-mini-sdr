import sqlite3
from sigint_lib import db_tools
from sigint_lib import app_env

DB_FILE = "sigint.sqlite3"
APP_IMAGE_FILE = "logo.png"


APP_TITLE = "sigint-ui-project"
APP_VENDOR = "Prime Security"


db = sqlite3.connect(database=DB_FILE, check_same_thread=False)
db_cursor = db.cursor()


result = db_tools.systemDB_make_schema(
    sqlite_db_object=db,
    sqlite_db_cursor=db_cursor
)

print(result)


result = db_tools.load_blob_from_db(
    key=app_env.KEY_DB__APP_ICON,
    value_binary_data=db_tools.file_to_binary(APP_IMAGE_FILE)["data"],
    data_type=app_env.DB_DATA_TYPE__SYSTEM,sqlite_db_cursor=db_cursor,sqlite_db_object=db
)


print(result)


result = db_tools.load_key_and_value_from_SYSTEM_CORE_DB(
    key=app_env.KEY_DB__APP_TITLE,
    value=APP_TITLE,
    sqlite_db_cursor=db_cursor,
    sqlite_db_object=db
)


print(result)


result = db_tools.load_key_and_value_from_SYSTEM_CORE_DB(
    key=app_env.KEY_DB__APP_VENDOR,
    value=APP_VENDOR,
    sqlite_db_cursor=db_cursor,
    sqlite_db_object=db
)


print(result)





