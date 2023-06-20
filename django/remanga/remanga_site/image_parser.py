import urllib.request

url = 'https://remanga.org/media/titles/martial_peak/56169d91c6668d8ab647b3c781e453fc.jpg'
#url.split('/')[-2] mkdir
filename = '56169d91c6668d8ab647b3c781e453fc.jpg' #url.split('/')[-1]
urllib.request.urlretrieve(url, filename)
