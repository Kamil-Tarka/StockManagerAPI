class CategoryNotFoundException(Exception):
    """Exception raised when a category is not found."""

    pass


class CategoryAlreadyExistsException(Exception):
    """Exception raised when a category already exists."""

    pass


class StockItemNotFoundException(Exception):
    """Exception raised when a stock item is not found."""

    pass


class StockItemAlreadyExistsException(Exception):
    """Exception raised when a stock item already exists."""

    pass


class RoleNotFoundException(Exception):
    """Exception raised when a role is not found."""

    pass


class RoleAlreadyExistsException(Exception):
    """Exception raised when a role already exists."""

    pass


class RoleNotCreatedException(Exception):
    """Exception raised when a role could not be created."""

    pass


class UserNotFoundException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass


class WrongPasswordException(Exception):
    pass


class UserAccountIsDisabledException(Exception):
    pass


class UserNotCreatedException(Exception):
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
