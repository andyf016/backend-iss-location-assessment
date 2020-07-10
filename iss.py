#!/usr/bin/env python

__author__ = '???'

import turtle
import requests
import time
import argparse
import sys

# api urls
coords_url = 'http://api.open-notify.org/iss-now.json'
names_url = 'http://api.open-notify.org/astros.json'
next_pass_url = 'http://api.open-notify.org/iss-pass.json'
# required parameters for next_pass_url
indy_params = {'lat': 39.7684, 'lon': -86.1581, 'n': 1}
# image for turtle
iss_image = 'iss.gif'


def get_names():
    """
    Obtains a list of the astronauts who are currently in space.
    Prints their full names, the spacecraft they are currently on
    board, and the total number of astronauts in space.
    """
    # send request to names_url and assign response
    response = requests.get(names_url)
    # retrieve json from response convert to dictionary
    parsd = (response.json())
    # extract list of people from json dict
    people = parsd.get("people")
    # print number os astronauts in space
    print(f'Astronauts in space: {len(people)} \n')
    # retrieve names and craft from person list
    for person in people:
        print(f'Astronaut: {person.get("name")}')
        print(f'Stationed on: {person.get("craft")}')
        print('*' * 15)
    return


def get_coords():
    """
    obtain the current geographic coordinates (lat/lon)
    of the space station, along with a timestamp
    """
    response = requests.get(coords_url)
    parsd = (response.json())
    coords = parsd.get('iss_position')
    coords.setdefault('timestamp', parsd.get('timestamp'))
    return coords


def get_indy():
    """
    Find out the next time that the ISS will be overhead of
    Indianapolis, Indiana. Use the geographic lat/lon of Indianapolis,
    Indiana to plot a yellow dot on the map.
    """
    # send request with required parameters
    response = requests.get(next_pass_url, params=indy_params)
    parsd = response.json()
    rise_info = parsd.get('response')
    # extract rise time from response
    rise_time = rise_info[0].get('risetime')
    # convert to human time
    final = time.ctime(rise_time)
    return final


def iss_map(coords, indy_time):
    # set up screen
    turtle.title("ISS Current Location")
    screen = turtle.Screen()
    screen.bgpic('map.gif')
    screen.setup(720, 360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    # add iss image to be used by turtle
    screen.addshape(iss_image)
    # initialize indy turtle and iss turtle
    indy = turtle.Turtle()
    space_station = turtle.Turtle(shape=iss_image)
    indy.speed(0)
    indy.hideturtle()
    # indy fill and border color
    indy.color('yellow', 'yellow')
    indy.penup()
    # go to location and draw dot
    indy.goto(-86.1581, 39.791)
    indy.pendown()
    indy.begin_fill()
    indy.circle(1)
    indy.end_fill()
    indy.write(f'Next pass: {indy_time}')
    # move iss turtle to long and lat on map
    space_station.hideturtle()
    space_station.penup()
    space_station.goto(float(coords.get('longitude')),
                       float(coords.get('latitude')))
    space_station.showturtle()
    turtle.done()
    return


def create_parser():
    """Create a command line parser object with 2 argument definitions."""
    parser = argparse.ArgumentParser(
        description="Display ISS location and next flyover of indianapolis")
    parser.add_argument('--astro',
                        help='print current astonauts and their craft',
                        action='store_true')
    parser.add_argument('--map',
                        help='''display world map with
                        ISS location and next flyover of Indy''',
                        action='store_true')
    return parser


def main(args):
    parser = create_parser()
    ns = parser.parse_args(args)
    if not ns:
        parser.print_usage()
        sys.exit(1)
    if ns.astro:
        get_names()
    if ns.map:
        iss_map(get_coords(), get_indy())


if __name__ == '__main__':
    main(sys.argv[1:])
