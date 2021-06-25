import ldap

username = 'vikram.c.singh@ericsson.com'
password = 'P@ssw0rd@123'

def get_ldap_connection():
    conn = ldap.initialize('LDAP://ericsson.se')
    conn.protocol_version = ldap.VERSION3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    return conn

def get_info(username, password):
        conn = get_ldap_connection()
        bind = conn.simple_bind_s(username, password)
        base = "dc=ericsson, dc=se"
        criteria = "(&(mail={}))".format(username)
        attributes = ['displayName', 'signum']
        result = conn.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
        for dn, entry in result:
            if isinstance(entry, dict):
                name = entry['displayName']
                signum = entry['eriSignumUpperCase']
                name = [n.decode('utf-8') for n in name]
                signum = [n.decode('utf-8') for n in signum]
                #name = name[0]
                #signum = signum[0]
                return(name, signum)

get_info(username, password)