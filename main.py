from flask import Flask, render_template, make_response

app = Flask(__name__)

DEBUG = False

# Default URLs (deprecated, still used)
links = ['https://femmessor.com/accueil'
,'https://femmessor.com/abonnement-infolettre'
,'https://fr.linkedin.com/company/femmessor-qu%C3%A9bec'
,'https://twitter.com/femmessor'
,'https://www.instagram.com/femmessor/'
,'https://www.youtube.com/channel/UCtul9JAsLW-vB_KrlGSxHOw'
,'18445237767']

icons = ['http://femmessor.com/signature/Logo-Femmessor.png'
,'http://femmessor.com/signature/Facebook-Femmessor.png'
,'http://femmessor.com/signature/LinkedIn-Femmessor.png'
,'http://femmessor.com/signature/Twitter-Femmessor.png'
,'http://femmessor.com/signature/Instagram-Femmessor.png'
,'http://femmessor.com/signature/Youtube-Femmessor.png'
,'http://femmessor.com/signature/Facebook-Femmessor-MTL.png'
,'https://femmessor.com/signature/Facebook-Femmessor-Laval.png'
,'https://femmessor.com/signature/VCard4.png']


# Default URLs (used for social media)
infoDefaults = {
    'website' : {
        'url': 'https://femmessor.com/accueil',
        'icon':'https://femmessor.com/themes/default/images/fr/logo-home-v2.png'},
    'infolettre' : {
        'url': 'https://femmessor.com/abonnement-infolettre',
         'icon':''},
    'phone' : {
        'url': '18445237767',
        'icon':''},
    'vCard' : {
        'url': '18445237767', 'icon':'https://femmessor.com/signature/VCard4.png'},
    'Facebook1' : {
        'url': 'https://www.facebook.com/Femmessorqc/',
        'icon':'http://femmessor.com/signature/Facebook-Femmessor.png'},
    'Facebook2' : {
        'url': '',
        'icon':'http://femmessor.com/signature/Facebook-Femmessor.png'},
    'LinkedIn' : {
        'url': 'https://fr.linkedin.com/company/femmessor-qu%C3%A9bec',
        'icon':'http://femmessor.com/signature/LinkedIn-Femmessor.png'},
    'Twitter' : {
        'url': 'https://twitter.com/femmessor',
        'icon':'http://femmessor.com/signature/Twitter-Femmessor.png'},
    'Instagram' : {
        'url': 'https://www.instagram.com/femmessor/',
        'icon':'http://femmessor.com/signature/Instagram-Femmessor.png'},
    'YouTube' : {
        'url': 'https://www.youtube.com/channel/UCtul9JAsLW-vB_KrlGSxHOw',
        'icon':'http://femmessor.com/signature/Youtube-Femmessor.png'},
}

# spreadsheet positions of social media overrides
socialMediaMapping = {
    'Facebook1': 12,
    'Facebook2': 13,
    'LinkedIn' : 14,
    'Twitter' : 15,
    'Instagram' : 16,
    'YouTube' : 17
}

def buildInfoDict(info):

    infoDict = copy.deepcopy(infoDefaults)

    # Override default URLs when relevant.
    for k, i in socialMediaMapping.items():
        if info[i]:
            infoDict[k]['url'] = info[i]

    # e.dalphond exceptions, she has 2 FB accounts w/ specific icons.
    # UPDATE 2019/12/04 : not needed anymore.
    #if info[5] == 'e.dalphond@femmessorqc.com':
    #    infoDict['Facebook1']['icon'] = 'https://femmessor.com/signature/Facebook-Femmessor-Laval.png'
    #    infoDict['Facebook2']['icon'] = 'http://femmessor.com/signature/Facebook-Femmessor-MTL.png'

    # generate vcard URL
    infoDict['vCard']['url'] = 'http://femqsignatures.innovsa.ca/%s/vcard' % info[5]

    if DEBUG:
        print("***INFO***")
        for i in range(len(info)):
            print(i, info[i])
        print("***INFODEFAULTS***")
        for k, v in infoDefaults.items():
            print(k, v)
        print("***INFODICT***")
        for k, v in infoDict.items():
            print(k, v)

    return infoDict



@app.route('/<email>/gmail')
def gmail(email):
    info = gsheet.getInfo(email)
    infoDict = buildInfoDict(info)
    return render_template('gmail_modele.html', info=info, links=links, icons=icons, infoDict=infoDict)

@app.route('/<email>/pipedrive')
def pipedrive(email):
    info = gsheet.getInfo(email)
    infoDict = buildInfoDict(info)
    return render_template('ppd_modele.html', info=info, links=links, icons=icons, infoDict=infoDict)

@app.route('/<email>/vcard')
def vcard(email):
    info = gsheet.getInfo(email)
    resp = make_response(render_template('vcard.vcf', info=info, links=links, icons=icons, mimetype='text/vcard'))
    resp.headers['Content-type'] = 'text/vcard; charset=utf-8'
    resp.headers['Content-Disposition'] = 'attachment; filename = %s %s.vcf' % (info[1], info[2])
    return resp


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)