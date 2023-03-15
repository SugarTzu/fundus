import datetime
from typing import List, Optional

from src.parser.html_parser import ArticleBody, BaseParser, register_attribute
from src.parser.html_parser.utility import (
    extract_article_body_with_selector,
    generic_author_parsing,
    generic_date_parsing,
    generic_topic_parsing,
)


class BerlinerZeitungParser(BaseParser):
    @register_attribute
    def body(self) -> ArticleBody:
        return extract_article_body_with_selector(
            self.precomputed.doc,
            summary_selector="div[data-testid=article-header] > p",
            subheadline_selector="div[id=articleBody] > p",
            paragraph_selector="div[id=articleBody] > h2",
        )

    @register_attribute
    def title(self) -> Optional[str]:
        return self.precomputed.meta.get("og:title")

    @register_attribute
    def authors(self) -> List[str]:
        return generic_author_parsing(self.precomputed.meta.get("author"))

    @register_attribute
    def publishing_date(self) -> Optional[datetime.datetime]:
        return generic_date_parsing(self.precomputed.ld.bf_search("datePublished"))

    @register_attribute
    def topics(self) -> Optional[List[str]]:
        return generic_topic_parsing(self.precomputed.ld.bf_search("keywords"))