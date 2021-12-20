import pickle
import pandas as pd
import sys
import json
import numpy as np

name = 'train.dat'

model = pickle.load(open(name, "rb"))

data = json.loads(sys.argv[-1])

dataset = pd.DataFrame(data=data, dtype=float)

preds = model.predict(dataset[0:])

preds = np.array(preds).tolist()

print(json.dumps(preds))

