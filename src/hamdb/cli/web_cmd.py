#!/usr/bin/env python3

from ..web.start import create_app


def web_main():
    app = create_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()


if __name__ == "__main__":
    web_main()
