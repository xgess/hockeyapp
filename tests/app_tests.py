"""
Test the Application class

"""
import mock
import httmock
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from hockeyapp import app


class ApplicationTestCase(unittest.TestCase):
    TOKEN = 'abcdef0123456789abcdef0123456789'
    APP_IDENTIFIER = 'zyxw98765'

    def setUp(self):
        self.app = app.Application(self.TOKEN)
        self.applications = app.Applications(self.TOKEN)

    def test_invalid_identifier_number(self):
        self.assertRaises(ValueError, self.app._check_app_id, 1)

    def test_invalid_identifier_format(self):
        self.assertRaises(ValueError, self.app._check_app_id, 'foo')

    @mock.patch.object(app.Applications, '_get')
    def test_list(self, get):
        self.applications.list()
        get.assert_called_with(uri_parts=['apps'])
        get.return_value.__getitem__.assert_called_with('apps')

    @mock.patch.object(app.Application, '_check_app_id')
    @mock.patch.object(app.Application, '_get')
    def test_statistics(self, get, _):
        application = app.Application(self.TOKEN, app_id=self.APP_IDENTIFIER)
        application.statistics()
        get.assert_called_with(uri_parts=['apps', self.APP_IDENTIFIER, 'statistics'])

    @mock.patch.object(app.Application, '_check_app_id')
    @mock.patch.object(app.Application, '_get')
    def test_versions(self, get, _):
        application = app.Application(self.TOKEN, app_id=self.APP_IDENTIFIER)
        application.versions()
        get.assert_called_with(uri_parts=['apps', self.APP_IDENTIFIER, 'app_versions'])

    @mock.patch.object(app.Application, '_check_app_id')
    @mock.patch.object(app.Application, '_get')
    def test_crash_group_search(self, get, _):
        query_string = 'created_at:[\"2014-05-01T00:00\"+TO+\"2014-05-30T23:59\"]'
        expected_request_params = 'order=asc&page=1&per_page=25&query=created_at:["2014-05-01T00:00"+TO+"2014-05-30T23:59"]&symbolication=0'
        expected_uri_parts = ['apps', self.APP_IDENTIFIER, 'crash_reasons', 'search']
        application = app.Application(self.TOKEN, app_id=self.APP_IDENTIFIER)

        application.crash_group_search(query_string)

        get.assert_called_with(uri_parts=expected_uri_parts, params=expected_request_params)
