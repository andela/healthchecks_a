from django.conf.urls import url
from hc.accounts import views

urlpatterns = [
    url(r'^login/$', views.login, name="hc-login"),
    url(r'^logout/$', views.logout, name="hc-logout"),
    url(r'^login_link_sent/$',
        views.login_link_sent, name="hc-login-link-sent"),

    url(r'^set_password_link_sent/$',
        views.set_password_link_sent, name="hc-set-password-link-sent"),

    url(r'^check_token/([\w-]+)/([\w-]+)/$',
        views.check_token, name="hc-check-token"),

    url(r'^profile/$', views.profile, name="hc-profile"),

    # Unsubscription urls
    url(r'^unsubscribe_reports/([\w-]+)/$',
        views.unsubscribe_reports, name="hc-unsubscribe-reports") , #monthly

    url(r'^unsubscribe_weekly_reports/([\w-]+)/$', 
        views.unsubscribe_weekly_reports, name="hc-unsubscribe-weekly-reports"),#weekly

    url(r'^unsubscribe_daily_reports/([\w-]+)/$', 
        views.unsubscribe_daily_reports, name="hc-unsubscribe-daily-reports"),#daily

    url(r'^set_password/([\w-]+)/$',
        views.set_password, name="hc-set-password"),

   url(r'^switch_team/([\w-]+)/$',
        views.switch_team, name="hc-switch-team"),


]
