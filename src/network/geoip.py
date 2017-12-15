# -*- coding:utf-8 -*-
import pygeoip

gi = pygeoip.GeoIP('')


def print_record(tgt):
    rec = gi.record_by_name(tgt)
    city = rec['city']
    region = rec['region_name']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']
    print('[*] Target: ' + tgt + ' Geo-located. ')
    print('[+] ' + str(city) + ', ' + str(region) + ', ' + str(country))
    print('[+] Latitude: ' + str(lat) + ', Longitude: ' + str(long))


tgt = '173.255.226.98'
print_record(tgt)
