from utility.config import Config

status_config = Config(name='Status', inputs=None, outputs=None, is_active=True, is_threaded=False)

utility_modules = {status_config.name: status_config}
utility_config = Config(name='Utility', modules=utility_modules)