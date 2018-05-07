Title: Test of image renditions
Date: 2018-04-05 02:17:49-07:00
Entry-ID: 336
UUID: a28a68eb-c668-4fb8-9d3a-6cbcc3920772

Image rendition tests

.....

## External images

External image with width set

![](//publ.beesbuzz.biz/static/images/IMG_0377.jpg{250} "so smol")

External image with height set

![](//publ.beesbuzz.biz/static/images/IMG_0377.jpg{height=250} "less smol")


External image with width and height set, with different scaling modes:

![{320,320,div_class="gallery",gallery_id="sizing"}](
//publ.beesbuzz.biz/static/images/IMG_0377.jpg "fit"
| //publ.beesbuzz.biz/static/images/IMG_0377.jpg{resize="fill"} "fill"
| //publ.beesbuzz.biz/static/images/IMG_0377.jpg{resize="stretch"} "stretch")


## Local images

![alt text](rawr.jpg "test single image")

![alt text](
rawr.jpg{width=240} "test lightbox" |
rawr.jpg{width=120} |
rawr.jpg "image 3"
)

![alt text](rawr.jpg "test single image")


## Mixed-content gallery

![such gallery{255,gallery_id="rawry"}](rawr.jpg | rawr.jpg{fullscreen_width=50} "Rawr!" | rawr.jpg{100}
| //publ.beesbuzz.biz/static/images/IMG_0377.jpg)


## PNG transparency

Base image:

![](notsmiley.png)

converted to jpeg, no background:

![](notsmiley.png{format="jpg"})

converted to jpeg, black background:

![](notsmiley.png{format="jpg",background="black"})

converted to jpeg, red background using a tuple:

![](notsmiley.png{format="jpg",background=(255,0,0)})

converted to jpeg, white background using hex code:

![](notsmiley.png{format="jpg",background='#fff'})

converted to jpeg, cyan background, multiple qualities on the spectrum:

![{256,background='cyan',format='jpg'}](
notsmiley.png{quality=1} "quality 1"
| notsmiley.png{quality=50} "quality 50"
| notsmiley.png{quality=99} "quality 99"
| notsmiley.png "quality default"
)

## Broken/parse failures

![broken image](missingfile.jpg)

![broken spec](foo{123[]})

![broken spec](poiu{100} foo{200})

![broken imageset](rawr.jpg rawr.jpg)
