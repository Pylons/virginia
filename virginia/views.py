import os
import mimetypes

mimetypes.add_type('text/html', '.stx')
mimetypes.add_type('application/pdf', '.pdf')

from zope.structuredtext import stx2html

from webob import Response
from webob.exc import HTTPFound

from pyramid.view import render_view_to_response
from pyramid.view import view_config

from virginia.interfaces import IFile
from virginia.interfaces import IDirectory

# default views: router will call these 

@view_config(context=IFile, permission='repoze.view')
def file_view(context, request):
    dirname, filename = os.path.split(context.path)
    name, ext = os.path.splitext(filename)
    result = render_view_to_response(context, request, ext)
    return result

@view_config(context=IDirectory, permission='repoze.view')
def directory_view(context, request):
    path_info = request.environ['PATH_INFO']
    if not path_info.endswith('/'):
        response = HTTPFound(location=path_info + '/')
        return response

    defaults = ('index.html', 'index.stx', 'index.pt')
    for name in defaults:
        try:
            index = context[name]
        except KeyError:
            continue
        return file_view(index, request)
    response = Response('No default view for %s' % context.path)
    response.content_type = 'text/plain'
    return response

# custom views: FileView will call these

@view_config(context=IFile, permission='repoze.view', name='.stx')
def structured_text_view(context, request):
    """ Filesystem-based STX view
    """
    result = stx2html(context.source)
    response = Response(result)
    response.content_type = 'text/html'
    return response

@view_config(context=IFile, permission='repoze.view', name='.html')
@view_config(context=IFile, permission='repoze.view', name='.pdf')
@view_config(context=IFile, permission='repoze.view', name='.txt')
@view_config(context=IFile, permission='repoze.view', name='.jpg')
def raw_view(context, request):
    """ Just return the source raw.
    """
    response = Response(context.source)
    dirname, filename = os.path.split(context.path)
    name, ext = os.path.splitext(filename)
    mt, encoding = mimetypes.guess_type(filename)
    response.content_type = mt or 'text/plain'
    return response
