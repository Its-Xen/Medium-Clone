from rest_framework.exceptions import APIException


class YouHaveAlreadyRated(APIException):
    status_code = 400
    default_detail = "have already rated this article"
    default_code = "bad_request"
