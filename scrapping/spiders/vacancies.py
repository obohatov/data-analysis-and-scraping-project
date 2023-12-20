import scrapy
from scrapy.http import Response
from typing import Generator

from scrapping.config import TECHNOLOGIES


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]

    def parse(self, response: Response, **kwargs) -> Generator[scrapy.Request, None, None]:
        for vacancy in response.css(".job-list-item"):
            vacancy_detail_url = vacancy.css(".job-list-item__link::attr(href)").get()

            yield response.follow(vacancy_detail_url, callback=self._parse_vacancy)

        next_page = response.css('li.page-item:last-child a.page-link::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def _parse_vacancy(self, response: Response) -> Generator[dict, None, None]:
        experience_years = self.get_experience_years(response)
        work_type, company_type = self.get_additional_info(response)

        yield {
            "title": response.css("h1::text").get().strip(),
            "stack": VacanciesSpider._vacancy_stack(response),
            "company": response.css(".job-details--title::text").get().strip(),
            "salary": response.css(".public-salary-item::text").get().strip(),
            "english_level": response.xpath('//div[contains(text(), "English:")]/text()').get(),
            "experience_years": experience_years,
            "work_type": work_type,
            "company_type": company_type,
            "applications": response.css("p.text-muted").extract_first().split()[-3],
            "url": response.url
        }

    @staticmethod
    def _vacancy_stack(response: Response) -> list:
        current_vacancy_stack = []

        for tech in TECHNOLOGIES:
            if tech.lower() in response.css(".mb-4").get().lower():
                current_vacancy_stack.append(tech)

        return current_vacancy_stack

    @staticmethod
    def get_additional_info(response: Response):
        work_type, company_type, test_available = None, None, None
        items = response.css("li.job-additional-info--item")
        for item in items:
            icon_class = item.css("span::attr(class)").get()
            text = item.css("div.job-additional-info--item-text::text").get()

            if "bi bi-building" in icon_class:
                work_type = text.strip() if text else None
            elif "bi bi-basket3-fill" in icon_class:
                company_type = text.strip() if text else None

        return work_type, company_type

    @staticmethod
    def get_experience_years(response: Response) -> int:
        exp_text = response.css(".job-additional-info--body li:last-child div::text").get()
        if "No experience" in exp_text:
            experience_years = 0
        else:
            experience_years = int(exp_text.split()[0].strip().replace("No experience", "0"))

        return experience_years
