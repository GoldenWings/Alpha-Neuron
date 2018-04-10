from utility.config import Config
status_config = Config(name='status', class_name='Status', inputs=None, outputs=None, is_active=True, is_threaded=False)
barrelwriter_cfg = Config(name='barrelwriter', class_name='BarrelWriter', inputs=['throttle', 'angle',
                                                                                  'image_frame'],
                          outputs=None, is_active=True, is_threaded=False, parameters=['servo', 'motor'])
barrelreader_cfg = Config(name='barrelreader', class_name='BarrelReader', inputs=None,
                          outputs=None, is_active=True, is_threaded=False)


utility_modules = {status_config.name: status_config, barrelwriter_cfg.name: barrelwriter_cfg,
                   barrelreader_cfg.name: barrelreader_cfg}
utility_config = Config(name='utility', modules=utility_modules)
