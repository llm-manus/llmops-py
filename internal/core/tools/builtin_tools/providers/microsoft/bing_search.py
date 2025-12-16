#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/4 23:39
#Author  :Emcikem
@File    :google_serper.py
"""
import re
import time
from typing import Any, List, Optional, Type

import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

from internal.lib.helper import add_attribute

class BingSearchArgsSchema(BaseModel):
    """bing API搜索参数描述"""
    query: str = Field(description="需要检索查询的语句。")
    date_range: Optional[str] = Field(
        default="all",
        description="网络搜索的数据日期范围，一小时内:past_hour；一天内：past_day；一周内：past_week；一个月内：past_month；一年内：past_year；全部时间范围：all")

class SearchResultItem(BaseModel):
    """搜索结果条目数据类型"""
    url: str  # 搜索条目URL链接
    title: str  # 搜索条目标题
    snippet: str = ""  # 搜索条目摘要信息

class SearchResults(BaseModel):
    """搜索结果数据模型"""
    query: str  # 查询query
    date_range: Optional[str] = None  # 日期筛选范围
    total_results: int = 0  # 搜索结果条数
    results: List[SearchResultItem] = Field(default_factory=list)  # 搜索结果

class BingSearchTool(BaseTool):
    """根据关键词查询网络数据"""
    name: str = "bing_search"
    description: str = "当你想要去搜索网络上的数据时可以使用这个工具"
    args_schema: Type[BaseModel] = BingSearchArgsSchema

    def __init__(self):
        """构造函数，初始化bing搜索引擎的相关信息"""
        super().__init__()
        self._base_url = "https://www.bing.com/search"
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        self._cookies = httpx.Cookies()

    def _run(self, *args: Any, **kwargs: Any) -> List[str]:
        """根据传递的query+date_range调用bing搜索获取搜索内容"""
        query = kwargs.get("query")
        date_range = kwargs.get("date_range")

        # 1.构建请求参数
        params = {"q": query}

        # 2.判断date_range是否存在并提取真实数据
        if date_range and date_range != "all":
            # 3.获取当前日期距离1970-01-01的天数
            days_since_epoch = int(time.time() / (24 * 60 * 60))

            # 4.创建日期检索数据类型映射
            date_mapping = {
                "past_hour": "ex1%3a\"ez1\"",
                "past_day": "ex1%33a\"ez1\"",
                "past_week": "ex1%3a\"ez2\"",
                "past_month": "ex1%3a\"ez3\"",
                "past_year": f"ex1%3a\"ez5_{days_since_epoch - 365}_{days_since_epoch}"
            }

            # 5.判断是否传递了date_range并且在date_mapping中可以找到
            if date_range in date_mapping:
                params["filters"] = date_mapping[date_range]

        try:
            # 6.使用httpx创建一个异步客户端上下文
            with httpx.Client(
                    headers=self._headers,
                    cookies=self._cookies,
                    timeout=60,
                    follow_redirects=True,
            ) as client:
                # 7.调用客户端发起请求
                response = client.get(self._base_url, params=params)
                response.raise_for_status()

                # 8.更新cookie信息
                self._cookies.update(response.cookies)

                # 9.使用bs4解析html内容
                soup = BeautifulSoup(response.text, "html.parser")

                # 10.定义搜索结果并解析li.b_algo对应的dom元素
                search_results = []
                result_items = soup.find_all("li", class_="b_algo")

                # 11.循环遍历所有匹配的元素
                for item in result_items:
                    try:
                        # 12.定义变量存储标题+url链接
                        title, url = ("", "")
                        title_tag = item.find("h2")
                        if title_tag:
                            a_tag = title_tag.find("a")
                            if a_tag:
                                title = a_tag.get_text(strip=True)
                                url = a_tag.get("href", "")

                        # 14.判断标题是否存在，如果不存在则提取该dom下a标签的href+text作为标题和链接
                        if not title:
                            a_tag = item.find_all("a")
                            for a_tag in a_tag:
                                # 15.提取标签中的文本并判断长度是否大于10
                                text = a_tag.get_text(strip=True)
                                if len(text) > 10 and not text.startswith("http"):
                                    title = text
                                    url = a_tag.get("href", "")
                                    break

                        # 16.如果用两种方式还是没有标题
                        if not title:
                            continue

                        # 17.提取检索条目的摘要信息
                        snippet = ""
                        snippet_items = item.find_all(
                            ["p", "div"],
                            class_= re.compile(r"b_lineclamp|b_descript|b_caption"),
                        )
                        if snippet_items:
                            snippet = snippet_items[0].get_text(strip=True)

                        # 18.如果这个情况还找不到摘要则查询所有的p标签，同时获取文本内容，并判断内容长度是否大于20
                        if not snippet:
                            p_tags = item.find_all("p")
                            for p in p_tags:
                                text = p.get_text(strip=True)
                                if len(text) > 20:
                                    snippet = text
                                    break

                        # 19.如果还找不到摘要信息，可以提起元素下的所有文本，并使用常记的分割符进行分割，例如: .!。\n?等等
                        if not snippet:
                            all_text = item.get_text(strip=True)

                            # 20.将所有文本按常记的句子结尾标识进行拆分
                            sentences = re.split(r"[.!?\n。！]]", all_text)
                            for sentence in sentences:
                                clean_sentence = sentence.strip()
                                if len(clean_sentence) > 20 and clean_sentence != title:
                                    snippet = clean_sentence
                                    break

                        # 21.补全相对路径的url链接或者是缺失的协议
                        if url and not url.startswith("http"):
                            if url.startswith("//"):
                                url = "https:" + url
                            elif url.startswith("/"):
                                url = "https://www.bing.com" + url

                        # 22.如果标题和链接都存在则添加数据
                        search_results.append(SearchResultItem(
                            url=url,
                            title=title,
                            snippet=snippet,
                        ))
                    except Exception as e:
                        # 单挑搜索信息出错则记录日志并跳过该条数据
                        # logger.warning(f"Bing搜索结果解析失败: {str(e)}")
                        continue
                # 30.以及有对应结果了则直接返回ToolResult
                return [result.model_dump() for result in search_results]
        except Exception as e:
            # 31.记录下异常信息
            # logger.error(f"Bing搜索出错: {str(e)}")
            return []


@add_attribute("args_schema", BingSearchArgsSchema)
def bing_search(**kwargs) -> BaseTool:
    """bing搜索"""
    return BingSearchTool()