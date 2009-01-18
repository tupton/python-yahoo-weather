#! /usr/bin/python

"""
Fetches weather reports from Yahoo!

Written by Thomas Upton (http://thomas.fiveuptons.com/),
with contributions from Chris Lasher (http://igotgenes.blogspot.com/).

This code is licensed under a BY-NC-SA Creative Commons license.
http://creativecommons.org/licenses/by-nc-sa/3.0/us/

See http://thomas.fiveuptons.com/?p=202 for more information.
"""

import sys
import urllib
from optparse import OptionParser
from xml.dom.minidom import parse

# Yahoo!'s limit on the number of days they will forecast for
DAYS_LIMIT = 2
WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
METRIC_PARAMETER = '&u=c'
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'

def get_weather(location_code, days, metric):
    """
    Fetches weather report from Yahoo!

    :Parameters:
    -`location_code`: A five digit US zip code.
    -`days`: number of days to obtain forecasts for

    :Returns:
    -`weather_data`: a dictionary of weather data
    """

    # Get the correct weather url.
    if metric:
        url = WEATHER_URL % location_code + METRIC_PARAMETER
    else:
        url = WEATHER_URL % location_code

    # Parse the XML feed.
    dom = parse(urllib.urlopen(url))

    # Get the units of the current feed.
    yunits = dom.getElementsByTagNameNS(WEATHER_NS, 'units')[0]

    # Get the location of the specified location code.
    ylocation = dom.getElementsByTagNameNS(WEATHER_NS, 'location')[0]

    # Get the currrent conditions.
    ycondition = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]

    # Hold the forecast in a hash.
    forecasts = []

    # Walk the DOM in order to find the forecast nodes.
    for i, node in enumerate(dom.getElementsByTagNameNS(WEATHER_NS,'forecast')):
        
        # Stop if the number of obtained forecasts equals the number of requested days
        if i + 1 > days:
            break
        else:
            # Insert the forecast into the forcast dictionary.
            forecasts.append (
                {
                    'date': node.getAttribute('date'),
                    'low': node.getAttribute('low'),
                    'high': node.getAttribute('high'),
                    'condition': node.getAttribute('text')
                }
            )

    # Return a dictionary of the weather that we just parsed.
    weather_data = {
        'current_condition': ycondition.getAttribute('text'),
        'current_temp': ycondition.getAttribute('temp'),
        'forecasts': forecasts,
        'units': yunits.getAttribute('temperature'),
        'city': ylocation.getAttribute('city'),
        'region': ylocation.getAttribute('region'),
    }
    
    return weather_data

def create_report(weather_data, options):
    """
    Constructs a weather report as a string.

    :Parameters:
    -`weather_data`: a dictionary of weather data
    -`options`: options to determine output selections

    :Returns:
    -`report_str`: a formatted string reporting weather

    """

    report = []
    
    if options.location:
        if options.verbose:
            # Add the location header.
            report.append("Location:")

        # Add the location.
        location_str = "%(city)s %(region)s\n" % weather_data
        report.append(location_str)

    if (not options.nocurr):
        if options.verbose:
            # Add current conditions header.
            report.append("Current conditions:")

        # Add the current weather.
        curr_str = "%(current_temp)s%(units)s and %(current_condition)s\n" % weather_data
        report.append(curr_str)

    if (options.forecast > 0):
        if options.verbose:
            # Add the forecast header.
            report.append("Forecast:")

        # Add the forecasts.
        for forecast in weather_data['forecasts']:
            
            forecast['units'] = weather_data['units']
        
            forecast_str = """\
  %(date)s
    High: %(high)s%(units)s
    Low: %(low)s%(units)s
    Condition: %(condition)s""" % forecast

            report.append(forecast_str)

    report_str = "\n".join(report)
    
    return report_str

def create_cli_parser():
    """
    Creates a command line interface parser.
    """

    usage = (
            "%prog [options] location_code",
            __doc__,
            """Arguments:
    LOCATION_CODE: The LOCATION_CODE for the region of interest.
                   See http://developer.yahoo.com/weather/#req"""
    )
    
    usage = "\n\n".join(usage)
    
    cli_parser = OptionParser(usage)
    
    # Add the CLI options
    cli_parser.add_option('-c', '--nocurr', action='store_true',
        help="suppress reporting the current weather conditions"
    )
    
    cli_parser.add_option('-m', '--metric', action='store_true',
        help="show the temperature in metric units (C)"
    )

    cli_parser.add_option('-f', '--forecast', action='store', type='int',
        help="show the forecast for DAYS days", metavar="DAYS")
    
    cli_parser.add_option('-l', '--location', action='store_true',
        help="give the location of the weather"
    )
    
    cli_parser.add_option('-v', '--verbose', action='store_true',
        help="print the weather section headers"
    )
    
    # Set the default number of days to forecast to 0
    cli_parser.set_defaults(forecast=0, metric=False)

    return cli_parser

def main(argv):

    # Create the command line parser.
    cli_parser = create_cli_parser()
    
    # Get the options and arguments.
    opts, args = cli_parser.parse_args(argv)

    # Check that an argument was passed.
    if len(args) < 1:
        cli_parser.error("Not enough arguments supplied.")

    # Check the location code
    location_code = args[0]
    
    # Check for a US location.
#    if len(location_code) != 5 or not location_code.isdigit():
#        cli_parser.error("ZIP code must be 5 digits")
    
    if opts.forecast > DAYS_LIMIT or opts.forecast < 0:
        cli_parser.error("Days to forecast must be between 0 and %d" % DAYS_LIMIT)

    # Get the weather.
    weather = get_weather(location_code, opts.forecast, opts.metric)

    # Create the report.
    report = create_report(weather, opts)

    print report

if __name__ == "__main__":
    main(sys.argv[1:])
