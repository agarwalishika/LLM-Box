
"""
1. list the URLs for infoboxes
2. infoboxTemplateName = extract the "Infobox_<template name>" from the url
3. get the html for the page https://en.wikipedia.org/wiki/Special:WhatLinksHere?target=Template%3A{infoboxTemplateName}&namespace=
using beautiful soup
4. get the list items under the <ul> where id="mw-whatlinkshere-list" using beautiful soup
for 500 / 20 list items: 
    5. articleLink = get the href under the <a> tag
    6. get all the article text under "https://en.wikipedia.org/{articleLink}"
    7. 
"""