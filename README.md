# KingCrown

KingCrown is a tool to quickly download, install and configure KingPhisher to a server for phishing. It will automagically generate DKIM keys and SSL certificates.  It also has an option to quickly change the domain if your campaign was burned.

### Requirements

- Python 3 and a few standard libs
  - subprocess
  - argparse
  - time
  - os
  - base64
- Tested on Ubuntu 18

### Use
1. Place all 4 .py files in the same directory and use Python 3 as sudo to run KingCrown.py
2. Follow along with the menus.
  2a. Alternatively you can use command line arguments for automation purposes. Ex. sudo python3 Kingcrown.py -d domainname.com -p 443 -i /opt/KingPhisher

## Disclaimer
Don't do anything illegal with this.
Usage of KingCrown for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, provincial/state and federal laws. Developer assume NO liability and are NOT responsible for any misuse or damage caused by this program.

"Don't be mean; we don't have to be mean, cuz, remember, no matter where you go, there you are." - Buckaroo Banzai

## About me
I am a full time Red Teamer.  Sometimes I release stuff I make if I think people will like it.

You can find me on Twitter: [@bhohenadel](https://twitter.com/bhohenadel)

## Thanks
Thank you to my beautiful wife for putting up with my late nights while I worked on this, and her fantastic support she has always given me.

[@jamcut](https://twitter.com/jamcut) for alpha/beta testing.

### TODO
- add support for running it via command line arguments for automation
- add support for other Linux distros
- add more error handling (there is very little)
