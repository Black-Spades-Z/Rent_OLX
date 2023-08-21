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
    json: bool = False,
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

    parser = bs(xml, 'lxml-xml')
    counter = 0


    channelTitle = parser.select_one("title").string.extract()
    channelLanguage = parser.select_one("language").string.extract()
    channelLink = parser.select_one("link").string.extract()
    channelDescription = parser.select_one("description").string.extract()
    items = parser.find_all("item")


    #For JSON output, more code, but better Result

    if json:

        items_list = list()

        #Before creating Dictionary for JSON, we should collect all item details

        for item in items:
            itemTitle = item.select_one("item> title").string.extract()
            itemLink = item.select_one("item> link").string.extract()
            itemPubDate = item.select_one("item > pubDate").string.extract()
            itemDescription = item.select_one("item> description").string.extract().strip()

            temp_dictionary = {
                "title": itemTitle,
                "pubDate": itemPubDate,
                "link": itemLink,
                "description": itemDescription,
            }
            items_list.append(temp_dictionary)

            #For limit parameter

            counter += 1
            if counter == limit:
                break

        # Creating dictionary for JSON converting

        json_dictionary = {
            "title": channelTitle,
            "language": channelLanguage,
            "link": channelLink,
            "description": channelDescription,
            "items": [items_list]
        }



        # Converting dictionary to JSON

        json_result = js.dumps(json_dictionary, indent=2, ensure_ascii=False)
        return list(str(json_result).split(", "))



    #If we do not need JSON format, we should create list to return it later

    result = list([f"Feed: {channelTitle}",
                   f"Language: {channelLanguage}",
                   f"Link: {channelLink}",
                   f"Description: {channelDescription}",
                   " ", " "])

    #Collecting item details

    for item in items:

        itemTitle = item.select_one("item> title").string.extract()
        itemLink = item.select_one("item> link").string.extract()
        itemPubDate = item.select_one("item > pubDate").string.extract()

        itemDescription = item.select_one("item> description").string.extract().strip()



        itemsList = list([f"Title: {itemTitle}",
                       f"Link: {itemLink}",
                       f"Published: {itemPubDate}",
                       " ",
                       f"{itemDescription}", " ", " "])
        counter += 1
        result.extend(itemsList)
        itemsList.clear()
        if counter == limit:
            break





    return result


def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
    """

    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )

    args = parser.parse_args(argv)
    xml = requests.get(args.source).text
    try:
        print("\n".join(rss_parser(xml, args.limit, args.json)))

        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
