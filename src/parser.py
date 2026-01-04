import os
from bs4 import BeautifulSoup
import glob

def parse_latest_filing():
    # 다운로드된 파일 찾기 (경로는 라이브러리가 생성한 구조를 따름)
    # sec_data/sec-edgar-filings/AAPL/10-Q/filing-ID/full-submission.txt 형식임
    # 여기서는 편의상 가장 최근에 수정된 파일을 찾음
    
    search_path = "./sec_data/sec-edgar-filings/AAPL/10-Q/*/*.txt"
    list_of_files = glob.glob(search_path)
    
    if not list_of_files:
        print("❌ 파일이 없습니다. 다운로드를 먼저 하세요.")
        return

    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"📖 파싱 대상 파일: {latest_file}")

    with open(latest_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # BeautifulSoup으로 텍스트만 추출
    soup = BeautifulSoup(html_content, 'lxml')
    text_content = soup.get_text(separator='\n\n')

    # 불필요한 공백 제거 및 저장
    clean_text = "\n".join([line.strip() for line in text_content.splitlines() if line.strip()])
    
    output_filename = "apple_latest_10q_clean.txt"
    with open(output_filename, "w", encoding='utf-8') as f:
        f.write(clean_text)
        
    print(f"✨ 변환 완료! 저장된 파일: {output_filename}")
    # 나중에는 이 clean_text를 바로 LLM API로 쏘면 됩니다.

if __name__ == "__main__":
    parse_latest_filing()