from sigint_lib.app_env import *

INITRAL_COMMAND = f"""
CREATE TABLE IF NOT EXISTS {DB_SYSTEM_TABLE} (
    id INTEGER NOT NULL,
    unique_key TEXT NOT NULL UNIQUE,
    key_value TEXT NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS {DB_BLOB_STORAGE} (
    id INTEGER NOT NULL,
    unique_blob_key TEXT NOT NULL UNIQUE,
    key_value BLOB NOT NULL,
    data_type TEXT NOT NULL DEFAULT 'user',
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS {DB_FREQUENCY_TABLE} (
    id INTEGER NOT NULL,
    frequency_name TEXT NOT NULL UNIQUE,
    frequency INTEGER NOT NULL,
    modulation TEXT NOT NULL DEFAULT 'NFM',
    required_decoder TEXT DEFAULT NULL,
    bandwidth INTEGER NOT NULL DEFAULT '12500',
    user_notes TEXT DEFAULT NULL, 
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS {DB_ACCESS_TABLE} (
    id INTEGER NOT NULL,
    telegram_user_id TEXT(64) NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS {DB_LOCAL_AUTHENTICATE_TABLE} (
    id INTEGER NOT NULL,
    safe_username TEXT(64) NOT NULL UNIQUE,
    safe_password TEXT(64) NOT NULL,
    PRIMARY KEY("id")
);
"""









def systemDB_make_schema(sqlite_db_object, sqlite_db_cursor) -> dict:
    try:
        sqlite_db_cursor.executescript(INITRAL_COMMAND)
        sqlite_db_object.commit()
        
        return {
            "success": "true",
            "message": "database successfully configured"
        }
    
    
    except Exception as error_message:
        return {
            "success": "false",
            "message": str(error_message) 
            
        }
        
    
def file_to_binary(target_file_path) -> dict:
    try:
        with open(target_file_path, "rb") as target_file:
            binary_data = target_file.read()

        return {
            "success": "true",
            "data": binary_data
        }
        
    except Exception as err:
        return {
            "success": "false",
            "message": str(err)
        }
        
        
def load_blob_from_db(key:str,value_binary_data:bin,data_type:str, sqlite_db_object, sqlite_db_cursor) -> dict:

    
    
    STATIC_SQL_COMMAND = f"""SELECT * FROM {DB_BLOB_STORAGE} WHERE unique_blob_key=?"""
    STATIC_DATA_TUPLE = (key,)
    try:
        sqlite_db_cursor.execute(STATIC_SQL_COMMAND, STATIC_DATA_TUPLE)
        result_is = sqlite_db_cursor.fetchall()
        
        if len(result_is) != 0:
            UPDATE_KEY = True
        else:
            UPDATE_KEY = False
    
    except Exception as err:
        return {
            "success" : "false",
            "message" : str(err)
            
        }       
    
    
    
    if  UPDATE_KEY:
        STATIC_SQL_COMMAND = f"""UPDATE {DB_BLOB_STORAGE} SET key_value=? WHERE unique_blob_key=?"""
        STATIC_DATA_TUPLE = (value_binary_data,key)
        
        try:
            sqlite_db_cursor.execute(STATIC_SQL_COMMAND, STATIC_DATA_TUPLE)
            sqlite_db_object.commit()

            return {
                "success" : "true",
                "message" : f"{key} successfully update {DB_BLOB_STORAGE} database"
            }
        except Exception as err:
            return {
                "success" : "false",
                "message" : f"Error: failed to update {DB_BLOB_STORAGE} err: {err}"
                
            }


    STATIC_SQL_COMMAND = f"""INSERT INTO {DB_BLOB_STORAGE}
    ( unique_blob_key, key_value, data_type ) VALUES (?, ?, ?)  """
    
    STATIC_DATA_TUPLE = (key, value_binary_data, data_type )
    
    try:
        sqlite_db_cursor.execute(STATIC_SQL_COMMAND, STATIC_DATA_TUPLE)
        sqlite_db_object.commit()
        
        return {
            "success" : "true",
            "message" : "binary successfully loaded from database"
        }
    
    except Exception as err:
        return {
            "success" : "false",
            "message" : str(err)
            
        }
        
        
def load_key_and_value_from_SYSTEM_CORE_DB(
    key:str,
    value:str,
    sqlite_db_cursor,
    sqlite_db_object
    ) -> dict:
    
    
    STATIC_SQL_COMMAND = f"""SELECT * FROM {DB_SYSTEM_TABLE} WHERE unique_key=?"""
    STATIC_DATA_TUPLE = (key,)
    try:
        sqlite_db_cursor.execute(STATIC_SQL_COMMAND, STATIC_DATA_TUPLE)
        result_is = sqlite_db_cursor.fetchall()
        
        if len(result_is) != 0:
            UPDATE_KEY = True
        else:
            UPDATE_KEY = False
    
    except Exception as err:
        return {
            "success" : "false",
            "message" : str(err)
            
        }       
    
    
    
    if  UPDATE_KEY:
        STATIC_SQL_COMMAND = f"""UPDATE {DB_SYSTEM_TABLE} SET key_value=? WHERE unique_key=?"""
        STATIC_DATA_TUPLE = (value,key)
        
        try:
            sqlite_db_cursor.execute(STATIC_SQL_COMMAND, STATIC_DATA_TUPLE)
            sqlite_db_object.commit()

            return {
                "success" : "true",
                "message" : f"{key} successfully update {DB_SYSTEM_TABLE} database"
            }
        except Exception as err:
            return {
                "success" : "false",
                "message" : f"Error: failed to update {DB_SYSTEM_TABLE} err: {err}"
                
            }

            
            
    STATIC_SQL_COMMAND = """INSERT INTO system_core (unique_key, key_value)
    VALUES (? , ?)"""
    STATIC_DATA_TUPLE = (key, value )
    
    try:
        sqlite_db_cursor.execute(STATIC_SQL_COMMAND, STATIC_DATA_TUPLE)
        sqlite_db_object.commit()

        return {
            "success" : "true",
            "message" : f"{key} and {value} successfully load system_core database"
        }
    except Exception as err:
        return {
            "success" : "false",
            "message" : str(err)
            
        }
    
    
    
    



def get_value_sysmtemCore(key:str, sqlite_db_cursor, sqlite_db_object) -> dict :
    STATIC_SQL_COMMAND = f"""SELECT * FROM {DB_SYSTEM_TABLE} WHERE unique_key=?"""
    STATIC_DATA_TUPLE = (key, )
    
    try:
        data_value = sqlite_db_cursor.execute(STATIC_SQL_COMMAND, STATIC_DATA_TUPLE).fetchall()[0][2]
        return {
            "success" : "true",
            "data": data_value
        }
    
    except Exception as err:
        return {
            "success" : "false",
            "data": f"error: {err} " 
        }
    


def get_value_blobStorage(key:str, sqlite_db_cursor, sqlite_db_object) -> dict :
    STATIC_SQL_COMMAND = f"""SELECT * FROM {DB_BLOB_STORAGE} WHERE unique_blob_key=?"""
    STATIC_DATA_TUPLE = (key, )
    
    try:
        data_value = sqlite_db_cursor.execute(STATIC_SQL_COMMAND, STATIC_DATA_TUPLE).fetchall()[0][2]
        
        return {
            "success" : "true",
            "data": data_value
        }
    
    except Exception as err:
        return {
            "success" : "false",
            "data": f"error: {err} " 
        }
    






