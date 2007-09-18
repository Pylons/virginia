from zope.pagetemplate import pagetemplatefile
from zope.interface import implements

from repoze.virginia.interfaces import IView

class mypt(pagetemplatefile.PageTemplateFile):
    def pt_getContext(self, args=(), **kw):
        rval = {'template': self,
                'args': args,
                'nothing': None,
                }
        rval.update(kw)
        rval.update(self.pt_getEngine().getBaseNames())
        return rval

    def __call__(self, *args, **kwargs):
        return self.pt_render(self.pt_getContext(args, **kwargs))


class PageTemplateView(object):
    implements(IView)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        f = mypt(self.context.filename)
        return f(context=self.context)
        
