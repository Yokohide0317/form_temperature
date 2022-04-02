# form_temperature

## Prep
```
vim app/Dockerfile
email, password, auth_keyの変更
```

## Docker
Docker-composeがインストールされている前提<br>

```
docker-compose build
docker-compose up -d
docker exec form_temperature-app-1 python3 main.py
```

## Edit information.json
```
cp Dockerfile Dockerfile.user
vim Dockerfile.user

url: url
email: Your email
password: Your Password
auth_key: 2段階認証のキー. Office365の右上から、「アカウントを表示」＞「セキュリティ情報」＞「方法の追加」＞認証アプリ＞「別の認証アプリを使用します」＞「画像をスキャンできませんか」
```
