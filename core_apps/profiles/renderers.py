import json
from rest_framework.renderers import JSONRenderer
"""
    The custom renderers allow you to manipulate
    and format the response data in your APIs
    before it's returned to the client.
    By creating a custom renderer, you control how the data is
    structured and presented,
    which is especially useful when you need a consistent format
    or want to wrap data with additional fields like status_code.
"""



class ProfileJSONRender(JSONRenderer):
    """
        This class use default json renderer to render a profile
    """
    charset = 'utf-8'

    def render(self, data, accepted_media_type = None, renderer_context = None):
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)
        
        if errors is not None:
            return super(ProfileJSONRender, self).render(data)
        return json.dumps({"status_code": status_code, "profile": data}) # if any error presents
    

class ProfilesJSONRender(JSONRenderer):
    """
        This class use default json renderer to render a list of profiles
    """
    charset = 'utf-8'

    def render(self, data, accepted_media_type = None, renderer_context = None):
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)
        
        if errors is not None:
            return super(ProfilesJSONRender, self).render(data)
        return json.dumps({"status_code": status_code, "profiles": data})