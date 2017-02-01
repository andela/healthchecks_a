#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegrambot.models import User, Chat, Bot, AuthToken
from telegrambot.test import factories, testcases
from factory import DjangoModelFactory, Sequence
from tests.models import Author
from django.core.urlresolvers import reverse
from rest_framework import status
from django.test.utils import override_settings
from django.conf import settings
from django.apps import apps


class TestLoginRequiredBotView(testcases.BaseTestBot):

    author_login_required_not_auth = {'in': '/author_auth',
                                      'out': {'parse_mode': 'Markdown',
                                              'reply_markup': '',
                                              'text': "You need an *authenticated chat*" +
                                                  " to perform this action please login" +
                                                      " [here](https://example.com/telegrambot/auth/"
                                              }
                                      }

    author_login_required_authed = {'in': '/author_auth',
                                    'out': {'parse_mode': 'Markdown',
                                            'reply_markup': '/author author_1',
                                            'text': "Select from list:\nauthor_1"
                                            }
                                    }

    def test_login_required_not_auth(self):
        AuthorFactory(name="author_1")
        self._test_message_ok(self.author_login_required_not_auth)

    def test_login_required_already_auth(self):
        token = factories.AuthTokenFactory()
        token.save()
        chat, _ = Chat.objects.get_or_create(**self.update.message.chat.to_dict())
        token.chat_api = chat
        token.save()
        AuthorFactory(name="author_1")
        self._test_message_ok(self.author_login_required_authed)

    @override_settings(TELEGRAM_BOT_TOKEN_EXPIRATION='-1')
    def test_login_required_expired_token(self):
        token = factories.AuthTokenFactory()
        token.save()
        chat, _ = Chat.objects.get_or_create(**self.update.message.chat.to_dict())
        token.chat_api = chat
        token.save()
        AuthorFactory(name="author_1")
        self._test_message_ok(self.author_login_required_not_auth)
