from bs4 import BeautifulSoup, NavigableString

def get_info_from_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    body_div = soup.find("div", id="page")
    tables = body_div.find_all("table", recursive=False)

    basic_info = tables[0]
    important_td = basic_info.find_all("td")[2]
    text_not_in_tags = [str(item).strip() for item in important_td.contents if isinstance(item, NavigableString) and str(item).strip()]

    term, enrollment, eligible_count, response_count, response_rate = text_not_in_tags

    class_id_container = basic_info.find_all("td")[3]
    class_id = class_id_container.find("a").get_text()
    school = str(class_id_container.find_all("b")[2].next_sibling).lstrip()

    """
    if int(response_count) == 0:
        return None
    """

    data = [["-", [term, class_id, school, enrollment, eligible_count, response_count, response_rate]]]

    # Everything except first table and last table is data we want
    i = 1
    for table in tables[1:-1]:
        try:
            tr = table.find_all("tr", recursive=False)[1]
        except:
            # this table is USELESS
            continue
        inner_table = tr.find("table")
        table_rows = inner_table.find_all("tr", recursive=False)[1:]
        for row in table_rows:
            question = row.find("td").get_text()
            fifth_td = row.find_all("td", recursive=False)[4]
            second_tr = fifth_td.find_all("tr")[1]
            all_tds = second_tr.find_all("td")
            counts = []
            for td in all_tds[1:-1]:
                if td.get_text() == "-":
                    counts.append(0)
                else:
                    counts.append(int(td.get_text()))
            total_ = sum(counts)
            counts.append(total_)
            data.append([question, counts])
        i += 1

    return data