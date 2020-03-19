import xml.etree.ElementTree as ET


def pick_article(content_items):
    for ci in content_items:
        media_type = ci.find('MediaType')
        if media_type.get('FormalName') == 'Text':
            article = ci.find("./DataContent/nitf")
            return article


def transformXML(storyname):
    f = open(storyname, 'rt')
    tree = ET.parse(f)
    root = tree.getroot()
    ni = root.find('NewsItem')
    duid = ni.get('Duid')
    multimedia_duid = duid + '.multimedia'
    texts_duid = multimedia_duid + '.texts'
    photo_duid = multimedia_duid + '.photos'
    video_duid = multimedia_duid + '.videos'
    multimedia_container = ni.find('NewsComponent[@Duid="%s"]' % multimedia_duid)
    try:
        texts_container = multimedia_container.findall("./NewsComponent[@Duid='%s']" % texts_duid)[0]
        content_items = texts_container.findall('./NewsComponent/ContentItem')
        article = pick_article(content_items)
    except IndexError:
        article = ET.fromstring("<nitf><body><body.content></body.content></body></nitf>")
    body = article.find('body')
    bc = body.find('body.content')
    try:
        photo_container = multimedia_container.findall("./NewsComponent[@Duid='%s']" % photo_duid)[0]
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
    except IndexError:
        pass
    try:
        video_container = multimedia_container.findall("./NewsComponent[@Duid='%s']" % video_duid)[0]
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
    except IndexError:
        pass
    return ET.tostring(article, encoding='UTF-8', method='xml')
