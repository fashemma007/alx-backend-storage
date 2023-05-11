#!/usr/bin/env python3
"""module docs for mains/5-main.py"""
from exercise import Cache, replay


cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)
