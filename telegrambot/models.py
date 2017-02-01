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
