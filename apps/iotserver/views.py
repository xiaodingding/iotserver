from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from users.models import User, LoginLog
# from assets.models import Asset
from devm.models import device
from terminal.models import Session
from common.utils import get_logger
# from json

logger = get_logger(__file__)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    session_week = None
    session_month = None
    session_month_dates = []
    session_month_dates_archive = []

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('assets:user-asset-list')
        return super(IndexView, self).get(request, *args, **kwargs)

    @staticmethod
    def get_user_count():
        return User.objects.filter(role__in=('Admin', 'User')).count()

    @staticmethod
    def get_asset_count():
        return device.Device.objects.all().count()

    @staticmethod
    def get_online_user_count():
        # return len(set(Session.objects.filter(is_finished=False).values_list('username', flat=True)))
        return 0


    @staticmethod
    def get_online_session_count():
        return Session.objects.filter(is_finished=False).count()


    def get_top5_user_a_week(self):
        return self.session_week.values('username').annotate(total=Count('username')).order_by('-total')[:5]


    def get_week_login_user_count(self):
        # return self.session_week.values('user').distinct().count()
        return self.session_week.values('username').distinct().count()

    def get_week_login_asset_count(self):
        return self.session_week.values('username').distinct().count()


    def get_month_day_metrics(self):
        month_str = [d.strftime('%m-%d') for d in self.session_month_dates] or ['0']
        return month_str

    def get_month_login_metrics(self):
        return [self.session_month.filter(datetime__date=d).count()
                for d in self.session_month_dates]

    def get_month_active_user_metrics(self):
        if self.session_month_dates_archive:
            return [q.values('username').distinct().count()
                    for q in self.session_month_dates_archive]
        else:
            return [0]

    def get_month_active_asset_metrics(self):
        if self.session_month_dates_archive:
            return [q.values('ip').distinct().count()
                    for q in self.session_month_dates_archive]
        else:
            return [0]

    def get_month_active_user_total(self):
        return self.session_month.values('username').distinct().count()
        # return 0

    def get_month_inactive_user_total(self):
        return User.objects.all().count() - self.get_month_active_user_total()

    def get_month_active_asset_total(self):
        # return self.session_month.values('asset').distinct().count()
        return 3

    def get_month_inactive_asset_total(self):
        # return Asset.objects.all().count() - self.get_month_active_asset_total()
        # return 0
        return 5

    @staticmethod
    def get_user_disabled_total():
        return User.objects.filter(is_active=False).count()

    @staticmethod
    def get_asset_disabled_total():
        # return device.Device.objects.filter(is_active=False).count()
        return 4

    def get_week_top10_asset(self):
        assets = list(self.session_week.values('ip').annotate(total=Count('ip')).order_by('-total')[:10])
        for asset in assets:
            last_login = self.session_week.filter(ip=asset["ip"]).order_by('datetime').last()
            asset['last'] = last_login
        return assets

    def get_week_top10_user(self):
        login_user = LoginLog.objects.all().values('username').annotate(total=Count('username')).order_by('-total')[:10]
        # logger.debug("login_user:{}".format(login_user.query) )
        for user in list(login_user):
            last_login = LoginLog.objects.filter(username=user["username"]).order_by('datetime').last()
            user['last'] = last_login
        return login_user

    def get_last10_sessions(self):
        login_user = LoginLog.objects.all().order_by('-datetime')[:10].values()
        user_list = []
        for user in list(login_user):
            try:
                user['avatar_url'] = User.objects.get(username=user['username']).avatar_url()
            except User.DoesNotExist:
                user['avatar_url'] = User.objects.first().avatar_url()
            user_list.append(user)
        return user_list

    def get_context_data(self, **kwargs):
        week_ago = timezone.now() - timezone.timedelta(weeks=1)
        month_ago = timezone.now() - timezone.timedelta(days=30)
        # self.session_week = Session.objects.filter(date_start__gt=week_ago)
        # self.session_month = Session.objects.filter(date_start__gt=month_ago)
        self.session_week = LoginLog.objects.filter(datetime__gt=week_ago)
        self.session_month = LoginLog.objects.filter(datetime__gt=month_ago)
        self.session_month_dates = self.session_month.dates('datetime', 'day')
        self.session_month_dates_archive = [
            self.session_month.filter(datetime__date=d)
            for d in self.session_month_dates
        ]

        context = {
            'assets_count': self.get_asset_count(),
            'users_count': self.get_user_count(),
            'online_user_count': self.get_online_user_count(),
            'online_asset_count': self.get_online_session_count(),
            'user_visit_count_weekly': self.get_week_login_user_count(),
            'asset_visit_count_weekly': self.get_week_login_asset_count(),
            'user_visit_count_top_five': self.get_top5_user_a_week(),
            'month_str': self.get_month_day_metrics(),
            'month_total_visit_count': self.get_month_login_metrics(),
            'month_user': self.get_month_active_user_metrics(),
            'mouth_asset': self.get_month_active_asset_metrics(),
            'month_user_active': self.get_month_active_user_total(),
            'month_user_inactive': self.get_month_inactive_user_total(),
            'month_user_disabled': self.get_user_disabled_total(),
            'month_device_active': self.get_month_active_asset_total(),
            'month_device_inactive': self.get_month_inactive_asset_total(),
            'month_device_disabled': self.get_asset_disabled_total(),
            'week_asset_hot_ten': self.get_week_top10_asset(),
            'last_login_ten': self.get_last10_sessions(),
            'week_user_hot_ten': self.get_week_top10_user(),
        }

        kwargs.update(context)
        return super(IndexView, self).get_context_data(**kwargs)
