def is_mobile(request):
  if "Mobile" in request.META['HTTP_USER_AGENT']:
     template = 'base.html'
  else:
     template = 'base-desktop.html'
  return template