# ShivBox

ShivBox is an easy to use discord rich presence client

## Quick Example


```py
from ShivBox import ShivBox as sb #Entire ShivBox Library#
from sb import rpclient as rpc #Imports the RP client#
    
client = rpc.Client("clientID") #Your application's ID as a string#
client.start() #Start the port connection#

current_time = time.time() #The start time for elapsing#

#Activity Info#
activity = {
    "state": "This is the state",
    "details": "Here are some details",
    "timestamps": {
        "start": int(current_time)
    },
    "assets": {
        "small_text": "Text for small_image",
        "small_image": "img_small",
        "large_text": "Text for large_image",
        "large_image": "img_large"
    },
    "party": {
    "size": [1, 6]
    }
}

While True:
    client.send_rich_presence(activity)

 ```

### Requirements
- Python 3.7.x
- Asyncio
