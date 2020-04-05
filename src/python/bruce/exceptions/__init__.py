class BruceError(Exception):
    pass


class FailedTaskException(BruceError):
    pass


class TaskNotFoundException(BruceError):
    pass
