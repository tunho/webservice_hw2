# MySQL 수동 설치 가이드 (Ubuntu 24.04)

현재 환경에 Docker가 없으므로 서버에 직접 MySQL을 설치해야 합니다.

## 1. MySQL 서버 설치

터미널에서 다음 명령어를 실행하세요:

```bash
# 패키지 목록 업데이트
sudo apt update

# MySQL 서버 설치
sudo apt install -y mysql-server

# MySQL 서비스 시작 및 자동 실행 설정
sudo systemctl start mysql
sudo systemctl enable mysql
```

## 2. 데이터베이스 및 사용자 설정

루트 권한으로 MySQL 쉘에 접속합니다:

```bash
sudo mysql
```

MySQL 쉘 내부에서 다음 SQL 명령어를 실행하세요:

```sql
-- 1. 데이터베이스 생성
CREATE DATABASE bookstore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 사용자 생성 ('password' 부분은 원하는 비밀번호로 변경하세요)
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';

-- 3. 권한 부여
GRANT ALL PRIVILEGES ON bookstore.* TO 'user'@'localhost';

-- 4. 변경 사항 적용
FLUSH PRIVILEGES;

-- 5. 종료
EXIT;
```

## 3. 프로젝트 설정 업데이트

`.env` 파일을 수정하여 새로운 MySQL 데이터베이스에 연결합니다:

```bash
# .env 파일 열기
nano .env
```

데이터베이스 설정을 다음과 같이 변경하세요:

```properties
# SQLite 비활성화 (주석 처리)
# SQLALCHEMY_DATABASE_URI=sqlite:///./sql_app.db

# MySQL 활성화
DB_HOST=localhost
DB_PORT=3306
DB_USER=user
DB_PASSWORD=password  # 2단계에서 설정한 비밀번호
DB_NAME=bookstore
```

## 4. 연결 확인

시드 스크립트를 실행하여 연결을 확인하고 초기 데이터를 생성합니다:

```bash
PYTHONPATH=src python src/app/db/seed.py
```

성공 시 "Database seeded successfully!" 메시지가 표시됩니다.
