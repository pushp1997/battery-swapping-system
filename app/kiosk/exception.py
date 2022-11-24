class Invalid_User_Input(Exception):
    def __str__(self) -> str:
        return "Invalid user input provided"


class User_Already_Exists_Email(Exception):
    def __str__(self) -> str:
        return "Either User email id or License Number is not unique."


class User_Already_Exists_License(Exception):
    def __str__(self) -> str:
        return "User license number is not unique."


class Payment_Failed(Exception):
    def __str__(self) -> str:
        return "Payment failure please try again after sometime"
