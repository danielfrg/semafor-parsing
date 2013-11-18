from semafor.master.worker import tasks

#print tasks.create_instances.delay(2)

urls = ['http://brandednoise.com/2013/07/28/the-wabi-sabi-edge/',
'http://annaleawest.com/2013/11/05/cancer-cant-take-a-joke/',
'http://qz.com/145666/404-and-fail-are-the-most-popular-words-of-2013/',
'http://thisclimbingbean.wordpress.com/2013/10/24/lessons-in-feminism-from-my-father/']

from semafor.master.test_long import urls as urls_long

print tasks.semafor_parse.delay(urls, n_instances=1)
