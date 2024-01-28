Update: Oh snap this still works

# peloton_client
## Wrapper for OnePeloton Web API

Based on endpoints documented at:  
https://app.swaggerhub.com/apis/DovOps/peloton-unofficial-api/0.2.3

In the broad strokes, this API client for python can access user:  
 - workout data
 - public account data
 - public account summary
 - achievements
 - followers & following
 - calendar data
 - ride data
 - workout metrics
 
**How to use:**   
git clone this repository into your project folder. 

```
git clone https://github.com/kiera-bot/peloton_client.git
```
  
import peloton client into your .py
```   
from peloton_client import peloton_client
```

make sure you pip install requests 
   
authenticate. here is a very simple example:
```
client = peloton_client.PelotonClient(username="youremail@email.com", password="yourpassword")
workouts = client.fetch_workouts()
```

in sum, a simple main.py should look like this: 
```
from peloton_client import peloton_client

client = peloton_client.PelotonClient(username="youremail@email.com", password="yourpassword")
workouts = client.fetch_workouts()
print(workouts)

```

This will return a JSON object with your workout metrics.

