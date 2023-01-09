from decimal import Decimal
from enum import Enum
from typing import Optional, List, Any
from http import HTTPStatus
import json

from requests_html import HTMLSession
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup


class GoodParams(BaseModel):
    strain_type: Optional[str]
    thc: Optional[str]
    flavor: Optional[str]
    type: Optional[str]
    effect: Optional[str]
    indor_yield: Optional[str]
    outdor_yield: Optional[str]
    indor_height: Optional[str]
    outdor_height: Optional[str]
    genetics: Optional[str]

class Good(BaseModel):
    name: Optional[str]
    gg_price_gel: Optional[Decimal]
    ava_url: Optional[str]
    gg_url: Optional[str]
    description: Optional[str]
    params: Optional[GoodParams]


URL_PREFIX = "https://growgrow.ge"
def get_soap(url: str) -> Optional[BeautifulSoup]:
    # session = HTMLSession()

    # resp = session.get(url=url)
    # resp.html.render()
    resp = requests.get(url=url)
    return BeautifulSoup(resp.text, "html.parser") if resp.status_code is HTTPStatus.OK.value else None

def get_cards(soap: BeautifulSoup) -> List[Any]:
    result = []
    items = soap.find_all("div", {"class": "product-item"})
    for item in items:
        good = Good()
        a_ = item.find("a")
        good.gg_url = URL_PREFIX + a_["href"]
        
        good.ava_url = "https:" + a_.find("div").find("img")["data-src"].replace("{width}", "200")

        sub_div = item.find("div", {"class": "product-item__info-inner"})
        good.name = sub_div.find("a", {"class": "product-item__title text--strong link"}).text
        good.gg_price_gel = Decimal(sub_div.find("div", {"class": "product-item__price-list price-list"}
            ).find("span").find("span", {"class": "money conversion-bear-money"}).text.split(" ")[0])
        result.append(good)

        # add description $ params
        params = {}
        desc_soap = get_soap(good.gg_url)
        core = desc_soap.find("div", {"class": "product-block-list__item product-block-list__item--description"}
                ).find("div", {"class": "card"}
                )

        try:
            descs = core.find("p").find_all("span")
        except:
            descs = []

        descs = [e.text for e in descs]
        good.description = "".join(descs)

        table = core.find("table")

        def get_attr(text: str):
            try:
                result = table.find(lambda tag:tag.name=="th" and text in tag.text).parent.find("td").text
            except:
                result = ""
            return result

        params["strain_type"] = get_attr("Strain Type")
        params["thc"] = get_attr("THC")
        params["flavor"] = get_attr("Flavor")
        params["type"] = get_attr("Type")
        params["flowering"] = get_attr("Flowering")
        params["effect"] = get_attr("Effect")
        params["indor_yield"] = get_attr("Indoor Yield")
        params["outdor_yield"] = get_attr("Outdoor Yield")
        params["indor_height"] = get_attr("Indoor Height")
        params["outdor_height"] = get_attr("Outdoor Height")
        params["genetics"] = get_attr("Genetics")

        good_params = GoodParams(**params)
        good.params = good_params

    return [r.json() for r in result]

if __name__ == "__main__":
    soap = get_soap(URL_PREFIX + '/collections/seeds')
    goods = get_cards(soap=soap)
    with open("/Users/q0tik/Projects/UB-back-fastapi/result.json", "w+") as file:
        file.write(f'"goods": {goods}')
