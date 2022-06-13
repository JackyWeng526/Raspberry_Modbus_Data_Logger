# %% Import packages or libraries
import pandas as pd
import numpy as np
import datetime
import sqlite3
import os
import pymodbus_reader # pymodbus_reader.py should be in the path: "/src" 


# Create file path
BATH_PATH = os.path.dirname(os.path.abspath(__file__))
ETC_PATH = os.path.join(BATH_PATH, "..", "etc")
DATA_PATH = os.path.join(BATH_PATH, "..", "data")
POINT_TABLE_PATH = os.path.join(ETC_PATH, "point_table")
ERROR_LOG_PATH = os.path.join(ETC_PATH, "error_log")


# Field setting, read Point_Table and Field_Name
########################################################################################################
BA_Point_filename = [f for f in os.listdir(POINT_TABLE_PATH) if ("BA_Point_List" in f) & (f.endswith(".xlsx"))]
BA_Point_Table = BA_Point_filename[0]
Field_name = BA_Point_Table.split("-")[1]
########################################################################################################

print(F"Point Table: {BA_Point_Table}") # If there is more than one file of Point table, please check the file name and contents.


# %% Error log function
def error_log(error_log_txt): 
    txt = error_log_txt
    file_name = "error_log-data_saver.txt"
    if file_name not in  os.listdir(ERROR_LOG_PATH):
        f = open(os.path.join(ERROR_LOG_PATH, file_name), "w")
        f.write(F"{txt}\n")
        f.close()
    else:
        f = open(os.path.join(ERROR_LOG_PATH, file_name), "a")
        f.write(F"{txt}\n")
        f.close()    


# %% Point Data reading
# RTU
def get_RTU_point(): 
    point_list = pd.read_excel(os.path.join(ETC_PATH, BA_Point_Table), sheet_name="rtu") # Reading rtu page of the Point Table
    point_list = point_list[point_list["Protocol"]=="modbus_rtu"] # Check types of protocols
    return point_list.iloc[:, 2:]


# TCP
def get_TCP_point(): 
    point_list = pd.read_excel(os.path.join(ETC_PATH, BA_Point_Table), sheet_name="tcp") # Reading tcp page of the Point Table
    point_list = point_list[point_list["Protocol"]=="modbus_tcp"] # Check types of protocols
    return point_list.iloc[:, 2:]


# %% Function of logging point data
# Extract TCP data, the raw data will be in the type of python dictionary
def get_TCP_data():
    TCP_data = pymodbus_reader.read_TCP_sensor()
    return TCP_data


# Extract RTU data, the raw data will be in the type of python dictionary
def get_RTU_data():
    RTU_data = pymodbus_reader.read_RTU_sensor()
    return RTU_data


# %%
# Save RTU data
def log_RTU_data():
    data_log = get_RTU_data() # Gather current data 
    # Check data logging
    if len(data_log)!=0:
        df_data = pd.DataFrame.from_dict(data_log) # Transform data as dataframe
        print(df_data)
        path = os.path.join(DATA_PATH, F"Data_logger-{Field_name}.db") # DB file path
        conn = sqlite3.connect(path) # Connect to DB file

        # Check table list of the DB file.
        cursor = conn.cursor() # Create cursor 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") 
        table_list = [i[0] for i in cursor.fetchall()]

        # Saving
        table = "RTU_history"
        reformed_data = {}
        reformed_data["Time"] = []
        reformed_data["Point_ID"] = []
        reformed_data["Value"] = []
        for col in df_data.columns:
            if col == "Time":
                reformed_data[col] = [df_data[col].values[0]] * (len(df_data.columns) - 1)
            if col != "Time":
                reformed_data["Point_ID"].append(col)
                reformed_data["Value"].append(df_data[col].values[0])        
        
        reformed_df = pd.DataFrame.from_dict(reformed_data)
        if (len(reformed_df) >= 0) & (table in table_list):
            reformed_df.to_sql(name=table, con=conn, if_exists="append")  
            conn.close()
            print(F"{table} is updated!")

        # Check reformed table existance.
        elif (len(reformed_df) >= 0) & (table not in table_list):
            conn = sqlite3.connect(path)
            reformed_df.to_sql(name=table, con=conn, if_exists="append")
            conn.close()
            error_log(F"{table} is created for reformed data!")
            print(F"{table} is created for reformed data!")    
        # Record the timestamp
        error_log(table)
        return reformed_data        
    # Record error event when logging fail
    else:
        error_log("RTU data log failed")



# Save TCP data
def log_TCP_data():
    data_log = get_TCP_data() # Gather current data 
    if len(data_log)!=0:
        df_data = pd.DataFrame.from_dict(data_log) # Transform data as dataframe
        print(df_data)
        path = os.path.join(DATA_PATH, F"Data_logger-{Field_name}.db") # DB file path
        conn = sqlite3.connect(path) # Connect to DB file

        # Check table list of the DB file.
        cursor = conn.cursor() # Create cursor 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") 
        table_list = [i[0] for i in cursor.fetchall()]

        table = "TCP_history"
        reformed_data = {}
        reformed_data["Time"] = []
        reformed_data["Point_ID"] = []
        reformed_data["Value"] = []
        for col in df_data.columns:
            if col == "Time":
                reformed_data[col] = [df_data[col].values[0]] * (len(df_data.columns) - 1)
            if col != "Time":
                reformed_data["Point_ID"].append(col)
                reformed_data["Value"].append(df_data[col].values[0])        

        reformed_df = pd.DataFrame.from_dict(reformed_data)
        if (len(reformed_df) >= 0) & (table in table_list):
            reformed_df.to_sql(name=table, con=conn, if_exists="append")  
            conn.close()
            print(F"{table} is updated!")

        # Check reformed table existance.
        elif (len(reformed_df) >= 0) & (table not in table_list):
            conn = sqlite3.connect(path)
            reformed_df.to_sql(name=table, con=conn, if_exists="append")
            conn.close()
            error_log(F"{table} is created for reformed data!")
            print(F"{table} is created for reformed data!")    
        # Record the timestamp
        error_log(table)
        return reformed_data
    # Record error event when logging fail
    else:
        error_log("TCP data log failed")


if __name__ == "__main__":
    # Save RTU data
    try:
        log_RTU_data()
        print("RTU_Sensor updated!")
    except:
        print("RTU_Sensor may not be installed properly.")
        error_log("RTU data save failed")
        pass

    # Save TCP data
    try:
        log_TCP_data()
        print("TCP_Sensor updated!")
    except:
        print("TCP_Sensor may not be installed properly.")
        error_log("TCP data save failed")
        pass
