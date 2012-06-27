#!/usr/bin/env python
# encoding: utf-8

"""because I was too lazy to copy every url from their api explorer, and replace the secrets, etc. will work on it later"""

json_photos = { "photos": { "page": 1, "pages": 9, "perpage": 100, "total": "853",
                "photo": [
                  { "id": "6110599952", "owner": "91259891@N00", "secret": "xxxxxx", "server": "6087", "farm": 7, "title": "lizanie cukierka przez szybę", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
                  { "id": "6110054827", "owner": "91259891@N00", "secret": "xxxxxx", "server": "6201", "farm": 7, "title": "święto kawalerii", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
                  { "id": "6110054503", "owner": "91259891@N00", "secret": "xxxxxx", "server": "6199", "farm": 7, "title": "zdziwiony kotek", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
                  { "id": "6110045859", "owner": "91259891@N00", "secret": "xxxxxx", "server": "6182", "farm": 7, "title": "kolorki", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
                  { "id": "6110589742", "owner": "91259891@N00", "secret": "xxxxxx", "server": "6190", "farm": 7, "title": "most", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
                  { "id": "6110589446", "owner": "91259891@N00", "secret": "xxxxxx", "server": "6075", "farm": 7, "title": "owca", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
                  ] }, "stat": "ok" }
json_info = { "photo": { "id": "6110054503", "secret": "c7458a7129", "server": "6199", "farm": 7, "dateuploaded": "1315090210", "isfavorite": 0, "license": 0, "safety_level": 0, "rotation": 0, "originalsecret": "d26fce212e", "originalformat": "jpg",
                        "owner": { "nsid": "91259891@N00", "username": "zalew", "realname": "jakub zalewski", "location": "", "iconserver": "2519", "iconfarm": 3 },
                        "title": { "_content": "zdziwiony kotek" },
                        "description": { "_content": "" },
                        "visibility": { "ispublic": 1, "isfriend": 0, "isfamily": 0 },
                        "dates": { "posted": "1315090210", "taken": "2011-09-03 18:43:47", "takengranularity": 0, "lastupdate": "1315090211" },
                        "permissions": { "permcomment": 3, "permaddmeta": 2 }, "views": 8,
                        "editability": { "cancomment": 1, "canaddmeta": 1 },
                        "publiceditability": { "cancomment": 1, "canaddmeta": 0 },
                        "usage": { "candownload": 1, "canblog": 1, "canprint": 1, "canshare": 1 },
                        "comments": { "_content": 0 },
                        "notes": {
                          "note": [

                          ] },
                        "people": { "haspeople": 0 },
                        "tags": {
                          "tag": [
                                { "id": "2306806-5707225239-207992", "author": "91259891@N00", "raw": "łódź", "_content": "łódź", "machine_tag": 0 },
                                { "id": "2306806-5707225239-170037", "author": "91259891@N00", "raw": "lodz", "_content": "lodz", "machine_tag": 0 },
                                { "id": "2306806-5707225239-8302", "author": "91259891@N00", "raw": "poland", "_content": "poland", "machine_tag": 0 },
                                { "id": "2306806-5707225239-8303", "author": "91259891@N00", "raw": "polska", "_content": "polska", "machine_tag": 0 },
                                { "id": "2306806-5707225239-9616057", "author": "91259891@N00", "raw": "bałuty", "_content": "bałuty", "machine_tag": 0 }
                              ] },
                        "urls": {
                          "url": [
                            { "type": "photopage", "_content": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/" }
                          ] }, "media": "photo" }, "stat": "ok" }



json_photos_extras = { "photos": { "page": 1, "pages": 9, "perpage": 100, "total": "859",
    "photo": [
      { "id": "6110054503", "owner": "91259891@N00", "secret": "c7458a7129", "server": "6199", "farm": 7, "title": "IMG_0996", "ispublic": 1, "isfriend": 0, "isfamily": 0,
        "description": { "_content": "photo for testing some api functions" }, "license": 0, "dateupload": "1337237200", "datetaken": "2012-05-17 08:45:10", "datetakengranularity": 0, "ownername": "zalew", "iconserver": "2519", "iconfarm": 3, "originalsecret": "d26fce212e", "originalformat": "jpg", "lastupdate": "1337237201", "latitude": 0, "longitude": 0, "accuracy": 0, "context": 0, "tags": "test", "machine_tags": "", "o_width": "1449", "o_height": "802", "views": 3, "media": "photo", "media_status": "ready", "pathalias": "zalew", "url_sq": "http:\/\/farm9.staticflickr.com\/8163\/7213959182_1678922289_s.jpg", "height_sq": 75, "width_sq": 75, "url_t": "http:\/\/farm9.staticflickr.com\/8163\/7213959182_1678922289_t.jpg", "height_t": 55, "width_t": 100, "url_s": "http:\/\/farm9.staticflickr.com\/8163\/7213959182_1678922289_m.jpg", "height_s": "133", "width_s": "240", "url_q": "http:\/\/farm9.staticflickr.com\/8163\/7213959182_1678922289_q.jpg", "height_q": "150", "width_q": "150", "url_m": "http:\/\/farm9.staticflickr.com\/8163\/7213959182_1678922289.jpg", "height_m": "277", "width_m": "500", "url_n": "http:\/\/farm9.staticflickr.com\/8163\/7213959182_1678922289_n.jpg", "height_n": "177", "width_n": "320", "url_z": "http:\/\/farm9.staticflickr.com\/8163\/7213959182_1678922289_z.jpg", "height_z": "354", "width_z": "640", "url_c": "http:\/\/farm9.staticflickr.com\/8163\/7213959182_1678922289_c.jpg", "height_c": "443", "width_c": "800", "url_l": "http:\/\/farm9.staticflickr.com\/8163\/7213959182_1678922289_b.jpg", "height_l": "567", "width_l": "1024", "url_o": "http:\/\/farm9.staticflickr.com\/8163\/7213959182_d19ce857bf_o.jpg", "height_o": "802", "width_o": "1449" },
      { "id": "7213959374", "owner": "91259891@N00", "secret": "ffeff7f17b", "server": "7231", "farm": 8, "title": "IMG_0995", "ispublic": 1, "isfriend": 0, "isfamily": 0,
        "description": { "_content": "photo for testing some api functions" }, "license": 0, "dateupload": "1337237199", "datetaken": "2006-10-15 11:30:25", "datetakengranularity": 0, "ownername": "zalew", "iconserver": "2519", "iconfarm": 3, "originalsecret": "2d2c56417c", "originalformat": "jpg", "lastupdate": "1337237201", "latitude": 0, "longitude": 0, "accuracy": 0, "context": 0, "tags": "test", "machine_tags": "", "o_width": "1600", "o_height": "1200", "views": 2, "media": "photo", "media_status": "ready", "pathalias": "zalew", "url_sq": "http:\/\/farm8.staticflickr.com\/7231\/7213959374_ffeff7f17b_s.jpg", "height_sq": 75, "width_sq": 75, "url_t": "http:\/\/farm8.staticflickr.com\/7231\/7213959374_ffeff7f17b_t.jpg", "height_t": 75, "width_t": 100, "url_s": "http:\/\/farm8.staticflickr.com\/7231\/7213959374_ffeff7f17b_m.jpg", "height_s": "180", "width_s": "240", "url_q": "http:\/\/farm8.staticflickr.com\/7231\/7213959374_ffeff7f17b_q.jpg", "height_q": "150", "width_q": "150", "url_m": "http:\/\/farm8.staticflickr.com\/7231\/7213959374_ffeff7f17b.jpg", "height_m": "375", "width_m": "500", "url_n": "http:\/\/farm8.staticflickr.com\/7231\/7213959374_ffeff7f17b_n.jpg", "height_n": "240", "width_n": "320", "url_z": "http:\/\/farm8.staticflickr.com\/7231\/7213959374_ffeff7f17b_z.jpg", "height_z": "480", "width_z": "640", "url_c": "http:\/\/farm8.staticflickr.com\/7231\/7213959374_ffeff7f17b_c.jpg", "height_c": "600", "width_c": "800", "url_l": "http:\/\/farm8.staticflickr.com\/7231\/7213959374_ffeff7f17b_b.jpg", "height_l": "768", "width_l": "1024", "url_o": "http:\/\/farm8.staticflickr.com\/7231\/7213959374_2d2c56417c_o.jpg", "height_o": "1200", "width_o": "1600" },
      { "id": "7213959622", "owner": "91259891@N00", "secret": "c354340150", "server": "7220", "farm": 8, "title": "IMG_0941", "ispublic": 1, "isfriend": 0, "isfamily": 0,
        "description": { "_content": "photo for testing some api functions" }, "license": 0, "dateupload": "1337237198", "datetaken": "2006-10-15 10:25:41", "datetakengranularity": 0, "ownername": "zalew", "iconserver": "2519", "iconfarm": 3, "originalsecret": "1aa3a9cc5b", "originalformat": "jpg", "lastupdate": "1337237201", "latitude": 0, "longitude": 0, "accuracy": 0, "context": 0, "tags": "test", "machine_tags": "", "o_width": "1600", "o_height": "1200", "views": 1, "media": "photo", "media_status": "ready", "pathalias": "zalew", "url_sq": "http:\/\/farm8.staticflickr.com\/7220\/7213959622_c354340150_s.jpg", "height_sq": 75, "width_sq": 75, "url_t": "http:\/\/farm8.staticflickr.com\/7220\/7213959622_c354340150_t.jpg", "height_t": 75, "width_t": 100, "url_s": "http:\/\/farm8.staticflickr.com\/7220\/7213959622_c354340150_m.jpg", "height_s": "180", "width_s": "240", "url_q": "http:\/\/farm8.staticflickr.com\/7220\/7213959622_c354340150_q.jpg", "height_q": "150", "width_q": "150", "url_m": "http:\/\/farm8.staticflickr.com\/7220\/7213959622_c354340150.jpg", "height_m": "375", "width_m": "500", "url_n": "http:\/\/farm8.staticflickr.com\/7220\/7213959622_c354340150_n.jpg", "height_n": "240", "width_n": "320", "url_z": "http:\/\/farm8.staticflickr.com\/7220\/7213959622_c354340150_z.jpg", "height_z": "480", "width_z": "640", "url_c": "http:\/\/farm8.staticflickr.com\/7220\/7213959622_c354340150_c.jpg", "height_c": "600", "width_c": "800", "url_l": "http:\/\/farm8.staticflickr.com\/7220\/7213959622_c354340150_b.jpg", "height_l": "768", "width_l": "1024", "url_o": "http:\/\/farm8.staticflickr.com\/7220\/7213959622_1aa3a9cc5b_o.jpg", "height_o": "1200", "width_o": "1600" },
      { "id": "7213959784", "owner": "91259891@N00", "secret": "1d3a2a84ed", "server": "8156", "farm": 9, "title": "IMG_0934", "ispublic": 1, "isfriend": 0, "isfamily": 0,
        "description": { "_content": "photo for testing some api functions" }, "license": 0, "dateupload": "1337237197", "datetaken": "2006-10-15 10:09:08", "datetakengranularity": 0, "ownername": "zalew", "iconserver": "2519", "iconfarm": 3, "originalsecret": "5baf16000e", "originalformat": "jpg", "lastupdate": "1337237202", "latitude": 0, "longitude": 0, "accuracy": 0, "context": 0, "tags": "test", "machine_tags": "", "o_width": "1600", "o_height": "1200", "views": 2, "media": "photo", "media_status": "ready", "pathalias": "zalew", "url_sq": "http:\/\/farm9.staticflickr.com\/8156\/7213959784_1d3a2a84ed_s.jpg", "height_sq": 75, "width_sq": 75, "url_t": "http:\/\/farm9.staticflickr.com\/8156\/7213959784_1d3a2a84ed_t.jpg", "height_t": 75, "width_t": 100, "url_s": "http:\/\/farm9.staticflickr.com\/8156\/7213959784_1d3a2a84ed_m.jpg", "height_s": "180", "width_s": "240", "url_q": "http:\/\/farm9.staticflickr.com\/8156\/7213959784_1d3a2a84ed_q.jpg", "height_q": "150", "width_q": "150", "url_m": "http:\/\/farm9.staticflickr.com\/8156\/7213959784_1d3a2a84ed.jpg", "height_m": "375", "width_m": "500", "url_n": "http:\/\/farm9.staticflickr.com\/8156\/7213959784_1d3a2a84ed_n.jpg", "height_n": "240", "width_n": "320", "url_z": "http:\/\/farm9.staticflickr.com\/8156\/7213959784_1d3a2a84ed_z.jpg", "height_z": "480", "width_z": "640", "url_c": "http:\/\/farm9.staticflickr.com\/8156\/7213959784_1d3a2a84ed_c.jpg", "height_c": "600", "width_c": "800", "url_l": "http:\/\/farm9.staticflickr.com\/8156\/7213959784_1d3a2a84ed_b.jpg", "height_l": "768", "width_l": "1024", "url_o": "http:\/\/farm9.staticflickr.com\/8156\/7213959784_5baf16000e_o.jpg", "height_o": "1200", "width_o": "1600" },
    ] }, "stat": "ok" }

json_sizes = { "sizes": { "canblog": 1, "canprint": 1, "candownload": 1,
                    "size": [
                      { "label": "Square", "width": 75, "height": 75, "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_c7458a7129_s.jpg", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/sq\/", "media": "photo" },
                      { "label": "Thumbnail", "width": 100, "height": 67, "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_c7458a7129_t.jpg", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/t\/", "media": "photo" },
                      { "label": "Small", "width": "240", "height": "160", "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_c7458a7129_m.jpg", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/s\/", "media": "photo" },
                      { "label": "Medium", "width": "500", "height": "333", "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_c7458a7129.jpg", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/m\/", "media": "photo" },
                      { "label": "Medium 640", "width": "640", "height": "427", "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_c7458a7129_z.jpg?zz=1", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/z\/", "media": "photo" },
                      { "label": "Large", "width": "1023", "height": "682", "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_c7458a7129_b.jpg", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/l\/", "media": "photo" },
                      { "label": "Original", "width": "1023", "height": "682", "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_d26fce212e_o.jpg", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/o\/", "media": "photo" }
                    ] }, "stat": "ok" }

json_exif = { "photo": { "id": "6110054503", "secret": "zzzzz", "server": "6199", "farm": 7, "camera": "Canon EOS 20D",
                    "exif": [
                      { "tagspace": "JFIF", "tagspaceid": 0, "tag": "JFIFVersion", "label": "JFIFVersion",
                        "raw": { "_content": 1.01 } },
                      { "tagspace": "JFIF", "tagspaceid": 0, "tag": "ResolutionUnit", "label": "Resolution Unit",
                        "raw": { "_content": "None" } },
                      { "tagspace": "IFD0", "tagspaceid": 0, "tag": "Rating", "label": "Rating",
                        "raw": { "_content": 1 } },
                      { "tagspace": "ExifIFD", "tagspaceid": 0, "tag": "ExposureTime", "label": "Exposure",
                        "raw": { "_content": "1\/100" },
                        "clean": { "_content": "0.01 sec (1\/100)" } },
                      { "tagspace": "ExifIFD", "tagspaceid": 0, "tag": "FNumber", "label": "Aperture",
                        "raw": { "_content": 2.8 },
                        "clean": { "_content": "f\/2.8" } },
                      { "tagspace": "ExifIFD", "tagspaceid": 0, "tag": "ExposureProgram", "label": "Exposure Program",
                        "raw": { "_content": "Aperture-priority AE" } },
                      { "tagspace": "ExifIFD", "tagspaceid": 0, "tag": "ISO", "label": "ISO Speed",
                        "raw": { "_content": 100 } },
                      { "tagspace": "ExifIFD", "tagspaceid": 0, "tag": "Flash", "label": "Flash",
                        "raw": { "_content": "Off, Did not fire" },
                        "clean": { "_content": 16 } },
                      { "tagspace": "ExifIFD", "tagspaceid": 0, "tag": "FocalLength", "label": "Focal Length",
                        "raw": { "_content": "30.0 mm" },
                        "clean": { "_content": "30 mm" } },
                      { "tagspace": "ExifIFD", "tagspaceid": 0, "tag": "DateTimeOriginal", "label": "Date and Time (Original)",
                        "raw": { "_content": "2011:09:03 18:43:47" } },
                      { "tagspace": "ExifIFD", "tagspaceid": 0, "tag": "CreateDate", "label": "Date and Time (Digitized)",
                        "raw": { "_content": "2011:09:03 18:43:47" } },
                      { "tagspace": "ExifIFD", "tagspaceid": 0, "tag": "ExposureCompensation", "label": "Exposure Bias",
                        "raw": { "_content": "-1\/3" },
                        "clean": { "_content": "-1\/3 EV" } },
                    ] }, "stat": "ok" }

json_geo = None

json_user = { "person": { "id": "91259891@N00", "nsid": "91259891@N00", "ispro": 1, "iconserver": "2519", "iconfarm": 3, "path_alias": "zalew",
                    "username": { "_content": "zalew" },
                    "realname": { "_content": "jakub zalewski" },
                    "mbox_sha1sum": { "_content": "xxxxxxxx" },
                    "location": { "_content": "" },
                    "photosurl": { "_content": "http:\/\/www.flickr.com\/photos\/zalew\/" },
                    "profileurl": { "_content": "http:\/\/www.flickr.com\/people\/zalew\/" },
                    "mobileurl": { "_content": "http:\/\/m.flickr.com\/photostream.gne?id=2306806" },
                    "photos": {
                      "firstdatetaken": { "_content": "1999-01-01 00:00:00" },
                      "firstdate": { "_content": "1232265567" },
                      "count": { "_content": "853" },
                      "views": { "_content": "3309" } } }, "stat": "ok" }

json_sets_list = { "photosets": { "cancreate": 1, "page": 1, "pages": 1, "perpage": 29, "total": 29,
    "photoset": [
      { "id": "72157627449841099", "primary": "6104844887", "secret": "xxxx6e", "server": "6081", "farm": 7, "photos": 6, "videos": 0,
        "title": { "_content": "nad Zegrzem" },
        "description": { "_content": "" }, "needs_interstitial": 0, "visibility_can_see_set": 1, "count_views": 3, "count_comments": 0, "can_comment": 1, "date_create": "1314940248", "date_update": "1314940250" },
      { "id": "72157627246467301", "primary": "6014904069", "secret": "fxxx3e", "server": "6014", "farm": 7, "photos": 94, "videos": 0,
        "title": { "_content": "Zachełmie, Jelenia Góra, Książ, Wałbrzych, Muzeum Miniatur Dolnego Śląska" },
        "description": { "_content": "" }, "needs_interstitial": 0, "visibility_can_see_set": 1, "count_views": 22, "count_comments": 0, "can_comment": 1, "date_create": "1312657071", "date_update": "1314934810" },
      { "id": "72157626691416808", "primary": "5707226627", "secret": "a49xxxx2a", "server": "2411", "farm": 3, "photos": 6, "videos": 0,
        "title": { "_content": "Łódź" }, }
    ] }, "stat": "ok" }

json_set_info = { "photoset": { "id": "72157627449841099", "owner": "91259891@N00", "primary": "6104844887", "secret": "fxxx26e", "server": "6081", "farm": 7, "photos": 6, "count_views": 3, "count_comments": 0, "count_photos": 6, "count_videos": 0,
    "title": { "_content": "nad Zegrzem" },
    "description": { "_content": "" }, "can_comment": 1, "date_create": "1314940248", "date_update": "1314940250" }, "stat": "ok" }

json_set_photos = { "photoset": { "id": "72157627449841099", "primary": "6104844887", "owner": "91259891@N00", "ownername": "zalew",
    "photo": [
      { "id": "6110599952", "secret": "xxxxxx", "server": "6087", "farm": 7, "title": "lizanie cukierka przez szybę", "isprimary": 1},
      { "id": "6110054827", "secret": "xxxxxx", "server": "6201", "farm": 7, "title": "święto kawalerii", "isprimary": 0},
      { "id": "6110054503", "secret": "xxxxxx", "server": "6199", "farm": 7, "title": "zdziwiony kotek", "isprimary": 0},
      { "id": "6110045859", "secret": "xxxxxx", "server": "6182", "farm": 7, "title": "kolorki", "isprimary": 0},
      { "id": "6110589742", "secret": "xxxxxx", "server": "6190", "farm": 7, "title": "most", "isprimary": 0 },
            { "id": "6105388484", "secret": "3xxxx45b", "server": "6078", "farm": 7, "title": "kwiatki", "isprimary": 0 },
    ], "page": 1, "per_page": "500", "perpage": "500", "pages": 1, "total": 6 }, "stat": "ok" }



json_collection_tree_user = { "collections": {
    "collection": [
      { "id": "2306806-72157628832150727", "title": "Travel", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif",
        "collection": [
          { "id": "2306806-72157628832176039", "title": "Germany", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
          { "id": "2306806-72157628832174511", "title": "Turkey", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
          { "id": "2306806-72157628832172707", "title": "Oman", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
          { "id": "2306806-72157628832793585", "title": "Netherlands", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
          { "id": "2306806-72157628832167505", "title": "United Arab Emirates", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
          { "id": "2306806-72157628832164035", "title": "Morocco", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" }
        ] },
      { "id": "2306806-72157628829299935", "title": "Warszawa", "description": "", "iconlarge": "http:\/\/farm8.staticflickr.com\/7005\/cols\/72157628829299935_b92bf5d0fd_l.jpg", "iconsmall": "http:\/\/farm8.staticflickr.com\/7005\/cols\/72157628829299935_b92bf5d0fd_s.jpg",
        "set": [
          { "id": "72157628829392599", "title": "Bielany", "description": "" },
          { "id": "72157617923644738", "title": "Warszawa", "description": "" },
          { "id": "72157620542349675", "title": "ej zrobcie tutaj miejsce z deka", "description": "bo bede zaraz tatatatanczyc breka" },
          { "id": "72157620597366137", "title": "warszawski deszcz", "description": "" },
          { "id": "72157622271517834", "title": "praskie spotkania z kultura", "description": "" }
        ] },
      { "id": "2306806-72157628829439561", "title": "moto", "description": "", "iconlarge": "http:\/\/farm8.staticflickr.com\/7005\/cols\/72157628829439561_0a97496f50_l.jpg", "iconsmall": "http:\/\/farm8.staticflickr.com\/7005\/cols\/72157628829439561_0a97496f50_s.jpg",
        "set": [
          { "id": "72157620884882249", "title": "bmw e23", "description": "zim zimma who got the keys to ma bimma\n\n<a href=\"http:\/\/bmwe23.wordpress.com\" rel=\"nofollow\">bmwe23.wordpress.com<\/a>\n\n-----------------------------------------------------------" },
          { "id": "72157623974867442", "title": "BMW Klub Polska - Zlot Wiosna 2010", "description": "<a href=\"http:\/\/bmw-klub.pl\" rel=\"nofollow\">bmw-klub.pl<\/a>" },
          { "id": "72157623823894012", "title": "e31 w galerii mockotów ", "description": "  <a href=\"http:\/\/posterous.com\" rel=\"nofollow\">Posted via email<\/a>  from <a href=\"http:\/\/jakubzalewski.net\/e31-w-galerii-mockotow\" rel=\"nofollow\">zalew<\/a>  " },
          { "id": "72157622943467192", "title": "Barbórka 2009 - Karowa", "description": "" },
          { "id": "72157622943438594", "title": "Ułęż 2009", "description": "spotkanie ścigancko-towarzyskie, BMW Klub Polska i inni" },
          { "id": "72157617139554505", "title": "BMW Klub Polska - Zlot Jesień 2008", "description": "" }
        ] }
    ] }, "stat": "ok" }

# collection with sets
json_collection_tree_col_sets = { "collections": {
    "collection": [
      { "id": "2306806-72157628829299935", "title": "Warszawa", "description": "", "iconlarge": "http:\/\/farm8.staticflickr.com\/7005\/cols\/72157628829299935_b92bf5d0fd_l.jpg", "iconsmall": "http:\/\/farm8.staticflickr.com\/7005\/cols\/72157628829299935_b92bf5d0fd_s.jpg",
        "set": [
          { "id": "72157628829392599", "title": "Bielany", "description": "" },
          { "id": "72157617923644738", "title": "Warszawa", "description": "" },
          { "id": "72157620542349675", "title": "ej zrobcie tutaj miejsce z deka", "description": "bo bede zaraz tatatatanczyc breka" },
          { "id": "72157620597366137", "title": "warszawski deszcz", "description": "" },
          { "id": "72157622271517834", "title": "praskie spotkania z kultura", "description": "" }
        ] }
    ] }, "stat": "ok" }

#collection with other collections
json_collection_tree_col_cols = { "collections": {
    "collection": [
      { "id": "2306806-72157628832150727", "title": "Travel", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif",
        "collection": [
          { "id": "2306806-72157628832176039", "title": "Germany", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
          { "id": "2306806-72157628832174511", "title": "Turkey", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
          { "id": "2306806-72157628832172707", "title": "Oman", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
          { "id": "2306806-72157628832793585", "title": "Netherlands", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
          { "id": "2306806-72157628832167505", "title": "United Arab Emirates", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
          { "id": "2306806-72157628832164035", "title": "Morocco", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" }
        ] },
      { "id": "2306806-72157628832176039", "title": "Germany", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
      { "id": "2306806-72157628832174511", "title": "Turkey", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
      { "id": "2306806-72157628832172707", "title": "Oman", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
      { "id": "2306806-72157628832793585", "title": "Netherlands", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
      { "id": "2306806-72157628832167505", "title": "United Arab Emirates", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" },
      { "id": "2306806-72157628832164035", "title": "Morocco", "description": "", "iconlarge": "\/images\/collection_default_l.gif", "iconsmall": "\/images\/collection_default_s.gif" }
    ] }, "stat": "ok" }

json_collection_info = { "collection": { "id": "2306806-72157628829299935",
    "title": { "_content": "Warszawa" },
    "description": { "_content": "" }, "child_count": 5, "datecreate": "1326320254", "iconlarge": "http:\/\/farm8.staticflickr.com\/7005\/cols\/72157628829299935_b92bf5d0fd_l.jpg", "iconsmall": "http:\/\/farm8.staticflickr.com\/7005\/cols\/72157628829299935_b92bf5d0fd_s.jpg",
    "iconphotos": {
      "photo": [
        { "id": "3668197375", "owner": "91259891@N00", "secret": "d27c065ed5", "server": "3543", "farm": 4, "title": "break na starówce", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
        { "id": "3893587576", "owner": "91259891@N00", "secret": "894ef4f468", "server": "2539", "farm": 3, "title": "smalec", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
        { "id": "3668202733", "owner": "91259891@N00", "secret": "4326db1cf4", "server": "3305", "farm": 4, "title": "break na starówce", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
        { "id": "6015004455", "owner": "91259891@N00", "secret": "55671d24cb", "server": "6020", "farm": 7, "title": "Centrum Nauki Kopernik", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
        { "id": "3893589024", "owner": "91259891@N00", "secret": "a9336b8b25", "server": "2552", "farm": 3, "title": "podwórko", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
        { "id": "5242581750", "owner": "91259891@N00", "secret": "57af4e803d", "server": "5121", "farm": 6, "title": "stadion most", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
        { "id": "6015002763", "owner": "91259891@N00", "secret": "525b7532aa", "server": "6006", "farm": 7, "title": "pasaż", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
        { "id": "5242583420", "owner": "91259891@N00", "secret": "db97b4bff3", "server": "5241", "farm": 6, "title": "stadion", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
        { "id": "3733608957", "owner": "91259891@N00", "secret": "a61fe74e1d", "server": "2449", "farm": 3, "title": "plac teatralny", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
        { "id": "3668195679", "owner": "91259891@N00", "secret": "3bf5805354", "server": "3582", "farm": 4, "title": "break na starówce", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
        { "id": "6015555176", "owner": "91259891@N00", "secret": "160e5378b2", "server": "6027", "farm": 7, "title": "Tamka", "ispublic": 1, "isfriend": 0, "isfamily": 0 },
        { "id": "3893588506", "owner": "91259891@N00", "secret": "fb558eb347", "server": "2477", "farm": 3, "title": "bazar różyckiego", "ispublic": 1, "isfriend": 0, "isfamily": 0 }
      ] }, "server": "7005", "secret": "b92bf5d0fd" }, "stat": "ok" }

