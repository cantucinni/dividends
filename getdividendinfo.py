#
# get dividend info by cantucinni no rights reserved 2018
#
# this uses a modified api from https://github.com/Jamonek/Robinhood/
#

import Robinhood
import json
import base64
import os

def DoMyStuff():

    #login to rh
    configfile = 'config.json'

    if not os.path.exists(configfile):
        print("Make sure that config.json exists.")
        return

    data = json.load(open('config.json'))

    if 'Sites' not in data or 'Robinhood' not in data['Sites'] or 'u' not in data['Sites']['Robinhood'] or 'p' not in data['Sites']['Robinhood']:
        print("Please make sure u and p are in config.json")
        return

    u = data['Sites']['Robinhood']['u']
    p = data['Sites']['Robinhood']['p']

    if 'base64' == data['Sites']['Robinhood']['dec']:
        u = base64.b64decode(u)
        p = base64.b64decode(p)

    rhapi = Robinhood.Robinhood()

    #print("Logging in using [{0},{1}]".format(u,p))

    do = open("dividends.csv", 'w')

    if False == rhapi.login(username=u, password=p):
        print("Login failed.")
        return

    div = rhapi.dividends()

    open('dividends.json', 'w').write(json.dumps(div))

    data = "{:>15}\t{:>15}\t{:>15}\t{:>15}\t{:>15}".format('Symbol', 'Position', 'Rate', 'Amount', 'Payable Date')
    print(data)
    do.write(data + "\n")


    if 'results' in div:
        for d in div['results']:
            if 'instrument' in d:
                ret = rhapi.get_url(d['instrument'])
                #get dividend
                if 'symbol' in ret and 'rate' in d and 'amount' in d and 'paid_at' in d and 'position' in d:
                    data = "{:>15}\t{:>15.4f}\t{:>15.4f}\t{:>15.4f}\t{:>15}".format(ret['symbol'], float(d['position']), float(d['rate']), float(d['amount']), d['payable_date'])
                    print(data)
                    #write divident to csv   
                    do.write(data + "\n")
    do.close()
    print("Written stuff to dividends.csv")

    pass

if __name__ == '__main__':
    DoMyStuff()