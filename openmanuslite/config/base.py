class BaseConfig:
    def __init__(self, config_data=None):
        """
        初始化 Config 对象
        :param config_data: 传入的字典配置数据
        """
        self._config_data = config_data or {}
        for key, value in self._config_data.items():
            setattr(self, key, self._process_value(value))

    def load_config(self, config_data):
        """
        // 加载配置数据, 传入字典
        """
        self._config_data = config_data

    def _process_value(self, value):
        """
        处理配置值，若为字典则转为 Config 实例
        """
        return BaseConfig(value) if isinstance(value, dict) else value

    def get(self, key, default=None):
        """
        通过键获取配置值
        """
        return self._config_data.get(key, default)

    def set(self, key, value):
        """
        通过键设置配置值
        """
        self._config_data[key] = self._process_value(value)
        setattr(self, key, self._process_value(value))

    def to_dict(self):
        """
        将 Config 对象转换为字典，包括嵌套的 Config 对象
        """
        result = {}
        for key, value in self._config_data.items():
            result[key] = value.to_dict() if isinstance(value, BaseConfig) else value
        return result

    def display_config(self):
        """
        显示所有配置选项
        """
        for key, value in self._config_data.items():
            print(f"{key}: {value}")

    def __getattr__(self, name):
        if name in self._config_data:
            return self._process_value(self._config_data[name])
        raise AttributeError(f"Config object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        自定义 setattr 方法，以保证字典键值同步
        """
        if name != "_config_data":
            self._config_data[name] = self._process_value(value)
        super().__setattr__(name, value)

    def __str__(self):
        return f"Config({self._config_data})"

    def __repr__(self):
        return self.__str__()
