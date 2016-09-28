from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ### Test that team access works
    def test_team_can_access_check(self):
    	self.client.login(username="bob@example.org", password="password")
    	url = "/accounts/switch_team/%s/" % self.alice.username
    	r = self.client.get(url)
    	self.assertEquals(r.status_code, 302)
