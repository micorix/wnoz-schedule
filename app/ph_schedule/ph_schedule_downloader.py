import os.path

import requests
import bs4

PH_SCHEDULE_PAGE_URL = "https://wnoz.wum.edu.pl/pl/zdrowie-publiczne-plan-zajec"
DOMAIN = "https://wnoz.wum.edu.pl"


class PhScheduleDownloader:
    data: list[dict[str, str]]

    def __init__(self):
        self.data = []

    def _extract_table_data(self, dom):
        tables = dom.select("table")
        data = []
        for table in tables:
            semester = table.select_one("caption").text
            semester = "letni" if "letni" in semester.lower() else "zimowy"

            headings = [th.text for th in table.select("th")]

            rows = table.select("tr")
            for row in rows:
                cells = row.select("td")
                if all([not cell.text for cell in cells]):
                    continue
                data.append(
                    {
                        "Semestr": semester,
                        **{headings[i]: cell.text for i, cell in enumerate(cells)},
                    }
                )
                link_element = row.select_one("a")
                if link_element:
                    data[-1]["url"] = f"{DOMAIN}{link_element['href']}"
        return data

    def scrape(self):
        response = requests.get(PH_SCHEDULE_PAGE_URL)
        response.raise_for_status()
        dom = bs4.BeautifulSoup(response.text, "html.parser")
        self.data = self._extract_table_data(dom)

    def download(self, filter_func=None, download_dir="./"):
        data = self.data
        if filter_func:
            data = [row for row in self.data if filter_func(row)]

        filenames = []
        for row in data:
            if not row.get("url"):
                continue
            response = requests.get(row["url"])
            file_name = row["url"].split("/")[-1]
            response.raise_for_status()
            full_path = os.path.join(download_dir, file_name)
            with open(full_path, "wb") as f:
                f.write(response.content)
            filenames.append(full_path)
        return filenames
