import xml.etree.ElementTree as ET


def pick_article(content_items):
    for ci in content_items:
        media_type = ci.find('MediaType')
        if media_type.get('FormalName') == 'Text':
            article = ci.find("./DataContent/nitf")
            return article

out = open("testout.xml", "w")
out.write('<?xml version="1.0">')
out.write('<!DOCTYPE nitf PUBLIC "-//IPTC-NAA//DTD NITF 3.1//EN"')
out.write('"http://www.nitf.org/site/nitf-documentation/nitf-3-1.dtd"')
out.close()

with open('data/4193550_71475729.xml', 'rt') as f:
    tree = ET.parse(f)
    root = tree.getroot()
    ni = root.find('NewsItem')
    duid = ni.get('Duid')
    multimedia_container = ni.find('NewsComponent')

    texts_duid = multimedia_container.get('Duid') + '.texts'
    photo_duid = multimedia_container.get('Duid') + '.photos'
    video_duid = multimedia_container.get('Duid') + '.videos'

    texts_container = multimedia_container.findall("./NewsComponent[@Duid='%s']" % texts_duid)[0]
    content_items = texts_container.findall('./NewsComponent/ContentItem')
    article = pick_article(content_items)
    body = article.find('body')
    bc = body.find('body.content')

    photo_container = multimedia_container.findall("./NewsComponent[@Duid='%s']" % photo_duid)[0]
    if photo_container:
        photo_components = photo_container.findall('NewsComponent')
        for photo in photo_components:
            loc = photo.findall("./NewsComponent/ContentItem")[0]
            url = loc.get('Href')
            media = ET.SubElement(bc, 'media')
            media.set('media-type', 'image')
            meta = ET.SubElement(media, "media-metadata")
            meta.set("name", "id")
            photo_xtern_id = url.split('.')[0]
            meta.set("value", photo_xtern_id)
            src = ET.SubElement(media, "media-reference")
            src.set("source", url)
            text_field = photo.findall("./NewsComponent/ContentItem")[1]
            caption = text_field.findall("./DataContent/nitf/body/body.content/p")[0].text
            copy = ET.SubElement(media, "media-caption")
            copy.text = caption

    video_container = multimedia_container.findall("./NewsComponent[@Duid='%s']" % video_duid)[0]
    if video_container:
        video_components = video_container.findall('NewsComponent')
        for video in video_components:
            ET.dump(video)
            ###get binary video file###
            #video_loc = video.findall(".//*[@FormalName='Video']/..ContentItem")
            video_loc = video.findall("./NewsComponent/ContentItem")[0]
            url = video_loc.get('Href')
            media = ET.SubElement(bc, 'media')
            media.set('media-type', 'video')
            media_details = ET.SubElement(media, 'media-reference')
            mime_type = video_loc.find('MimeType')
            media_details.set('mime-type', mime_type.get('FormalName'))
            media_details.set('source', url)
            ###get poster preview photo###
            #poster_loc = video.find(".//MediaType[@FormalName='Photo']/../ContentItem")
            poster_loc = video.findall("./NewsComponent/ContentItem")[1]
            poster_url = poster_loc.get('Href')
            poster = ET.SubElement(media, 'media-reference')
            poster.set("name", "tncms-view-poster")
            poster.set("source", poster_url)
            ###get copy for title, caption, external id string###
            #text_loc = video.find(".//MediaType[@FormalName='Text']/../ContentItem")
            """text_loc = video.findall("./NewsComponent/ContentItem")[2]
            id_string = text_loc.find("./DataContent/nitf/head/docdata/doc-id").get('id-string')
            title = text_loc.find("./DataContent/nitf/head/title")
            ET.dump(title)
            v_caption = text_loc.find(".//body.content")
            meta = ET.SubElement(media, 'media-metadata')
            meta.set('name', 'id')
            meta.set('value', id_string)
            meta_title = ET.SubElement(media, 'media-metadata')
            meta_title.set('name', 'title')
            meta_title.set('value', title.text)
            media_caption = ET.SubElement(media, 'media-caption')
            media_caption.text = v_caption"""



    out_binary = open("testout.xml", "wb")
    out_binary.write(ET.tostring(article, encoding='UTF-8', method='xml'))
    out_binary.close()