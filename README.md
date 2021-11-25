# certbot_fg_update
Python Script for signingn LetsEncrypt certificate with certbot, and update them into Fortigate (to be used into the WEB VPN or Load Balancer certificate)

As most of you should know LetsEncrypt certificate are valid for 90 days, and the script is just automatic if the certificate is within the server. On my case, the public facing device is a Fortigate (for Web VPN and also for hosting pages with LB feature)
I was looking for a solution already designed, cause i did not find it i created this simple script myself.

In order to use this script, you need to paste your domains names into "dom" list, and paste fortigate credentials and then add this script to crontab to be executed daily o weekley (in my case: * * * * 1 /home/scripts/ssl_renew/ssl_renew.py )

* Check if certificate needs to be updated, if they are close to the expire (30 days) it will update them
* If the certificates has been renewed, this will create / update the private key and certificate key from the .pem files into fortigate
* After running fortigate part will print the status of the fortigate change.

I hope this helps you,
