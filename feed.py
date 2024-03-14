#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   feed.py
@Time    :   2024/03/14 20:35:35
@Author  :   Duy Nam Nguyen
@Version :   1.0
@Contact :   nam.nd.00@gmail.com
@Desc    :   None
"""

import yaml
import xml.etree.ElementTree as xml_tree

with open("feed.yaml", "r") as file:
    yaml_data = yaml.load(file, Loader=yaml.FullLoader)

    rss_element = xml_tree.Element(
        "rss",
        {
            "version": "2.0",
            "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
            "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
        },
    )

channel_level = xml_tree.SubElement(rss_element, "channel")

link_prefix = yaml_data["link"]

xml_tree.SubElement(channel_level, "title").text = yaml_data["title"]
xml_tree.SubElement(channel_level, "format").text = yaml_data["format"]
xml_tree.SubElement(channel_level, "subtitle").text = yaml_data["subtitle"]
xml_tree.SubElement(channel_level, "itunes:author").text = yaml_data["author"]
xml_tree.SubElement(channel_level, "description").text = yaml_data["description"]
xml_tree.SubElement(
    channel_level, "itunes:image", {"href": link_prefix + yaml_data["image"]}
).text = yaml_data["image"]
xml_tree.SubElement(channel_level, "language").text = yaml_data["language"]
xml_tree.SubElement(channel_level, "link").text = link_prefix
xml_tree.SubElement(
    channel_level, "itunes:category", {"text": link_prefix + yaml_data["category"]}
).text = yaml_data["category"]

for item in yaml_data["item"]:
    item_level = xml_tree.SubElement(channel_level, "item")
    xml_tree.SubElement(item_level, "title").text = item["title"]
    xml_tree.SubElement(item_level, "itunes:author").text = yaml_data["author"]
    xml_tree.SubElement(item_level, "description").text = item["description"]
    xml_tree.SubElement(item_level, "itunes:duration").text = item["duration"]
    xml_tree.SubElement(item_level, "pubDate").text = item["published"]
    xml_tree.SubElement(item_level, "title").text = item["title"]

    enclosure = xml_tree.SubElement(
        item_level,
        "enclosure",
        {
            "url": link_prefix + item["file"],
            "type": "audio/mpeg",
            "length": item["length"],
        },
    )

output_tree = xml_tree.ElementTree(rss_element)
output_tree.write("podcast.xml", encoding="utf-8", xml_declaration=True)
