from typing import List,Dict,Tuple

class Response():
    """
    Wrapper class for response json object
    """
    def __init__(self,user_id: int, version_num: int, description: str):
        self.user_id = user_id
        self.version_num = version_num
        self.description = description


    def get_response(self) -> Dict:
        response = dict()
        response['user_id'] = self.user_id
        response['version_num'] = self.version_num
        response['description'] = self.description
        return response