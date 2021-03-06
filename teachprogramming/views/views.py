from pyramid.view      import view_config
from pyramid.renderers import render_to_response
from pyramid.response  import Response
from pyramid.httpexceptions import HTTPFound

from . import web, etag
import teachprogramming.lib.make_ver  as make_ver
import teachprogramming.lib.constants as constants

import datetime
default_http_cache_duration = datetime.timedelta(seconds=0) #get_setting('web.cache.expire') 86400


@view_config(route_name='project', http_cache=default_http_cache_duration)
@etag()
@web
def project(request):
    return render_to_response(
        'teachprogramming:templates/html/projects/%(project_type)s/%(project)s.mako' % request.matchdict, 
        request.matchdict,
        request=request,
        # cache= ?? pass to mako template?
    )

@view_config(route_name='project_code', http_cache=default_http_cache_duration)
@etag()
@web
def project_code(request):
    code = '\n'.join( make_ver.make_ver(constants.project_filename_dict.format(**request.matchdict), ver_name=request.matchdict['version'], lang=request.matchdict['selected_lang'] ) )
    request.response.text = code
    # TODO: cache this response with beaker/dogpile?
    request.response.content_type = "text/plain"
    return request.response

#@view_config(route_name='select_language_redirect')
#def select_language_redirect(request):
#    request.session['selected_lang'] = request.matchdict['selected_lang'] #request.params.get('selected_lang', default_language)
#    return HTTPFound(location=request.referer)
