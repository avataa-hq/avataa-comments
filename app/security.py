from fastapi import HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.requests import Request  # noqa
import requests
from settings import settings
import jwt
from time import sleep
from requests.exceptions import ConnectionError


class OAuth2AuthorizationCodeBearerCustom(OAuth2AuthorizationCodeBearer):
    def __init__(
        self,
        keycloak_public_url: str,
        authorization_url: str,
        token_url: str,
        refresh_url: str | None = None,
        scheme_name: str | None = None,
        scopes: dict[str, str] | None = None,
        description: str | None = None,
        auto_error: bool = True,
    ):
        super(OAuth2AuthorizationCodeBearerCustom, self).__init__(
            authorizationUrl=authorization_url,
            tokenUrl=token_url,
            refreshUrl=refresh_url,
            scheme_name=scheme_name,
            scopes=scopes,
            description=description,
            auto_error=auto_error,
        )
        self.keycloak_public_url = keycloak_public_url
        self._public_key = None
        self._options = {
            "verify_signature": True,
            "verify_aud": False,
            "verify_exp": True,
        }

    def _get_public_key(self):
        connect_attempts = 5
        attempt = 0
        while attempt < connect_attempts:
            try:
                res = requests.get(self.keycloak_public_url, timeout=5)
            except ConnectionError:
                sleep(1)
                attempt += 1
            else:
                if res.status_code == 200:
                    break
                else:
                    sleep(1)
                    attempt += 1
                    continue
        else:
            raise HTTPException(
                status_code=503, detail="Token verification service unavailable"
            )

        public_key = (
            "-----BEGIN PUBLIC KEY-----\n"
            + res.json()["public_key"]
            + "\n-----END PUBLIC KEY-----"
        )
        return public_key

    async def __call__(self, request: Request) -> dict | None:
        token = await super(OAuth2AuthorizationCodeBearerCustom, self).__call__(
            request
        )

        if self._public_key is None:
            self._public_key = self._get_public_key()

        user_info = await self.decode_token(token)
        return {"user_info": user_info, "credentials": token}

    async def decode_token(self, token: str):
        try:
            decoded_token = jwt.decode(
                token,
                self._public_key,
                algorithms=["RS256"],
                options=self._options,
            )
        except jwt.MissingRequiredClaimError as e:
            print(e)
            raise HTTPException(status_code=403, detail=str(e))
        except jwt.ExpiredSignatureError as e:
            print(e)
            raise HTTPException(status_code=403, detail=str(e))
        except jwt.PyJWTError as e:
            print(e)
            raise HTTPException(status_code=403, detail=str(e))
        return decoded_token


oauth2_scheme = OAuth2AuthorizationCodeBearerCustom(
    keycloak_public_url=settings.KEYCLOAK_PUBLIC_KEY_URL,
    token_url=settings.KEYCLOAK_TOKEN_URL,
    authorization_url=settings.KEYCLOAK_AUTHORIZATION_URL,
)
