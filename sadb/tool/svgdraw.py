import pygal
import pandas as pd
data=pd.read_csv("/home/zhangna/SAdatabase/result/SAG_Statistics_PAIRsex.csv")
xlab=data["sagd_id"].values

bar_chart = pygal.StackedBar(width=len(data["sagd_id"].values)*30,height=450,x_label_rotation=90,label_font_size = 14)
bar_chart.add('Female', data["SAG_Statistics_F"].values)
bar_chart.add('Male', data["SAG_Statistics_M"].values)
bar_chart.x_labels=data["sagd_id"].values
bar_chart.render_data_uri()
bar_chart.render_tree()
bar_chart.render_to_file("/opt/shimw/github/sex-associated/sadb/static/image/satic.svg")
