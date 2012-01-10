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
json_info = { "photo": { "id": "6110054503", "secret": "xxxxxx", "server": "6199", "farm": 7, "dateuploaded": "1315090210", "isfavorite": 0, "license": 0, "safety_level": 0, "rotation": 0, "originalsecret": "ddfgdfgd212e", "originalformat": "jpg", 
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
json_sizes = { "sizes": { "canblog": 1, "canprint": 1, "candownload": 1, 
                    "size": [
                      { "label": "Square", "width": 75, "height": 75, "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_c7458a7129_s.jpg", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/sq\/", "media": "photo" },
                      { "label": "Thumbnail", "width": 100, "height": 67, "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_c7458a7129_t.jpg", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/t\/", "media": "photo" },
                      { "label": "Small", "width": "240", "height": "160", "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_c7458a7129_m.jpg", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/s\/", "media": "photo" },
                      { "label": "Medium", "width": "500", "height": "333", "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_c7458a7129.jpg", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/m\/", "media": "photo" },
                      { "label": "Medium 640", "width": "640", "height": "427", "source": "http:\/\/farm7.staticflickr.com\/6199\/6110054503_c7458a7129_z.jpg", "url": "http:\/\/www.flickr.com\/photos\/zalew\/6110054503\/sizes\/z\/", "media": "photo" },
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
        "title": { "_content": "Łódź" },}
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

