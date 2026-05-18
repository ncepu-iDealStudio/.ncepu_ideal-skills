"""JWT placeholder utilities (enabled only in secure profile)."""


class JwtToken:
    @staticmethod
    def parse_token(token, secret_key):
        # TODO: replace with real JWT verification logic when secure profile is enabled.
        return True, {"token": token}
