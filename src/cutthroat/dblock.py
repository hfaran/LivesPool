import fcntl

from tornado import options


class DBLock(object):

    """Context manager for synchronized DB access

    Usage:
       with DBLock():
          ...

    # Converted from the example here:
    # http://blog.vmfarms.com/2011/03/cross-process-locking-and.html
    """

    def __init__(self):
        self.filename = options.dblock_file
        # Create the lock if it does not already exist
        self.handle = open(self.filename, 'w')

    def __enter__(self):
        # Acquire lock
        fcntl.flock(self.handle, fcntl.LOCK_EX)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Release lock
        fcntl.flock(self.handle, fcntl.LOCK_UN)

    def __del__(self):
        self.handle.close()
