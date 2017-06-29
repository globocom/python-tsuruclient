from tsuruclient.base import Manager as Base
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class Manager(Base):
    """
    Manage App resources.
    """

    def list(self, **kwargs):
        """
        Get a list of apps by query string.
        """
        return self.request("get", "/apps?{}".format(urlencode(kwargs)))

    def get(self, appname):
        """
        Get an app.
        """
        return self.request("get", "/apps/{}".format(appname))

    def remove(self, appname):
        """
        Remove an app.
        """
        return self.request("delete", "/apps/{}".format(appname))

    def create(self, **kwargs):
        """
        Create an app.
        """
        return self.request("post", "/apps", stream=True, data=kwargs)
