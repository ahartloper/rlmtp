import rlmtp
from datetime import datetime


def gen_db_summary():
    date = datetime.today().strftime('%Y-%m-%d')
    database_dir = './RESSLab_Material_DB'
    csv_output = 'Database_Summaries/Summarized_Material_DB_' + date + '.csv'
    rlmtp.write_description_database_csv(database_dir, csv_output)


if __name__ == "__main__":
    gen_db_summary()
