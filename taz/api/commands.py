import argparse

from taz.api.models.token import TokenModel

parser = argparse.ArgumentParser()
parser.add_argument('--owner', help='App name')
parser.add_argument('--token', help='Token')


class TokenCommand:

    def __init__(self, owner, token=None):
        self.owner = owner
        self.token_str = token

    def create_token(self):
        token = TokenModel.generate(
            owner=self.owner,
            token=self.token_str
        )

        print('Token: {} was successfully generated'.format(token.token))


if __name__ == '__main__':  # pragma: no cover
    args = parser.parse_args()
    token_command = TokenCommand(owner=args.owner, token=args.token)
    token_command.create_token()
