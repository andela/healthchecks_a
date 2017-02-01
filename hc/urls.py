from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('hc.accounts.urls')),
    url(r'^', include('hc.api.urls')),
    url(r'^', include('hc.front.urls')),
    url(r'^', include('hc.payments.urls')),
    url(r'^telegrambot/', include('telegrambot.urls', namespace="telegrambot")),

]
# #telegrambot
# urlpatterns = [command('start', StartView.as_command_view()),
#            command('author', AuthorCommandView.as_command_view()),
#            command('author_inverse', AuthorInverseListView.as_command_view()),
#            command('author_query', login_required(AuthorCommandQueryView.as_command_view())),
#            unknown_command(UnknownView.as_command_view()),
#            regex(r'author_(?P<name>\w+)', AuthorName.as_command_view()),
#
# ]
