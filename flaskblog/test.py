import ldap

username = 'vikram.c.singh@ericsson.com'
password = 'P@ssw0rd@123'

l = ldap.initialize('LDAP://ericsson.se')
try:
    l.protocol_version = ldap.VERSION3
    l.set_option(ldap.OPT_REFERRALS, 0)
 
    bind = l.simple_bind_s(username, password)
 
    base = "dc=ericsson, dc=se"
    criteria = "(&(mail={}))".format(username)
    attributes = ['displayName', 'eriSignumUpperCase']
    result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)

    name = ""
    signum = ""
    for dn, entry in result:
        if isinstance(entry, dict):
            name = entry['displayName']
            signum = entry['eriSignumUpperCase']
            name = [n.decode('utf-8') for n in name]
            signum = [n.decode('utf-8') for n in signum]
            name = name[0]
            signum = signum[0]
            print(name, signum)
 
    #results = [entry for dn, entry in result if isinstance(entry, dict)]
    #name = [r['displayName'] for r in results]
    #print(name)
finally:
    l.unbind()