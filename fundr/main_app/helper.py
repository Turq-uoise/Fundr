def is_mobile(request):
  print(request.META['HTTP_USER_AGENT'])
  return "Mobile" in request.META['HTTP_USER_AGENT']