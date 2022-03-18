#Meraki and DNAC API Homework

##OBTAIN LIST OF CLIENTS WITH DNA CENTER
--------------------------------------<br/>
**Required Headers | Value**:<br/>
Accept | application/json<br/>
Content-Type | application/json<br/>

1º Get Token:<br/>
HTTP Method: POST<br/>
URI: https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token<br/>
**Requires basic auth(Username: devnetuser ; Password: Cisco123!)**<br/>

2º Ask for client health list:<br/>
HTTP Method: GET<br/>
URI: https://sandboxdnac.cisco.com/dna/intent/api/v1/client-health<br/>
**Requires header x-auth-token and its value is the token received in the first step**.<br/>

==================================================================================<br/>

##OBTAIN LIST OF CLIENTS WITH MERAKI<br/>
----------------------------------<br/>
**Required Headers | Value**:<br/>
Accept | application/json<br/>
Content-Type | application/json<br/>
X-Cisco-Meraki-API-Key | 6bec40cf957de430a6f1f2baa056b99a4fac9ea0<br/>

1º Get Organization ID<br/>
HTTP Method: GET<br/>
URL: https://api.meraki.com/api/v1/organizations<br/>

2º Choose an Organization.<br/>

3º Get Organization networks via its ID (ex: 681155)<br/>
HTTP Method: GET<br/>
URL: https://api.meraki.com/api/v1/organizations/681155/networks<br/>

4º Choose a network from that organization.<br/>

5º Get Network clients via its Network ID(ex: L_566327653141843049)<br/>
HTTP Method: GET<br/>
URL: https://api.meraki.com/api/v1/networks/L_566327653141843049/clients<br/>