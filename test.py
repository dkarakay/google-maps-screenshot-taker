"""Tests to make some huge Gmaps. See README.md for more info."""

from main import create_map


def take_screenshot(lat, long, row, col, count):
    create_map(
        lat_start=lat,
        long_start=long,
        zoom=21,
        number_rows=row,
        number_cols=col,
        scale=0.5,
        sleep_time=2,
        offset_left=0,  # My value: 0.05
        offset_top=0.17,  # My value: 0.17
        offset_right=0,  # My value: 0.03
        offset_bottom=0.10,  # My value: 0.09
        outfile='image',
        count=count,
    )


#take_screenshot(lat=40.0145067, long=-82.9892051, row=5, col=5, count=0)
#take_screenshot(lat=40.0412929, long=-82.9919352, row=5, col=5, count=25)
#take_screenshot(lat=39.9996844, long=-83.0172387, row=5, col=5, count=50)
#take_screenshot(lat=39.9869356, long=-83.0102847, row=5, col=5, count=75)
#take_screenshot(lat=39.9903258, long=-83.0162431, row=10, col=10, count=100)
#take_screenshot(lat=40.0054915, long=-83.0024523, row=5, col=5, count=200)3
#take_screenshot(lat=40.0127152, long=-82.9936538, row=5, col=5, count=225)
take_screenshot(lat=39.9839328, long=-83.0201511, row=5, col=5, count=250)
take_screenshot(lat=39.9830482, long=-83.0163365, row=5, col=5, count=275)
take_screenshot(lat=39.9804690, long=-83.0190504, row=5, col=5, count=300)
take_screenshot(lat=39.9845519, long=-83.0342776, row=5, col=5, count=325)
take_screenshot(lat=40.0100192, long=-83.0134145, row=5, col=5, count=350)
