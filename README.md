# Hullpy
Python library for [Hull](https://www.hull.io)

## Install
Run `pip install git+https://github.com/ryubro/Hullpy.git` to install

## Basic usage
```
from hullpy import Hull

hull = Hull("<platform_id>",
            "<organisation_url>",
            "<app_secret>")
users = hull.get("/users")
```
