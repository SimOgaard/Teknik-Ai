from matplotlib import style
style.use("ggplot")
import matplotlib.pyplot as plt
import pandas as pd
import requests
import pandas as pd
from datetime import datetime
urls = ["https://car9o7qv7j.execute-api.us-east-1.amazonaws.com/iot/device?MAC=84:F3:EB:B4:6F:61","https://nkclsbr32f.execute-api.us-east-1.amazonaws.com/beta/device?MAC=DC:4F:22:5F:43:75"]
Simon = pd.DataFrame()
BBB = pd.DataFrame()

# from datetime import datetime
# timestamp = 1545730073
# dt_object = datetime.fromtimestamp(timestamp)
# print("dt_object =", dt_object)
# print("type(dt_object) =", type(dt_object))


info = requests.get(urls[0]).json()
for k in info['data']:            
    if k['CO2'] < 5000:
        k["time"]=datetime.fromtimestamp(k["time"]).strftime("%D:%H:%M:%S")
        # datetime.fromtimestamp(k["time"])
        Simon = Simon.append(k, ignore_index=True)

info = requests.get(urls[1]).json()
for k in info['data']:
    if k['CO2'] < 5000:
        k["time"]=datetime.fromtimestamp(k["time"]).strftime("%D:%H:%M:%S")
        BBB = BBB.append(k, ignore_index=True)


Simon[["CO2","LDR"]].plot()
plt.xticks(Simon.index,Simon["time"].values)
plt.tick_params(axis="x", rotation=90)
plt.show()

Simon[["Hum","Temp"]].plot()
plt.xticks(Simon.index,Simon["time"].values)
plt.tick_params(axis="x", rotation=90)
plt.show()


BBB[["CO2","LDR"]].plot()
plt.xticks(BBB.index,BBB["time"].values)
plt.tick_params(axis="x", rotation=90)
plt.show()

BBB[["Hum","Temp"]].plot()
plt.xticks(BBB.index,BBB["time"].values)
plt.tick_params(axis="x", rotation=90)
plt.show()

print(Simon.values.tolist())
print(BBB.values.tolist())