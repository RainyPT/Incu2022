#Meraki and DNAC API Homework

##OBTAIN LIST OF CLIENTS WITH DNA CENTER
--------------------------------------
**Required Headers | Value**:
Accept | application/json
Content-Type | application/json

1º Get Token:
HTTP Method: POST
URI: https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token
**Requires basic auth(Username: devnetuser ; Password: Cisco123!)**

2º Ask for client health list:
HTTP Method: GET
URI: https://sandboxdnac.cisco.com/dna/intent/api/v1/client-health
**Requires header x-auth-token and its value is the token received in the first step**.

==================================================================================

##OBTAIN LIST OF CLIENTS WITH MERAKI
----------------------------------
**Required Headers | Value**:
Accept | application/json
Content-Type | application/json
X-Cisco-Meraki-API-Key | 6bec40cf957de430a6f1f2baa056b99a4fac9ea0

1º Get Organization ID
HTTP Method: GET
URL: https://api.meraki.com/api/v1/organizations

2º Choose an Organization.

3º Get Organization networks via its ID (ex: 681155)
HTTP Method: GET
URL: https://api.meraki.com/api/v1/organizations/681155/networks

4º Choose a network from that organization.

5º Get Network clients via its Network ID(ex: L_566327653141843049)
HTTP Method: GET
URL: https://api.meraki.com/api/v1/networks/L_566327653141843049/clients