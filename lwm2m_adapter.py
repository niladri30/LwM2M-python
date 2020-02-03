import ssl
import requests
from recursive_json import extract_values
import schedule
import time
import json
import http.client


def job():

    # api-endpoint
    URL = "http://<hostname>.us-east-2.compute.amazonaws.com:8080/api/clients/urn:sap:11223344/3316/0/5700"
    certificate_file = 'certificate.pem'
    certificate_secret = '4U3GiIiDo5EKlOGD8GuAPoQcYaJvFtJ28mJ8'
    host = '<hostname>.eu10.cp.iot.sap'

    # SAP IoT Cockpit Values
    device_alternate_id = '33'
    capability_alternate_id = '11'
    sensor_alternate_id = '44'

    # sending get request and saving the response as response object
    r = requests.get(url=URL)

    # extracting data in json format
    #data = r.json()
    #print(data)
    values = extract_values(r.json(), 'value')

    # Defining parts of the HTTP request
    request_url='/iot/gateway/rest/measures/%s' % device_alternate_id
    request_headers = {
        'Content-Type': 'application/json'
    }
    request_body_dict = {
        'capabilityAlternateId': capability_alternate_id,
        'sensorAlternateId': sensor_alternate_id,
        'measures': [{
            'Voltage': values[0]
        }]
    }

    # Declare client certificate settings for https connection
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_cert_chain(certfile=certificate_file, password=certificate_secret)
    connection = http.client.HTTPSConnection(host, port=443, context=context)

    # HTTP POST request
    connection.request(method="POST", url=request_url,headers=request_headers, body=json.dumps(request_body_dict))

    # Print the HTTP response
    response = connection.getresponse()
    print(response.status, response.reason)
    #data = response.read()
    #print(data)

    print(json.dumps(request_body_dict))


schedule.every(10).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
