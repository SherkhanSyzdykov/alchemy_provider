from os import environ


__all__ = ('settings')


settings = None
if settings is None:
    development = environ.get('DEVELOPMENT', False)

    if development:
        print('Development mode. Please disable it in production')
        from . import development
        settings = development
    else:
        from . import production
        settings = production
