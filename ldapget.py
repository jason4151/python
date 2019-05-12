#!/usr/bin/python

import os, ldap, getpass

server = "ldaphost"
username = "uid=jason4151,ou=people,dc=example,dc=com"
password = getpass.getpass()

try:
    l = ldap.open(server)
    l.simple_bind_s(username, password)
    print "Successfully bound to server.\n"
except ldap.LDAPError, e:
    print e
    print "Could not connect to LDAP server.\n"

baseDN = "ou=people,ou=people,dc=example,dc=com"
retrieveAttributes = None
searchScope = ldap.SCOPE_SUBTREE
search = raw_input("Username to search for? ")

try:
    ldap_result_id = l.search(baseDN, searchScope, search, retrieveAttributes)
    result_set = []
    while 1:
        result_type, result_data = l.result(ldap_result_id, 0)
        if (result_data == []):
            break
    else:
        ## here you don't have to append to a list
        ## you could do whatever you want with the individual entry
        ## The appending to list is just for illustration.
        if result_type == ldap.RES_SEARCH_ENTRY:
            result_set.append(result_data)
            print result_set
except ldap.LDAPError, e:
    print e
