#https://github.com/Black-Spades-Z/Rent_OLX.git


# You shouldn't change  name of function or their arguments,
# but you can change content of the initial functions.
from argparse import ArgumentParser
from typing import List, Optional, Sequence
import requests
from bs4 import BeautifulSoup as bs
import json as js
import re


class UnhandledException(Exception):
    pass


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    metro: bool = False,
) -> List[str]:
    """
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.
        json: If True, format output as JSON.

    Returns:
        List of strings.
        Which then can be printed to stdout or written to file as a separate lines.

    Examples:
       # >>> xml = '<rss><channel><title>Some RSS Channel</title><link>https://some.rss.com</link><description>Some RSS Channel</description></channel></rss>'
       # >>> rss_parser(xml)
        ["Feed: Some RSS Channel",
        "Link: https://some.rss.com"]
      #  >>> print("\\n".join(rss_parser(xmls)))
        Feed: Some RSS Channel
        Link: https://some.rss.com
    """
    # Your code goes here

    html = bs(xml, 'html.parser')

    houses = list()

    PATTERN_LIST = ('qiz', 'qizlarga', 'qizlarni', 'qizga', 'qizga.', 'qizlar',
                    'киз', 'кизларга', 'кизларни', 'кизлар',
                    'девушкам', 'девушке', 'девочек',
                    'TTZ', 'ТТЗ', 'ттз-4',
                    'karasu', 'карасу',
                    'сергили','сергели', 'sergili',
                    'куйлик', 'куйлук', 'посуточно',
                    'шерикликка', 'шерикчилик',
                    'хозяйкой', 'xozyayka', 'xozaykali',
                    'семейным', 'oilaga', 'oila',
                    'дача'




                    )


    list_of_houses = html.find(attrs={"data-testid" : "listing-grid"})
    for elements in list_of_houses.find_all(attrs={"data-cy" : "l-card"}):
        confirm = False
        header =  elements.find('h6').get_text()
        name =  re.split('\s',header)
        for word in name:
            word = word.lower()
            if word in PATTERN_LIST:
                print("Found : ", name)
                confirm = True
                break
        if confirm:
            continue

        house = dict(
            {
                "Name" : header,
                "Price": elements.find('p').get_text(),
                "Link": "https://www.olx.uz" + elements.find("a", href = True)['href'],


             }
        )
        houses.append(house)
        print(house)

    print('\n\n\n Houses\n')
    for ads in houses:
        [print(key, ': ', value) for key, value in ads.items()]




    #
    # channelTitle = parser.select_one("title").string.extract()
    # channelLanguage = parser.select_one("language").string.extract()
    # channelLink = parser.select_one("link").string.extract()
    # channelDescription = parser.select_one("description").string.extract()
    # items = parser.find_all("item")
    #
    #
    # #For JSON output, more code, but better Result
    #
    # if json:
    #
    #     items_list = list()
    #
    #     #Before creating Dictionary for JSON, we should collect all item details
    #
    #     for item in items:
    #         itemTitle = item.select_one("item> title").string.extract()
    #         itemLink = item.select_one("item> link").string.extract()
    #         itemPubDate = item.select_one("item > pubDate").string.extract()
    #         itemDescription = item.select_one("item> description").string.extract().strip()
    #
    #         temp_dictionary = {
    #             "title": itemTitle,
    #             "pubDate": itemPubDate,
    #             "link": itemLink,
    #             "description": itemDescription,
    #         }
    #         items_list.append(temp_dictionary)
    #
    #         #For limit parameter
    #
    #         counter += 1
    #         if counter == limit:
    #             break
    #
    #     # Creating dictionary for JSON converting
    #
    #     json_dictionary = {
    #         "title": channelTitle,
    #         "language": channelLanguage,
    #         "link": channelLink,
    #         "description": channelDescription,
    #         "items": [items_list]
    #     }
    #
    #
    #
    #     # Converting dictionary to JSON
    #
    #     json_result = js.dumps(json_dictionary, indent=2, ensure_ascii=False)
    #     return list(str(json_result).split(", "))
    #
    #
    #
    # #If we do not need JSON format, we should create list to return it later
    #
    # result = list([f"Feed: {channelTitle}",
    #                f"Language: {channelLanguage}",
    #                f"Link: {channelLink}",
    #                f"Description: {channelDescription}",
    #                " ", " "])
    #
    # #Collecting item details
    #
    # for item in items:
    #
    #     itemTitle = item.select_one("item> title").string.extract()
    #     itemLink = item.select_one("item> link").string.extract()
    #     itemPubDate = item.select_one("item > pubDate").string.extract()
    #
    #     itemDescription = item.select_one("item> description").string.extract().strip()
    #
    #
    #
    #     itemsList = list([f"Title: {itemTitle}",
    #                    f"Link: {itemLink}",
    #                    f"Published: {itemPubDate}",
    #                    " ",
    #                    f"{itemDescription}", " ", " "])
    #     counter += 1
    #     result.extend(itemsList)
    #     itemsList.clear()
    #     if counter == limit:
    #         break
    #
    #
    #
    #
    #
    # return result


def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
    """

    parser = ArgumentParser(
        prog="Rent Finder",
        description="Program to sort houses",
    )
    parser.add_argument(
        "-L", "--lowest", help="Lowest price", type=int
    )
    parser.add_argument(
        "-H", "--highest", help="Highest available price", type=int)

    parser.add_argument(
        "-m", "--metro", help="Existence of metro", type=bool)

    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )

    args = parser.parse_args()


    LOWEST = int(args.lowest * 1000000)
    HIGHEST = int(args.highest * 1000000)
    LINK = f"https://www.olx.uz/list/q-Ташкент-Аренда-квартира/?search%5Border%5D=created_at:desc&search%5Bfilter_float_price:from%5D={LOWEST}&search%5Bfilter_float_price:to%5D={HIGHEST}"


    xml = requests.get(LINK).text
    try:
        rss_parser(xml, args.limit, args.metro)
        #print("\n".join(rss_parser(xml, args.limit, args.metro)))
       # print(xml)
        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
