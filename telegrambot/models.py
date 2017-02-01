from django.db import models
from django.conf import settings
from telegram import Bot as BotAPI
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from telegrambot.models import User
from telegrambot.handlers import HandlerResolver
from telegrambot.handlers import HandlerNotFound

logger = logging.getLogger(__file__)


class Bot(models.Model):
    token = models.CharField(_('Token'), max_length=100, db_index=True)
    user_api = models.OneToOneField(User, verbose_name=_("Bot User"), related_name='bot',
                                    on_delete=models.CASCADE, blank=True, null=True)
    enabled = models.BooleanField(_('Enable'), default=True)
    created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Date Modified'), auto_now=True)

    class Meta:
        verbose_name = _('Bot')
        verbose_name_plural = _('Bots')

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self._bot = None
        if self.token:
            self._bot = BotAPI(self.token)

    def __str__(self):
        return "%s" % (self.user_api.first_name or self.token if self.user_api else self.token)

    def handle(self, update):
        handlerconf = settings.TELEGRAM_BOT_HANDLERS_CONF
        resolver = HandlerResolver(handlerconf)
        try:
            resolver_match = resolver.resolve(update)
        except HandlerNotFound:
            logger.warning("Handler not found for %s" % update)
        else:
            callback, callback_args, callback_kwargs = resolver_match
            callback(self, update, **callback_kwargs)

    def send_message(self, chat_id, text, parse_mode=None, disable_web_page_preview=None, **kwargs):
        self._bot.sendMessage(chat_id=chat_id, text=text, parse_mode=parse_mode,
                              disable_web_page_preview=disable_web_page_preview, **kwargs)

class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(_('First name'), max_length=255)
    last_name = models.CharField(_('Last name'), max_length=255, blank=True, null=True)
    username = models.CharField(_('User name'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return "%s" % self.first_name


class Chat(models.Model):

    PRIVATE, GROUP, SUPERGROUP, CHANNEL = 'private', 'group', 'supergroup', 'channel'

    TYPE_CHOICES = (
        (PRIVATE, _('Private')),
        (GROUP, _('Group')),
        (SUPERGROUP, _('Supergroup')),
        (CHANNEL, _('Channel')),
    )

    id = models.BigIntegerField(primary_key=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')

    def __str__(self):
        return "%s" % (self.title or self.username)

    def is_authenticated(self):
        return hasattr(self, 'auth_token') and not self.auth_token.expired()
