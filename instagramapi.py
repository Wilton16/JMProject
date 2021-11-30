import requests

instagram_app_id = '611600239990087'
instagram_secret_id = 'd79ad0b4ff77e65c2d3e74d9abcdd92a'

baseurl = 'api.instagram.com'

https://api.instagram.com/oauth/authorize
  ?client_id=instagram_app_id
  &redirect_uri={redirect-uri}
  &scope={scope}
  &response_type=code
  &state={state}     