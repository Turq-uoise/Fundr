def is_mobile(request):
  print(request.META['HTTP_USER_AGENT'])
  if( "Mobile" in request.META['HTTP_USER_AGENT']):
    return 'base.html'
  else:
    return 'base-desktop.html'