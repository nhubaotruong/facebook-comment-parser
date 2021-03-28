from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import urllib
from bs4 import BeautifulSoup
import re
from contextlib import suppress
import dateparser
from deep_translator import GoogleTranslator


@require_http_methods(["GET"])
def test(request):
    return JsonResponse({"status": "success"})


@require_http_methods(["POST"])
def parse_comment(request):
    request_body = dict(urllib.parse.parse_qsl(request.body.decode()))
    if not request_body.get("fbContent"):
        return JsonResponse({"result": []})
    selector = BeautifulSoup(request_body.get("fbContent"), "html.parser")

    comment_list = []
    comment_raws = selector.find_all("div", {"class": "ee"})
    for element in comment_raws:
        comment = dict()
        with suppress(Exception):
            name = element.select_one("div h3 a").get_text(strip=True)
            comment["name"] = name

        with suppress(Exception):
            profile_link = element.select_one("div h3 a").attrs.get("href", "")
            comment["profile_link"] = fb_link(profile_link)

        with suppress(Exception):
            comment_text = element.select_one("div h3 + div").get_text(strip=True)
            comment["comment_text"] = comment_text

        try:
            comment_text_eng = GoogleTranslator(source="auto", target="en").translate(
                comment.get("comment_text", "")
            )
        except Exception:
            comment_text_eng = ""
        comment["comment_text_eng"] = comment_text_eng

        with suppress(Exception):
            comment_img = element.select_one("div h3 + div + div img").attrs.get(
                "src", ""
            )
            comment["comment_img"] = comment_img

        with suppress(Exception):
            comment_time = element.select_one("abbr").get_text(strip=True)
            comment["comment_date"] = dateparser.parse(comment_time).strftime(
                "%d/%m/%Y"
            )

        with suppress(Exception):
            child_node = element.findChildren("div")
            if len(child_node) == 7:
                comment["has_reply"] = True
            else:
                comment["has_reply"] = False

        if comment.get("has_reply", False):
            with suppress(Exception):
                reply_link = element.find_all("a")[-1].attrs.get("href")
                comment["reply_link"] = "https://mbasic.facebook.com" + reply_link

        if (
            comment.get("name")
            and comment.get("profile_link")
            and comment.get("comment_date")
        ):
            comment_list.append(comment)

    return JsonResponse({"result": comment_list})


link_regex = re.compile(r"(.+?)\?")
link_regex2 = re.compile(r"(.+?)&")


def fb_link(st: str) -> str:
    try:
        if "profile.php" in st:
            fblink = "https://facebook.com" + link_regex2.search(st).group(1)
        else:
            fblink = "https://facebook.com" + link_regex.search(st).group(1)
        return fblink
    except Exception:
        return "https://facebook.com"
