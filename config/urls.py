from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.flatpages import views as flatpage_views
from django.contrib.flatpages.sitemaps import FlatPageSitemap

# NOTE: This is needed to control language switcher
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from radio_funk.mode.views import enable_dark_mode, enable_light_mode
# TODO: Add google analytics client_secret file
# from jet.dashboard.dashboard_modules import google_analytics_views
# from jet.dashboard.dashboard import Dashboard, AppIndexDashboard

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from filebrowser.sites import site as filebrowser
# from photologue.sitemaps import GallerySitemap, PhotoSitemap

from config.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    # "photologue_galleries": GallerySitemap,
    # "photologue_photos": PhotoSitemap,
}

# TODO: Add google analytics client_secret file
# class CustomIndexDashboard(Dashboard):
#     columns = 3

#     def init_with_context(self, context):
#        self.available_children.append(google_analytics_views.GoogleAnalyticsVisitorsTotals)
#        self.available_children.append(google_analytics_views.GoogleAnalyticsVisitorsChart)
#        self.available_children.append(google_analytics_views.GoogleAnalyticsPeriodVisitors)

urlpatterns = i18n_patterns(
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        _("discovery/"), TemplateView.as_view(template_name="pages/search.html"), name="discover"
    ),
    path(
        _("radio/"), TemplateView.as_view(template_name="pages/about.html"), name="radio"
    ),
    path(
        _("podcasts/"), TemplateView.as_view(template_name="pages/about.html"), name="podcasts"
    ),
    path(
        _("history/"), TemplateView.as_view(template_name="pages/about.html"), name="history"
    ),
    path(
        _("events/"), TemplateView.as_view(template_name="pages/about.html"), name="events"
    ),
    path("dark_mode/", view=enable_dark_mode, name="mode"),
    path("light_mode/", view=enable_light_mode, name="lmode"),

    # Django Admin, use {% url 'admin:index' %}
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.ADMIN_DOC_URL, include("django.contrib.admindocs.urls")),

    # User management
    path('rosetta/', include('rosetta.urls')),
    # path('photologue/', include('photologue.urls', namespace='photologue')),
    path(_("users/"), include("radio_funk.users.urls", namespace="users")),
    path(_("accounts/"), include("allauth.urls")),
    path(_("podcast/"), include("podcast.urls")),

    # Your stuff: custom urls includes go here
    path('tinymce/', include('tinymce.urls')),
    path('unicorn/', include('django_unicorn.urls')),
    path(settings.ADMIN_FILEBROWSER_URL, filebrowser.urls),

    path("__reload__/", include("django_browser_reload.urls")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

# flatpages
if flatpage_views:
    urlpatterns += [
        path(_("terms/"), flatpage_views.flatpage, {"url": "/terms/"}, name="terms"),
        path(_("cookies/"), flatpage_views.flatpage, {"url": "/cookies/"}, name="cookies"),
        path(_("privacy/"), flatpage_views.flatpage, {"url": "/privacy/"}, name="privacy"),
    ]

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    path("sitemap.xml/", sitemap, kwargs={"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns


admin.site.site_header = _("Dashboard - Radio Funk")
admin.site.site_title = _("RadioFunk Dashboard")
admin.site.index_title = _("RadioFunk Dashboard")
