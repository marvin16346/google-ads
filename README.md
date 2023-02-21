# Google ADS API

## API 사용 전 
<br/>

### 로그인하여 Refresh token 얻기
<hr/>

```console
python google-ads-python/examples/authentication/generate_user_credentials.py -c="secret-take.json"
```

<br/>


### Refresh token을 주고 Access token 받기
<hr/>

```python
import requests

url = "https://www.googleapis.com/oauth2/v3/token"

payload={
    'grant_type': 'refresh_token',
    'client_id': GOOGLE_CLIENT_ID,
    'client_secret': GOOGLE_CLIENT_SECRET,
    'refresh_token': REFRESH_TOKEN
}
files=[

]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
```

<br/>

## API 구조
[Google Ads API 구조](https://developers.google.com/google-ads/api/docs/concepts/api-structure?hl=ko)

<br/><br/>

## API 사용
<br/>

### Header 공통
<hr/>

```python
headers = {
  'Authorization': 'Bearer ACCESS_TOKEN',
  'developer-token': DEVELOPER_TOKEN,
}
```

<br/>


## 구글 서비스 메소드
### search
<hr/>

pageSize, pageToken을 통해 많은 데이터를 페이지 단위로 받을 때 사용

```
POST /v13/customers/CUSTOMER_ID/googleAds:search HTTP/1.1
Host: googleads.googleapis.com
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN
developer-token: DEVELOPER_TOKEN

{
"pageSize": 10000,
"query": "SELECT ad_group_criterion.keyword.text, ad_group_criterion.status FROM ad_group_criterion WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status = 'ENABLED'",
"pageToken": "CPii5aS87vfFTBAKGJvk36qpLiIWUW5SZk8xa1JPaXJVdXdIR05JUUpxZyoCVjMwADjUBkD___________8B"
}
```

### searchStream
<hr/>

데이터를 한꺼번에 받을 때 사용

```
POST /v13/customers/CUSTOMER_ID/googleAds:searchStream HTTP/1.1
Host: googleads.googleapis.com
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN
developer-token: DEVELOPER_TOKEN

{
    "query": "SELECT ad_group_criterion.keyword.text, ad_group_criterion.status FROM ad_group_criterion WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status = 'ENABLED'"
}
```

### mutate
<hr/>

update, create, delete 시 사용

#### create
```
POST /v13/customers/CUSTOMER_ID/campaigns:mutate HTTP/1.1
Host: googleads.googleapis.com
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN
developer-token: DEVELOPER_TOKEN

{
  "operations": [
    {
    "create": {
        "name": "An example campaign",
        "status": "PAUSED",
        "campaignBudget": "customers/CUSTOMER_ID/campaignBudgets/CAMPAIGN_BUDGET_ID",
        "advertisingChannelType": "SEARCH",
        "networkSettings": {
          "targetGoogleSearch": true,
          "targetSearchNetwork": true,
          "targetContentNetwork": true,
          "targetPartnerSearchNetwork": false
        },
        "target_spend": {}
      }
    }
  ]
}
```
#### update
```
POST /v13/customers/CUSTOMER_ID/campaigns:mutate HTTP/1.1
Host: googleads.googleapis.com
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN
developer-token: DEVELOPER_TOKEN

{
  "operations": [
    {
      "updateMask": "name,status",
      "update": {
        "resourceName": "customers/CUSTOMER_ID/campaigns/CAMPAIGN_ID",
        "name": "My renamed campaign",
        "status": "PAUSED",
      }
    }
  ]
}
```
#### delete
```
POST /v13/customers/CUSTOMER_ID/campaigns:mutate HTTP/1.1
Host: googleads.googleapis.com
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN
developer-token: DEVELOPER_TOKEN

{
  "operations": [
    {
      "remove": "customers/CUSTOMER_ID/campaigns/CAMPAIGN_ID"
    }
  ]
}
```
<br/>


### RPC proto 대응 메소드
<hr/>

listAccessibleCustomers, createCustomerClient 등
proto 파일 확인
<br/>
[참고: google api github](https://github.com/googleapis/googleapis/tree/36f0f69727c7ed65048e587c88000f4358f3ca1d/google/ads/googleads/v13/services)

https://googleads.googleapis.com/v13/customers<mark>:listAccessibleCustomers</mark> 처럼 뒤에 ":"을 붙인 후 메소드 추가


<br/><br/>

## API 예시


### 로그인한 유저의 고객 계정 리스트
<hr/>

```python
import requests

url = "https://googleads.googleapis.com/v13/customers:listAccessibleCustomers"

payload = ""
headers = {
  'Authorization': 'Bearer ACCESS_TOKEN',
  'developer-token': DEVELOPER_TOKEN,
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

<br/>


### 캠페인 변경
<hr/>

```python
import requests
import json

url = "https://googleads.googleapis.com/v13/customers/3963943693/campaigns:mutate"

payload = json.dumps({
  "operations": [
    {
        "updateMask": "name,status",
        "update": {
            "resourceName": "customers/3963943693/campaigns/19705911960",
            "name": "롯데 왓따",
            "status": "PAUSED"
        }
    }
  ]
})
headers = {
  'Authorization': 'Bearer ACCESS_TOKEN',
  'developer-token': DEVELOPER_TOKEN,
  'login-customer-id': MANAGER_ID,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

<br/>


### 캠페인 검색 (보고서)
<hr/>

```python
import requests
import json

url = "https://googleads.googleapis.com/v13/customers/3963943693/googleAds:searchStream"

payload = "{\r\n  \"query\" : \"SELECT campaign.name, campaign.status,\r\n                    metrics.impressions, metrics.clicks, metrics.ctr,\r\n                    metrics.average_cpc, metrics.cost_micros\r\n            FROM campaign\r\n            WHERE segments.date DURING LAST_30_DAYS\"\r\n}"
headers = {
  'Authorization': 'Bearer ACCESS_TOKEN',
  'developer-token': DEVELOPER_TOKEN,
  'login-customer-id': MANAGER_ID,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

<br/>

