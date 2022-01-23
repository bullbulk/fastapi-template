from typing import Optional

from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm


class PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(
            self,
            grant_type: str = Form(None, regex="password"),
            username: str = Form(...),
            password: str = Form(...),
            fingerprint: str = Form(...),
            scope: str = Form(""),
            client_id: Optional[str] = Form(None),
            client_secret: Optional[str] = Form(None)
    ):
        super().__init__(grant_type, username, password, scope, client_id, client_secret)
        self.fingerprint = fingerprint
