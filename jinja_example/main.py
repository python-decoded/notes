from datetime import datetime


data = {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "image_link": "https://cdn-icons-png.flaticon.com/512/219/219969.png",
    "description": "Full-stack software engineer with a strong background "
                   "in frontend technologies and cloud infrastructure. "
                   "Passionate about building scalable web applications "
                   "and mentoring junior developers.",
    "birth_date": datetime(1992, 5, 17),
    "skills": ["Python", "JavaScript", "React", "AWS", "Docker", "Linux"],
    "background": [
        {
            "company": "Facebook",
            "from": datetime(2019, 10, 1),

            "duties": [
                "Architected and developed core features for the Facebook Marketplace team.",
                "Worked closely with product and UX to deliver customer-centric experiences.",
                "Deployed services using Kubernetes and monitored them with Prometheus + Grafana."
            ]
        },
        {
            "company": "Google",
            "from": datetime(2016, 6, 1),
            "to": datetime(2019, 9, 30),
            "duties": [
                "Led frontend development of internal tools used by over 1,000 employees.",
                "Improved web performance by 40% through code optimization and CDN usage.",
                "Mentored 3 junior engineers through onboarding and code reviews."
            ]
        }
    ]
}


# pip install jinja2
from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)

def duration(from_date, to_date=None) -> str:
    if to_date is None:
        to_date = datetime.now()

    # Calculate the total number of months
    total_months = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month)

    # Adjust if the end day is before the start day
    if to_date.day < from_date.day:
        total_months -= 1

    years = total_months // 12
    months = total_months % 12

    return f"{years}y {months}m"

env.filters["duration"] = duration


template = env.get_template("cv.html")
page = template.render(**data)

with open("CV.html", "wb") as f:
    f.write(page.encode("utf-8"))


# pip install playwright
# playwright install
from playwright.sync_api import sync_playwright


def html_to_pdf(html_content, file_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content)
        page.pdf(path=file_path)
        browser.close()


html_to_pdf(page, "CV.pdf")
