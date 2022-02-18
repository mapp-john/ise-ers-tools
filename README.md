# ***Cisco ISE ERS API Tools (Written for Python 3.6+)***

## **USAGE**

```
> python3 ise_ers_tools.py

***********************************************************************************************
*                                                                                             *
*                   Cisco ISE ERS API Tools (Written for Python 3.6+)                         *
*                                                                                             *
***********************************************************************************************
*                                                                                             *
* USER INPUT NEEDED:                                                                          *
*                                                                                             *
*  1. FQDN for ISE server (hostname.domain.com)                                               *
*                                                                                             *
*  2. API Username                                                                            *
*                                                                                             *
*  3. API Password                                                                            *
*                                                                                             *
***********************************************************************************************

Please Enter ISE fqdn: ise.domain.com
Attempting to connect to ise.domain.com on port 9060
Connecton successful to ise.domain.com on port 9060
Please Enter API Username: api
Please Enter Password:
Re-enter Password to Verify:

***********************************************************************************************
*                                                                                             *
* TOOLS AVAILABLE:                                                                            *
*                                                                                             *
*  1. Basic URL GET                                                                           *
*                                                                                             *
*  2. Bulk Delete Internal Users                                                              *
*                                                                                             *
***********************************************************************************************

Please Select Tool:
```

## **TOOLS AVAILABLE**
1. Basic URL GET
2. Delete Internal Users in bulk


_____________________________________________________________________________________________
### **Basic URL GET Script**

USER INPUT NEEDED:
1. URI Path (/ers/config/internaluser)
2. Save output to JSON file


_____________________________________________________________________________________________
### **Bulk Delete Internal Users**

USER INPUT NEEDED:
1. Enter ERS API filter for internal users
  * example: identityGroup.CONTAINS.DELETE_ME

