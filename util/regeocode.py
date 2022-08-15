import json
import requests

def regeocode(lng,lat,key):
    gps = str(lng)+','+str(lat)
    url = 'https://restapi.amap.com/v3/geocode/regeo?key=%s&location=%s&poitype=&radius=3000&extensions=all&batch=false&roadlevel=0'%(key,gps)

    res = requests.get(url)
    json_data = json.loads(res.text)

    addressComponent = json_data['regeocode']['addressComponent']
    province=addressComponent['province']
    city=addressComponent['city']
    district=addressComponent['district']
    streetNumber = addressComponent['streetNumber']
    streetNumber_street=streetNumber['street']
    streetNumber_number=streetNumber['number']
    streetNumber_distance = 0.0
    streetNumber_direction = None

    if streetNumber_number:
        streetNumber_direction=streetNumber['direction']
        streetNumber_distance=float(streetNumber['distance'])

    roads = json_data['regeocode']['roads'][0]
    roads_name = roads['name']
    roads_distance = float(roads['distance'])

    roadinters = json_data['regeocode']['roadinters'][0]
    first_name = roadinters['first_name']
    second_name = roadinters['second_name']
    roadinters_direction = roadinters['direction']
    roadinters_distance = float(roadinters['distance'])

    if streetNumber_number:
        street_dict = {'streetNumber_street':streetNumber_distance,'roads_name':roads_distance,'first_name':roadinters_distance}
        street_dict_={'streetNumber_street':streetNumber_street,'roads_name':roads_name,'first_name':first_name}
    else:
        street_dict = {'roads_name':roads_distance,'first_name':roadinters_distance}
        street_dict_ = {'roads_name':roads_name,'first_name':first_name}
    street = street_dict_[min(street_dict,key=street_dict.get)]
    # if streetNumber_number and streetNumber_distance < roadinters_distance and streetNumber_street == street:
    #     address = city + district + streetNumber_street + streetNumber_number + streetNumber_direction + str(int(streetNumber_distance)) + '米'
    # else:
    # address = city + district + first_name + '与' + second_name + '交叉口' + roadinters_direction + str(int(roadinters_distance)) + '米'

    address =f'{district}{roads_name}({first_name}与{second_name}交叉口{roadinters_direction}{int(roadinters_distance)}米)'

    return city,district,street,address