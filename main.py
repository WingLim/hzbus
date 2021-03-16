import os
import json
from prettytable import PrettyTable
from hzbus.parser import find_parse_route, get_route_detail, get_traffic_info, get_next_bus
from hzbus.utils import parse_seconds


def main():

    if os.path.exists('config.json'):
        load = input('是否要加载配置文件(y/n): ')
    if load == 'y':
        with open('config.json', 'r') as f:
            config = json.load(f)
        stopName, buses = get_next_bus(config['routeId'], config['stopId'])
        next_bus_table = PrettyTable(['公交车牌', '距离', '到达时间'])
        for one in buses:
            next_bus_table.add_row([one.plate, one.distance, parse_seconds(one.seconds)])
        print(stopName)
        if len(buses) == 0:
            print('非车辆运行时间')
        else:
            print(next_bus_table)
    else:
        routeName = input('输入你要查找的路线: ')
        result = find_parse_route(routeName)
        select_route_table = PrettyTable(['序号', '线路名', '起始站', '终点站'])
        for i, one in enumerate(result):
            select_route_table.add_row([i, one.name, one.origin, one.terminal])
        print(select_route_table)

        no = int(input('输入要查看的线路序号: '))
        if no > len(result):
            raise Exception('Out of range')
        route = get_route_detail(result[no])
        traffic_info = get_traffic_info(route)
        route_table = PrettyTable(['序号', '站点名', '公交车牌', '距离', '到达时间'])
        for i, one in enumerate(route.stops):
            if len(one.buses):
                time = parse_seconds(one.buses[0].seconds)
                route_table.add_row([i, one.name, one.buses[0].plate, one.buses[0].distance, time])
            else:
                route_table.add_row([i, one.name, '', '', ''])
        route_table.add_column("交通情况", traffic_info)
        print(route_table)

        save = input('是否要保存(y/n): ')
        if save == 'y':
            no = int(input('输入要查看的站点序号: '))
        else:
            exit(0)

        with open('config.json', 'w+') as f:
            config = {
                'routeId': route.id,
                'stopId': route.stops[no].id
            }
            json.dump(config, f)



if __name__ == '__main__':
    main()
