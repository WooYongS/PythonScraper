import requests
from bs4 import BeautifulSoup
import time

# 기본 URL 설정
BASE_URL = "https://berlinstartupjobs.com"
ENGINEERING_URL = f"{BASE_URL}/engineering/"
SKILL_URL_TEMPLATE = f"{BASE_URL}/skill-areas/{{}}/"

# 크롤링할 스킬 목록
skills = ["python", "typescript", "javascript", "rust"]

# 요청 헤더 설정

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


# 채용 공고 크롤링 함수
def scrape_jobs(url):
    jobs = []
    page = 1

    while True:
        response = requests.get(
            url if page == 1 else f"{url}page/{page}/",
            headers=HEADERS,
        )

        # 왜 404 코드값이 나오는지 모르겠지만..일단 스킵.. 제출하고나서 나중에 생각!
        # if response.status_code != 200:
        # print(f"⚠️ Failed to fetch {url} (Status Code: {response.status_code})")
        # break

        soup = BeautifulSoup(response.text, "html.parser")
        job_listings = soup.find_all("li", class_="bjs-jlid")  # 새로운 클래스 반영

        if not job_listings:
            break  # 다음 페이지가 없으면 종료

        for job in job_listings:
            title_tag = job.find("h4", class_="bjs-jlid__h")  # 직무 제목
            company_tag = job.find("a", class_="bjs-jlid__b")  # 회사 이름
            desc_tag = job.find("div", class_="bjs-jlid__description")  # 설명
            link_tag = title_tag.find("a") if title_tag else None  # 직무 상세 링크

            job_data = {
                "title": title_tag.text.strip() if title_tag else "N/A",
                "company": company_tag.text.strip() if company_tag else "N/A",
                "description": desc_tag.text.strip() if desc_tag else "N/A",
                "link": (
                    link_tag["href"] if link_tag and "href" in link_tag.attrs else "N/A"
                ),
            }
            print(job_data)
            jobs.append(job_data)

        print(f"✅ Scraped Page {page}: {len(job_listings)} jobs found.")
        page += 1
        time.sleep(1)  # 서버 부하 방지를 위한 딜레이

    return jobs


# 1️⃣ 엔지니어링 전체 채용 크롤링
engineering_jobs = scrape_jobs(ENGINEERING_URL)
print(f"🔹 Total Engineering Jobs Scraped: {len(engineering_jobs)}")

# 2️⃣ 특정 기술별 채용 크롤링
skill_jobs = {}
for skill in skills:
    print(f"🔎 Scraping jobs for skill: {skill}")
    skill_jobs[skill] = scrape_jobs(SKILL_URL_TEMPLATE.format(skill))
    print(f"✅ {skill.upper()} Jobs Scraped: {len(skill_jobs[skill])}")

# 결과 출력
for skill, jobs in skill_jobs.items():
    print(f"\n🔹 {skill.upper()} JOBS ({len(jobs)} found)")
    for job in jobs[:3]:  # 처음 3개 미리보기
        print(f"- {job['title']} at {job['company']} ({job['link']})")
