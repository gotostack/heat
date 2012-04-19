import sys
import os
sys.path.append(os.environ['PYTHON_NOVACLIENT_SRC'])

import nose
import unittest
import mox
import json
import sqlalchemy

from nose.plugins.attrib import attr
from nose import with_setup

from tests.v1_1 import fakes
from heat.engine import resources
import heat.db as db_api
from heat.engine import parser

@attr(tag=['unit', 'resource'])
@attr(speed='fast')
class ResourcesTest(unittest.TestCase):
    def setUp(self):
        self.m = mox.Mox()
        self.cs = fakes.FakeClient()

    def tearDown(self):
        self.m.UnsetStubs()

    def test_initialize_instance_from_template(self):
        f = open('../../templates/WordPress_Single_Instance_gold.template')
        t = json.loads(f.read())
        f.close()

        params = {}
        parameters = {}
        params['KeyStoneCreds'] =  None
        t['Parameters']['KeyName']['Value'] = 'test'
        stack = parser.Stack('test_stack', t, 0, params)
 
        self.m.StubOutWithMock(db_api, 'resource_get_by_name_and_stack')
        db_api.resource_get_by_name_and_stack(None, 'test_resource_name',\
                                              stack).AndReturn(None)

        self.m.StubOutWithMock(resources.Instance, 'nova')
        resources.Instance.nova().AndReturn(self.cs)
        resources.Instance.nova().AndReturn(self.cs)
        resources.Instance.nova().AndReturn(self.cs)
        resources.Instance.nova().AndReturn(self.cs)

        
        print self.cs.flavors.list()[0].name 
        self.m.ReplayAll()
        t['Resources']['WebServer']['Properties']['ImageId']  = 'CentOS 5.2'
        t['Resources']['WebServer']['Properties']['InstanceType'] = '256 MB Server'
        instance = resources.Instance('test_resource_name',\
                                      t['Resources']['WebServer'], stack)

        instance.itype_oflavor['256 MB Server'] = '256 MB Server'
        instance.create()

   # allows testing of the test directly, shown below
    if __name__ == '__main__':
        sys.argv.append(__file__)
        nose.main()
   
