# -*- coding: utf-8 -*-
#!/usr/bin/env python

from os import environ
from src import create_app
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def main():
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
    
if __name__ == '__main__':
    main()
