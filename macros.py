import csv, glob, json
from operator import itemgetter

def twitter():
	return """<a href="#aftertw" id="skiptw">Skip tweets</a><a class="twitter-timeline" href="https://twitter.com/c4dm" data-widget-id="561187870955040769" data-chrome="nofooter" width="300" height="900">Tweets by @c4dm</a><script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script><br /><a name="aftertw" id="aftertw"></a>"""


def peoplelist(criteria=None):
	if criteria==None:
		criteria = {}
	ret = "<table width='100%' class='peoplelist'>"
	ret += "\n  <tr><th>Name</th><th>Project/interests/keywords</th></tr>"

	peopledata = {}
	for fpath in glob.glob("input/people_data/*.json"):
		with open(fpath, 'rb') as jsonfp:
			aperson = json.load(jsonfp)
			aperson['sortkey'] = aperson['name'].strip().split(' ')[-1]
			for atheme in aperson['themes']:
				aperson['theme_%s' % atheme] = '1'
			peopledata[aperson['name']] = aperson

	for x in sorted(peopledata.values(), key=itemgetter('sortkey')):
		if any([x.get(key, '') != val for key, val in criteria.items()]):
			continue
		if x.get('url', '') != '':
			htmlname = "<a href='%s'>%s</a>" % (x['url'], x.get('name'))
		else:
			htmlname = x.get('name')
		if x.get('acadposition', '') != '':
			htmlname += "<br />%s" % (x.get('acadposition'))
		blurb = x.get('blurb', '')
		if blurb in [None, 'None', '*']:
			blurb = ''
		ret += "\n   <tr><td>%s</td><td>%s</td></tr>" % (htmlname, blurb)
	ret += "</table>"
	return ret

def publicationslist(year):
	ret = """<p>Select year: <strong>%i</strong>""" % year
	for otheryear in range(year-1, 1995, -1):
		ret += " <a href='pubs%i.html'>%i</a>" % (otheryear, otheryear)
	ret +="""
<h2>%i</h2>""" % year
	# Now load the content pre-rendered by bibtex2html
	with open("input/pubs%i_raw.html" % year, "r") as fp:
		data = ''.join(fp.readlines())
	ret += data
	return ret

def pagesourceurl():
	#return "https://github.com/c4dm/c4dmpoole/tree/master/%s" % (str(page))
        return "https://github.com/c4dm/c4dmpoole/edit/master/%s" % (str(page))


