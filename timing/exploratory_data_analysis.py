import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

timing = pd.read_csv('./timing_final.csv')
timing = timing.drop(columns='index')
print()
print(timing.describe())
print()
make_req_t_test = ttest_ind(timing['Req_get_make_new_every_time'],timing['session_make_new'])
print('Making req everytime (mean_req - mean_session):\nstatistic:', make_req_t_test[0],'\np val:',make_req_t_test[1],end='\n\n')
add_url_id_t_test = ttest_ind(timing['Req_get_add_url_id'],timing['session_add_url_id'])
print('Adding url and id everytime (mean_req - mean_session):\nstatistic:', add_url_id_t_test[0],'\np val:', add_url_id_t_test[1],end='\n\n')
add_id_t_test = ttest_ind(timing['Req_get_add_id'],timing['session_add_id'])
print('Adding id everytime (mean_req - mean_session):\nstatistic:', add_id_t_test[0],'\np val:', add_id_t_test[1],end='\n\n')
sns.displot(data=timing, kind='kde',palette=['#ff9eba','#d1003b','#ff2e69','#0062ff','#0041a8','#002259'])
plt.xlabel('Latency of getting res json (s)')
plt.ylabel('Count')
plt.show()