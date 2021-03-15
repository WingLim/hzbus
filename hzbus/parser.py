import json
from hzbus.api import Api
from hzbus.model import Route, Stop, Bus


def find_parse_route(routeName):
    raw = Api().find_route_by_name(routeName)
    routes = json.loads(raw)['items'][0]['routes']
    result = []
    for route in routes:
        a_route = Route()
        a_route.name = route['routeName']
        a_route.id = route['routeId']
        a_route.opposite_id = route['oppositeId']
        a_route.origin = route['origin']
        a_route.terminal = route['terminal']
        a_route.no = route['routeNo']
        result.append(a_route)

    return result


def parse_stops(stops):
    result = []
    for stop in stops:
        buses = stop['buses']
        stop = stop['routeStop']
        a_stop = Stop()
        a_stop.id = stop['stopId']
        a_stop.name = stop['stopName']
        a_stop.lng = stop['lng']
        a_stop.lat = stop['lat']
        a_stop.buses = parse_buses(buses)
        result.append(a_stop)

    return result


def parse_buses(buses):
    result = []
    for bus in buses:
        a_bus = Bus()
        a_bus.id = bus['busId']
        a_bus.plate = bus['busPlate']
        a_bus.lng = bus['lng']
        a_bus.lat = bus['lat']
        a_bus.distance = bus['nextDistance']
        a_bus.is_arrive = bus['isArrive']
        result.append(a_bus)

    return result


def get_route_detail(route):
    api = Api()
    raw = api.get_bus_position_by_routeId(route.id)
    stops = json.loads(raw)['items'][0]['routes'][0]['stops']
    route.stops = parse_stops(stops)

    return route


def get_traffic_info(route):
    raw = Api().get_route_traffic_info(route.no)
    info = json.loads(raw)['item']['traffic']
    if info[0]['startStopName'] != route.origin:
        raw = Api().get_route_traffic_info(route.no, 5)
        info = json.loads(raw)['item']['traffic']
    result = ['']
    for one in info:
        result.append(one['trafficSpeed'])

    return result


def get_next_bus(routeId, stopId):
    raw = Api().get_next_bus_by_route_stopId(routeId, stopId)
    buses = json.loads(raw)['item']['nextBuses']['buses']
    stopName = json.loads(raw)['item']['nextBuses']['stopName']
    result = []
    for bus in buses:
        a_bus = Bus()
        a_bus.id = bus['busId']
        a_bus.plate = bus['busPlate']
        a_bus.lng = bus['lng']
        a_bus.lat = bus['lat']
        a_bus.distance = bus['targetDistance']
        a_bus.seconds = bus['']
        a_bus.is_arrive = bus['isArrive']
        result.append(a_bus)

    return stopName, result