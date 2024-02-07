import pandas

timing_df = pandas.read_csv('./req_data.csv')
session_add_id = pandas.read_csv('./session_add_id.csv')
session_add_url_id = pandas.read_csv('./session_add_url_id.csv')
session_make_new = pandas.read_csv('./session_make_new.csv')
print(timing_df.head())
print(session_add_id.head())

timing_df['session_add_id'] = session_add_id['session_add_id']
timing_df['session_add_url_id'] = session_add_url_id['session_add_url_id']
timing_df['session_make_new'] = session_make_new['session_make_new']

print(timing_df.head())
timing_df.to_csv('./timing_final.csv')