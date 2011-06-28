#!/usr/bin/env python

from distutils.core import setup

long_description = 'Slaps your desired apps on your screen in your desired style'

setup(name = 'appslap',
        version = '0.1',
        description = 'Slap apps on your screen',
        maintainer = 'Mathias Nyman',
        maintainer_email = 'mcnyman@cc.hut.fi',
        url = 'http://www.github.com/appSlap', #TODO: define url
        long_description = long_description,
        packages = ['appslap']
        )

