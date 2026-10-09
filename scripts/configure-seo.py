#!/usr/bin/env python3
"""Rebuild all pages so editorial content and SEO metadata stay in sync."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name('build-site.py')), run_name='__main__')
