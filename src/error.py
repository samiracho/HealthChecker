class HealthError(object):

    def __init__(self, service, errors=[]):
        """
        :param service: Service name
        :param errors: List of errors detected during the health check
        """
        self.service = service
        self.errors = errors

    def getJson(self):
        return {'service': self.service, 'description': str(self.errors).strip('[]')}
