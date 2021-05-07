import rlmtp


database_dir = './RESSLab_Material_DB'
csv_output = './Summarized_Material_DB.csv'
rlmtp.write_description_database_csv(database_dir, csv_output)
