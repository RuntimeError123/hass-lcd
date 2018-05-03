import requests
import json

protocol = 'https'
homeassistant_ip = '192.168.1.XX'
port = '8123'
api_password = 'password'
entity_id_temp_in = 'sensor.netatmo_indoor_temperature'
entity_id_hum_in = 'sensor.netatmo_indoor_humidity'
entity_id_temp_out = 'sensor.netatmo_outdoor_temperature'
entity_id_hum_out = 'sensor.netatmo_outdoor_humidity'

display_ip = '192.168.1.XX'
display_led_gpio = '0'

try:
    api_password
except:
    headers = {'content-type' : 'application/json'}
else:
    headers = {'x-ha-access' : api_password, \
   'content-type' : 'application/json'}

def get_entity_state(entity_id: str):
    url = protocol+'://'+homeassistant_ip+':'+port+'/api/states/'+entity_id
    state = str(int(float(json.loads(requests.get(url, headers=headers).text)['state'])))
    return state

state_temp_in = get_entity_state(entity_id_temp_in)
state_hum_in = get_entity_state(entity_id_hum_in)
state_temp_out = get_entity_state(entity_id_temp_out)
state_hum_out = get_entity_state(entity_id_hum_out)

ledstatus = json.loads(requests.get('http://' +display_ip+ '/control?cmd=status,GPIO,'+display_led_gpio).text)['state']

requests.get('http://' +display_ip+ '/control?cmd=lcdcmd,clear')
requests.get('http://' +display_ip+ '/control?cmd=lcd,1,Indoor%3A%20%20'+state_temp_in+'%C2%B0C%20%2F%20'+state_hum_in+'%25')
requests.get('http://' +display_ip+ '/control?cmd=lcd,2,Outdoor%3A%20'+state_temp_out+'%C2%B0C%20%2F%20'+state_hum_out+'%25')

if ledstatus == 0:
    requests.get('http://' +display_ip+ '/control?cmd=GPIO,'+display_led_gpio+',1')
