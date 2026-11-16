#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Generated entry template for Flask app."""

from app import create_app

app = create_app("develop")


if __name__ == "__main__":
    app.run()
