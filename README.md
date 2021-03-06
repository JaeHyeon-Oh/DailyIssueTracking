# dailyworks-back
## Slack Social Login + JWT Process
![슬랙 소셜로그인+JWT](https://user-images.githubusercontent.com/72315719/179645779-74ac1be1-5422-4700-88ab-43a78a1c05bf.png)

## Conceptual Modeling
![개념적 모델링](https://user-images.githubusercontent.com/72315719/179645920-543aa933-0690-4341-8017-b1ed047f6e67.png)

## Logical Modeling
![논리적 모델링](https://user-images.githubusercontent.com/72315719/179645943-436538e4-339e-4074-b56c-556049f3ca72.png)

## ITSJWT.settings
### Write code
* SECRET_KEY = [Search Django ](https://djecrety.ir/)
* CORS_ORIGIN_WHITELIST = (FrontendUrl , BackendUrl)
*
<pre>
<code>
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB Name,
        # 사용자 유저 계정 생성 후 입력하기
        'USER': Root,
        # 사용자 비밀번호 생성 후 입력하기
        'PASSWORD': Password,
        'HOST': '127.0.0.1',
        # MySQL default 포트 번호
        'PORT': '3306',
    }
}
</code>
</pre>
*
<pre>
<code>
JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': Algorithm,
    'JWT_ALLOW_REFRESH': True or False,
    'JWT_EXPIRATION_DELTA': Time,
    'JWT_REFRESH_EXPIRATION_DELTA': Time,
}
</code>
</pre>



## Run 
1. pip install -r requirements.txt
2. python manage.py makemigrations
3. python manage.py migrate
4. python manage.py runserver '0.0.0.0:5000'


## After Slack Login ->Setting DB Model 
* Department
* ResponsibleIssue
* Responsibility


