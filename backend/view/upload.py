from lib import upload
from model.upload import UserUpload
from slim.base.permission import Permissions
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from view import route
from view.permissions import permissions_add_all
from view.user import UserMixin


@route('upload')
class TopicView(UserMixin, PeeweeView):
    model = UserUpload

    @route.interface('POST')
    async def token(self):
        user = self.current_user
        if user:
            if self.current_role in ('user', 'admin', 'superuser'):
                return self.finish(RETCODE.SUCCESS, upload.get_token(user.id.hex()))
        self.finish(RETCODE.FAILED)

    @route.interface('POST')
    async def qn_callback(self):
        ua = self.headers.get('User-Agent', None)
        if not (ua and ua.startswith('qiniu-callback')):
            return self.finish(RETCODE.FAILED)

        auth = self.headers.get('Authorization', None)
        if auth:
            if upload.verify_callback(auth, self._request.url, str(await self._request.content.read(), 'utf-8')):
                # 鉴权成功，确认为七牛服务器回调。
                return self.finish(RETCODE.SUCCESS)

        self.finish(RETCODE.FAILED)

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('hash', 'upload_entity')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permissions_add_all(permission)