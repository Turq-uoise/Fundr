def is_mobile(request):
  if "Mobile" in request.META['HTTP_USER_AGENT']:
     template = 'base.html'
  else:
     template = 'base-desktop.html'
  return template


def formatPostcode(postcode):
   arr = [x for x in postcode]
   arr[-3:-3] = ' '
   return ''.join(arr)
