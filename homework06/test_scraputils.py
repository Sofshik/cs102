import io
import os
import typing as tp
import unittest
from unittest.mock import patch

import responses
import scraputils as scrap
from bs4 import BeautifulSoup


class ScrapperTestCase(unittest.TestCase):
    maxDiff = None

    def test_extract_news(self) -> None:
        expected_news = [
            {
                "author": "blasrodri",
                "comments": None,
                "points": "1",
                "title": "Oracle Cloud to Acquire Linux Kernel Technology eBPF",
                "url": "cilium.io",
            },
            {
                "author": "adenozine",
                "comments": None,
                "points": "1",
                "title": "Tell HN: Thanks for the Maturity",
                "url": None,
            },
            {
                "author": "CapitalistCartr",
                "comments": None,
                "points": "2",
                "title": "Poorer and minority older adults are suspicious of the US health care system",
                "url": "theconversation.com",
            },
        ]
        with open(
            f"{os.path.dirname(os.path.realpath(__file__))}/mock_templates/example_response.html"
        ) as f:
            mock_response_text = f.read()
        soup = BeautifulSoup(mock_response_text, "html.parser")
        news = scrap.extract_news(soup)
        self.assertEqual(expected_news, news[:3])

    def test_extract_next_page(self) -> None:
        expected_link = "newest?next=26660430&n=31"
        with open(
            f"{os.path.dirname(os.path.realpath(__file__))}/mock_templates/example_response.html"
        ) as f:
            mock_response_text = f.read()
        soup = BeautifulSoup(mock_response_text, "html.parser")
        next_link = scrap.extract_next_page(soup)
        self.assertEqual(expected_link, next_link)

    @responses.activate  # type: ignore
    def test_get_news(self) -> tp.Any:
        with open(
            f"{os.path.dirname(os.path.realpath(__file__))}/mock_templates/example_response.html"
        ) as f:
            mock_response_text = f.read()
        responses.add(responses.GET, "https://news.ycombinator.com/newest", body=mock_response_text)
        expected_news = [
            {
                "author": "blasrodri",
                "comments": None,
                "points": "1",
                "title": "Oracle Cloud to Acquire Linux Kernel Technology eBPF",
                "url": "cilium.io",
            },
            {
                "author": "adenozine",
                "comments": None,
                "points": "1",
                "title": "Tell HN: Thanks for the Maturity",
                "url": None,
            },
            {
                "author": "CapitalistCartr",
                "comments": None,
                "points": "2",
                "title": "Poorer and minority older adults are suspicious of the US health care system",
                "url": "theconversation.com",
            },
        ]
        with patch("sys.stdout", new=io.StringIO()) as _:  # we do not want any output
            news_list = scrap.get_news("https://news.ycombinator.com/newest", n_pages=1)
        self.assertEqual(expected_news, news_list[:3])
