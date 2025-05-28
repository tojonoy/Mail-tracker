from typing import Optional

class ApiResponseDto:

    def __init__(self,message:str,data,status:Optional[str]="SUCCESS"):
        self.status=status
        self.message=message
        self.data=data