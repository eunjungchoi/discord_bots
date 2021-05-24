import os
import sys
from dc_butler import client

TOKENS = {
    'local': 'DC_TOKEN_LOCAL',
    'test': 'DC_TOKEN_TEST',
    'production': 'DISCORD_TOKEN'
}

if __name__ == '__main__':
    ENV = sys.argv[1]
    TOKEN = os.getenv(TOKENS[ENV])
    client.ENV = ENV
    client.run(TOKEN)
