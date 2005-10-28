#
# Example PloneTestCase
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase

from zope.app.tests.placelesssetup import setUp, tearDown
from Acquisition import aq_base


class TestPloneTestCase(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        setUp()
        self.catalog = self.portal.portal_catalog
        self.workflow = self.portal.portal_workflow

    def testAddDocument(self):
        self.failIf(self.catalog(id='new'))
        self.folder.invokeFactory('Document', id='new')
        self.failUnless(hasattr(aq_base(self.folder), 'new'))
        self.failUnless(self.catalog(id='new'))

    def testPublishDocument(self):
        self.folder.invokeFactory('Document', id='new')
        self.setRoles(['Reviewer'])
        self.workflow.doActionFor(self.folder.new, 'publish')
        self.assertEqual(self.workflow.getInfoFor(self.folder.new, 'review_state'), 'published')
        self.failUnless(self.catalog(id='new', review_state='published'))

    def testRetractDocument(self):
        self.folder.invokeFactory('Document', id='new')
        self.setRoles(['Reviewer'])
        self.workflow.doActionFor(self.folder.new, 'publish')
        self.assertEqual(self.workflow.getInfoFor(self.folder.new, 'review_state'), 'published')
        self.setRoles(['Member'])
        self.workflow.doActionFor(self.folder.new, 'retract')
        self.assertEqual(self.workflow.getInfoFor(self.folder.new, 'review_state'), 'visible')

    def testEditDocument(self):
        self.folder.invokeFactory('Document', id='new')
        self.assertEqual(self.folder.new.EditableBody(), '')
        self.folder.new.edit('plain', 'data', file='', safety_belt='')
        self.assertEqual(self.folder.new.EditableBody(), 'data')

    def testGetterSkinScript(self):
        self.folder.invokeFactory('Document', id='new', title='Foo')
        self.assertEqual(self.folder.new.TitleOrId(), 'Foo')

    def testSetterSkinScript(self):
        self.folder.invokeFactory('Document', id='new')
        self.assertEqual(self.folder.new.EditableBody(), '')
        self.folder.new.document_edit('plain', 'data', title='Foo')
        self.assertEqual(self.folder.new.EditableBody(), 'data')

    def beforeTearDown(self):
        tearDown()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPloneTestCase))
    return suite

if __name__ == '__main__':
    framework()
