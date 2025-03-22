class CategoryNotFoundException(Exception):
    pass


class CategoryAlreadyExistsException(Exception):
    pass


class StockItemNotFoundException(Exception):
    pass


class StockItemAlreadyExistsException(Exception):
    pass


class RoleNotFoundException(Exception):
    pass


class RoleAlreadyExistsException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass


class WrongPasswordException(Exception):
    pass


class UserAccountIsDisabledException(Exception):
    pass


class NoEnvirnomentVariableException(Exception):
    pass


class InvalidRoleException(Exception):
    pass


class WrongUsernameException(Exception):
    pass


class WrongTokenTypeException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class TokenExpiredException(Exception):
    pass
