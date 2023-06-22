def is_mobile(request):
  if ("Mobile" in request.META['HTTP_USER_AGENT']):
    return 'base.html'
  else:
    return 'base-desktop.html'
