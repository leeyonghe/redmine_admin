from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import RedmineUser
import hashlib

class RedmineAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # RedmineUser 테이블에서 사용자 조회
            user = RedmineUser.objects.get(login=username, status=1)
            
            # Redmine의 비밀번호 해시 방식 (SHA1(salt + SHA1(password)) 또는 단순 SHA1)
            if user.salt:
                # salt가 있는 경우: SHA1(salt + SHA1(password))
                password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
                hashed_password = hashlib.sha1((user.salt + password_hash).encode('utf-8')).hexdigest()
            else:
                # salt가 없는 경우: SHA1(password)
                hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
            
            if user.hashed_password == hashed_password:
                # RedmineUser를 Django User로 변환하여 반환
                django_user, created = User.objects.get_or_create(
                    username=user.login,
                    defaults={
                        'first_name': user.firstname,
                        'last_name': user.lastname,
                        'email': f"{user.login}@example.com",
                        'is_staff': user.admin,
                        'is_superuser': user.admin,
                    }
                )
                return django_user
        except RedmineUser.DoesNotExist:
            return None
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None 