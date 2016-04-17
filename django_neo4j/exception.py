# coding=utf-8


class _ErrorMessageMixin(object):
    def __init__(self):
        self.__message = None

    @property
    def message(self):
        return self.__message

    def __str__(self):
        return str(self.__message)

    def __unicode__(self):
        return self.__message


class DjangoNeo4jError(RuntimeError):
    pass


class OperationError(DjangoNeo4jError):
    pass


class OperationInitializationError(OperationError, ValueError, _ErrorMessageMixin):
    def __init__(self, operation, cause):
        super(OperationInitializationError, self).__init__()
        self.__message = u'operation {}: {}'.format(
            operation.name,
            cause,
        )


class OperationImplementationError(OperationError, NotImplementedError, _ErrorMessageMixin):
    def __init__(self, operation, method):
        super(OperationImplementationError, self).__init__()
        self.__message = u'operation {} method {} is not implemented'.format(
            operation.name,
            method,
        )


class OperationArgumentTypeError(OperationError, ValueError, _ErrorMessageMixin):
    def __init__(self, operation, arg):
        super(OperationArgumentTypeError, self).__init__()
        self.__message = u'operation {} argument of type {} not in types: {}'.format(
            operation.name,
            type(arg),
            operation.valid_types,
        )


class OperationArgumentMismatchError(OperationError, ValueError, _ErrorMessageMixin):
    def __init__(self, operation, a, b):
        super(OperationArgumentMismatchError, self).__init__()
        self.__message = u'operation {} with arguments of type {} and {} are not allowed together'.format(
            operation.name,
            type(a),
            type(b),
        )


class OperationArityError(OperationError, ValueError, _ErrorMessageMixin):
    def __init__(self, operation, given_arity):
        super(OperationArityError, self).__init__()
        self.__message = u'operation {} with arity {} given invalid arity of {}'.format(
            operation.name,
            operation.arity,
            given_arity,
        )


class OperationZeroDivisionError(OperationError, ZeroDivisionError):
    pass
