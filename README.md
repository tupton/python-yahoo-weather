# Python Yahoo Weather

Fetches weather reports from [Yahoo! Weather][yw].

[yw]: http://weather.yahoo.com/

Written by [Thomas Upton][tu] with contributions from [Chris Lasher][cl].

[tu]: http://www.thomasupton.com/
[cl]: http://igotgenes.blogspot.com/

This code is licensed under a [BY-NC-SA Creative Commons license][cc].

[cc]: http://creativecommons.org/licenses/by-nc-sa/3.0/us/

See [the blog post][blog] for more information.

[blog]: http://www.thomasupton.com/blog/?p=202

Usage: `weather.py [options] location_code` 

    $ weather.py --help
for options and their descriptions.

Weather data can be printed to an output file with the `--output` option.

    $ weather.py 24060 --output='weather.txt'

If a weather report cannot be generated, the specified output file is not
altered. This is useful when attempting to cache weather output while, for
instance, on a flaky network connection. To attempt to update the weather file
and output its contents, one could use the following command. If the weather
could not be loaded, the previous contents of the file are shown.

    $ weather.py 24060 --output='weather.txt' && cat weather.txt

## Example Usage

### Default output
    $ weather.py 24060
    25F and Partly Cloudy

### Metric units
    $ weather.py -m 24060
    -4C and Partly Cloudy

### Different delimiter
    $ weather.py -d " / " 24060
    50F / Mostly Cloudy

### With two days' forecast
    $ weather.py -lf2 24060
    Blacksburg VA

    25F and Partly Cloudy

      17 Jan 2009
        High: 30F
        Low: 22F
        Condition: Partly Cloudy
      18 Jan 2009
        High: 39F
        Low: 25F
        Condition: PM Snow Showers

### With headers
    $ weather.py -lvf2 24060
    Location:
    Blacksburg VA

    Current conditions:
    25F and Partly Cloudy

    Forecast:
      17 Jan 2009
        High: 30F
        Low: 22F
        Condition: Partly Cloudy
      18 Jan 2009
        High: 39F
        Low: 25F
        Condition: PM Snow Showers

