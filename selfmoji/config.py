
import os, json, logging

logger = logging.getLogger('CONFIG')

logger.setLevel(logging.INFO)

class Config:

    def __init__(self, filename: str):

        self._filename = filename

        self.data = Config.default()

    @staticmethod
    def default():
        return {
            "size": 64,
            "edit": True,
            "autoflush": False,
            "token": None,
            "prefix": "``"
        }
        
    def load(self):
        if os.path.isfile(self._filename):
            with open(self._filename, 'r') as file:
                self.data = json.load(file)
                logger.info(f"Config file [{self._filename}] loaded")
                for k, v in Config.default().items():
                    if k not in self.data:
                        logger.warning(f'Missing key [{k}] - using default')
                        self.data[k] = v

    def save(self):
        with open(self._filename, "w") as file:
            json.dump(self.data, file, indent=2)

    # Properties

    @property
    def edit(self) -> bool:
        return self.data['edit']
    
    @edit.setter
    def edit(self, b: bool):
        self.data['edit'] = b
    
    @property
    def size(self) -> int:
        return self.data['size']
    
    @size.setter
    def size(self, i: int):
        self.data['size'] = i
    
    @property
    def autoflush(self) -> bool:
        return self.data['autoflush']
    
    @autoflush.setter
    def autoflush(self, b: bool):
        self.data['autoflush'] = b

    @property
    def token(self) -> str:
        if (token := self.data['token']):
            return token
    
    @token.setter
    def token(self, s: str):
        self.data['token'] = s
    
    @property
    def prefix(self) -> str:
        return self.data['prefix']
    
    @prefix.setter
    def prefix(self, s: str):
        self.data['prefix'] = s