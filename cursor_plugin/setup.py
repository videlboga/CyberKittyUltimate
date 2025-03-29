#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="cursor_voice_avatar_plugin",
    version="1.0.0",
    description="Плагин для управления Voice Avatar MCP сервером через Cursor",
    author="CyberKitty",
    author_email="cyberkitty@example.com",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "asyncio",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
) 