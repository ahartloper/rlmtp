import rlmtp


def gen_db_summary():
    database_dir = './RESSLab_Material_DB'
    csv_output = 'Database_Summaries/Summarized_Material_DB.csv'
    rlmtp.write_description_database_csv(database_dir, csv_output)


if __name__ == "__main__":
    gen_db_summary()
