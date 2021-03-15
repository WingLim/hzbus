import base64
import hmac
import uuid
import random
import time
import string
import requests
from urllib.parse import quote
from hashlib import sha256

Version1 = 1
Version2 = 2

class Api:

    def __init__(self):
        self.url = ''
        self.uri = ''
        self.base_data = {

            'city': 330100,

        }

    def _gen_raw_str(self, base_data: dict) -> str:
        """
        Splice string for generate signature
        :param base_data: Request params
        :return: String
        """
        str_arr = list(base_data.keys())
        str_arr.sort()
        result = 'GET&%2F&'
        for key in str_arr:
            result += str(key)
            result += '%3D'
            result += str(base_data[key])
            result += '%26'
        return result[0:-3]

    def _gen_signature(self, raw_str) -> str:
        """
        Generate a unique for every request
        :param raw_str: Request params in string
        :return: Signture for a request
        """
        key = '23c2f22fadf46f3b28b6adddd242959e&'.encode('utf-8')
        message = raw_str.encode('utf-8')
        sign = base64.b64encode(
            hmac.new(key, message, digestmod=sha256).digest())
        sign = str(sign, 'utf-8')
        return quote(sign).replace('/', '%2F')

    def _gen_href(self, base_data: dict, signature: str = None):
        """
        Splice href to request
        :param base_data: Request params
        :param signature:
        :return: Request href
        """
        if signature:
            base_data['signature'] = signature
        href = self.url + self.uri + '?'
        for key, val in base_data.items():
            href += str(key)
            href += '='
            href += str(val)
            href += '&'
        return href[0:-1]

    def _send_request(self, version):
        if version == Version1:
            self.url = 'https://app.ibuscloud.com/v1/bus/'
            self.base_data['h5Platform'] = 6
            href = self._gen_href(self.base_data)
        elif version == Version2:
            self.url = 'https://app.ibuscloud.com/v2/bus/'
            str_list = [random.choice(string.digits + string.ascii_lowercase) for i in range(64)]
            data = {
                'uuid': str(uuid.uuid1()),
                'access_id': 'ptapp',
                'timestamp': '',
                'token': '',
                'appSource': 'com.dtdream.publictransit',
                'platform': 'iOS',
                'deviceId': ''.join(str_list),
            }
            self.base_data.update(data)
            self.base_data['timestamp'] = int(time.time() * 1000)
            raw_str = self._gen_raw_str(self.base_data)
            signature = self._gen_signature(raw_str)
            href = self._gen_href(self.base_data, signature)
        else:
            raise Exception("Invalid version")
        print(href)
        r = requests.get(href)
        return r.text

    def get_route_traffic_info(self, routeNo, direction=4):
        self.uri = 'getRouteTrafficInfo'
        self.base_data['routeNo'] = routeNo
        self.base_data['direction'] = direction
        return self._send_request(Version2)

    def find_route_by_name(self, routeName):
        self.uri = 'findRouteByName'
        self.base_data['routeName'] = routeName
        return self._send_request(Version1)

    def get_bus_position_by_routeId(self, routeId):
        self.uri = 'getBusPositionByRouteId'
        self.base_data['routeId'] = routeId
        return self._send_request(Version1)

    def get_next_bus_by_route_stopId(self, routeId, stopId):
        self.uri = 'getNextBusByRouteStopId'
        self.base_data['routeId'] = routeId
        self.base_data['stopId'] = stopId
        return self._send_request(Version1)


if __name__ == '__main__':
    api = Api()
    # print(api.get_bus_position_by_routeId(1001000003))

    print(api.get_route_traffic_info(1001000002, 5))
