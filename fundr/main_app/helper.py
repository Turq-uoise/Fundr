def is_mobile(request):
  return "Mobile" in request.META['HTTP_USER_AGENT']
