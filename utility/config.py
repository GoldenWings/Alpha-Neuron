class Config:
    def __init__(self, modules=None, name=None, inputs=None, outputs=None,is_active=True, is_threaded=None, parameters=[]):
        """
        Why default value of None?
        -> 2 Types of config : 1- PackageConfig e.x: controller, ModuleConfig ex: Motor
        -> Package config is container for modules configurations.
        :param modules: modules configuration of a package
        :param name = module name
        :param inputs: module input
        :param outputs: module output
        :param is_active: module active or obsolete
        :param is_threaded: is the module threaded
        :param parameters: set of parameters for constructor
        """
        self.modules = modules
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.is_active = is_active
        self.threaded = is_threaded
        self.parameters = parameters

    @property
    def parameterized(self):
        return True if self.parameters.count() > 0 else False

