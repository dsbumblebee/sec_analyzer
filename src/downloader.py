import os
from dotenv import load_dotenv
from sec_edgar_downloader import Downloader

load_dotenv()

user_name = os.getenv('SEC_USER_NAME')
user_email = os.getenv('SEC_USER_EMAIL')


def download_apple_filings():
    # 1. 저장할 경로 설정 (현재 폴더 아래 'sec_data')
    base_dir = "./sec_data"
    os.makedirs(base_dir, exist_ok=True)

    # 2. SEC 다운로더 초기화 
    # (반드시 본인 이메일 주소를 넣어야 합니다! 안 그러면 차단당함)
    dl = Downloader(user_name, user_email, base_dir)

    print("📥 애플(AAPL)의 최신 10-Q(분기보고서) 다운로드 시작...")
    
    # 3. 애플(AAPL)의 최신 10-Q 보고서 1개만 다운로드
    # (10-K는 연간보고서, 8-K는 수시공시)
    dl.get("10-Q", "AAPL", limit=1)
    
    print("✅ 다운로드 완료!")

if __name__ == "__main__":
    download_apple_filings()