## GPS data cleaner and Python data collector for Mikrotik
This is part of a larger project however the two pieces that other may find usefulis the Mikrotik script and the Python data collector. 

For my testing I am using Virtual Box running CHR and production is a LtAP mini.
You don't need the GPS module running to simulated the data the data will be empty.

---
In my settings I am using AWS as the broker, so the following is necessary for getting this going with AWS
## Configuring AWS IoT
- Create a new Thing under "Things". I called my "Thing" gps.
- Create a certificate for your new AWS IoT Thing.
- Create a policy for the certificate I called mine gps-Policy.
- The policy should have a publish, receive, subscribe. For testing my topic was sensor/gps
- Setup at least two "Connects" that have allow, one for publish and one for subscribe. This will be the MQTT client id.
---
## Configure MQTT on the Mikrotik
- Install the IoT extra package.
- Under System Certificates add in the AWS certificates for the new policy.
- Under IoT MQTT create a new broker
    - Name "AWS"
    - Address is your IoT end point
    - port 883
    - ssl checked
    - ClientID is the client ID created in the Publish "Connect."
    - Certificate select the imported certificate
- Set a schedule to run the script as often as necessary.
