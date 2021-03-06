#!/usr/bin/python -u
#

from MAPI import *
from MAPI.Util import *
import sys

if len(sys.argv) < 2:
    sys.exit('Usage: %s username' % sys.argv[0])

s = OpenECSession(sys.argv[1], '', 'file:///var/run/zarafa')
st = GetDefaultStore(s)
subtreeid = st.GetProps([PR_IPM_SUBTREE_ENTRYID], 0)[0].Value

openroot = st.OpenEntry(None, None, 0)
table = openroot.GetHierarchyTable(0)
table.SetColumns([PR_DISPLAY_NAME, PR_ENTRYID], 0)

while True:
        rows = table.QueryRows(20, 0) # Get 20 folders under the root

        if len(rows) == 0: # No results, die
                break

        for row in rows: # Run through the array
                if row[0].Value == "IPM_SUBTREE": # Find IPM_SUBTREE
                        eid = row[1].Value # Value of IPM_SUBTREE
                        if subtreeid == eid: # Both match, nothing to fix
                                print 'Result: IPM_SUBTREE_ENTRYID already matches IPM_SUBTREE!'
                                print 'IPM_SUBTREE_ENTRYID: ' + subtreeid.encode('hex') + '\nIPM_SUBTREE: ' + eid.encode('hex')
                        elif len(eid) < 2: # Check to ensure the proper ID is actually given
                                print 'Result: Invalid IPM_SUBTREE entryid found, aborting...'
                        else: # Broken, fix it
                                print 'Result: Setting PR_IPM_SUBTREE_ENTRYID to IPM_SUBTREE'
                                print 'PR_IPM_SUBTREE_ENTRYID current value: ' + subtreeid.encode('hex')
                                st.SetProps([SPropValue(PR_IPM_SUBTREE_ENTRYID, eid)]) # Set the proper ENTRYID
                                print 'PR_IPM_SUBTREE_ENTRYID set to: ' + subtreeid.encode('hex')
