Title: Test of image renditions
Date: 2018-04-05 02:17:49-07:00
Entry-ID: 336
UUID: a28a68eb-c668-4fb8-9d3a-6cbcc3920772

Image rendition tests

.....

External image:

![](http://beesbuzz.biz/d/lewi/lewi-51.jpg)

External image in a link and with width set:

[![](http://beesbuzz.biz/d/lewi/lewi-52.HIDPI.jpg{250} "so smol")](http://beesbuzz.biz/d/)

External image with width and height set:

![{320,320,div_class="gallery"}](
http://beesbuzz.biz/d/lewi/lewi-52.jpg "fit"
| http://beesbuzz.biz/d/lewi/lewi-52.jpg{resize="fill"} "fill"
| http://beesbuzz.biz/d/lewi/lewi-52.jpg{resize="stretch"} "stretch")


Local image:

![alt text](rawr.jpg "test single image")

![alt text](
rawr.jpg{width=240} "test lightbox" |
rawr.jpg{width=120} |
rawr.jpg "image 3"
)

![alt text](rawr.jpg "test single image")

![broken image](alsdkfjaks asdlfkas fsalkfj salfsa)

![broken spec](foo{123[]})

![broken spec](poiu{100} foo{200})


![such gallery{255,gallery_id="rawry"}](rawr.jpg | rawr.jpg{fullscreen_width=50} "Rawr!" | rawr.jpg{100}
| http://beesbuzz.biz/d/lewi/lewi-52.HIDPI.jpg)



transparent png:

![](notsmiley.png)

converted to jpeg, no background:

![](notsmiley.png{format="jpg"})

converted to jpeg, black background:

![](notsmiley.png{format="jpg",background="black"})

converted to jpeg, red background using a tuple:

![](notsmiley.png{format="jpg",background=(255,0,0)})

converted to jpeg, white background using hex code:

![](notsmiley.png{format="jpg",background='#fff'})
