from hc.api.models import Channel
from hc.test import BaseTestCase


class VerifyEmailTestCase(BaseTestCase):

    def setUp(self):
        super(VerifyEmailTestCase, self).setUp()
        self.channel = Channel(user=self.alice, kind="email")
        self.channel.value = "alice@example.org"
        self.channel.save()

    def test_it_works(self):
        token = self.channel.make_token()
        url = "/integrations/%s/verify/%s/" % (self.channel.code, token)

        r = self.client.post(url)
        self.assertEqual(r.status_code == 200, r.status_code)

        channel = Channel.objects.get(code=self.channel.code)
        self.assertTrue(channel.email_verified)

    def test_it_handles_bad_token(self):
        url = "/integrations/%s/verify/bad-token/" % self.channel.code

        r = self.client.post(url)
        self.assertEqual(r.status_code == 200, r.status_code)

        channel = Channel.objects.get(code=self.channel.code)
        self.assertFalse(channel.email_verified)

    def test_missing_channel(self):
        # Valid UUID, and even valid token but there is no channel for it:
        code = "6837d6ec-fc08-4da5-a67f-08a9ed1ccf62"
        token = self.channel.make_token()
        url = "/integrations/%s/verify/%s/" % (code, token)

        r = self.client.post(url)
        self.assertEqual(r.status_code, 404)
