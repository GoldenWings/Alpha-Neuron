from utility.config import Config

__name__ = 'utility.status'
status_config = Config(name='status', class_name='Status', inputs=None, outputs=None, is_active=True, is_threaded=False)

utility_modules = {status_config.name: status_config}
utility_config = Config(name='utility', modules=utility_modules)
