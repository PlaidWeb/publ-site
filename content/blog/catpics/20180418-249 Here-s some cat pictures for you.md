Title: Here's some cat pictures for you
Category: blog
Date: 2018-04-18 16:00:00-07:00
Entry-ID: 249
UUID: dcb8ca7a-2091-4d1d-aed2-6a1061064ff3
Path-Alias: /yay-cats-wooooo
Tag: demo
Tag: images
Tag: cats!!!

![{240,240,resize="fill",count_offset=7,div_class="gallery",more_text="There are {remain} more cat pictures!",more_class="caption"}](
IMG_20130701_223914.jpg "Why are there cat photos here?"
|1373225533243.jpg
|1377619425569.jpg
|1383506651641.jpg
|DSC00124.jpg "Well, I thought this would be a cute way to demonstrate..."
|DSC00125.jpg "Image galleries!"
|DSC00605.jpg
|DSC01272 - Version 2.jpg{fill_crop_x=.33}
|DSC07661.jpg "In particular, image galleries support a few neat things."
|DSC07672.jpg "For example, the blog and feed templates will only show a few images."
|DSC07926.jpg
|DSC07929.jpg
|DSC07935.jpg "And those images will link to the entry itself."
|DSC08896.jpg "But then when you click through, the whole gallery appears!"
|DSC09705.jpg "And we use Lightbox.js to present them nicely."
|IMG_0072.jpg "This is how I feel too."
|IMG_0074.jpg
|IMG_0086.jpg
|IMG_0118.jpg
|IMG_0122.jpg
|IMG_0131.jpg
|IMG_0133.jpg
)

.....

(If it isn't obvious, many of the images have captions. Try clicking on one!)

Anyway, this means Publ is now ready for me to start migrating my site over to
it. Eep/yay!


Oh, and if you want to see what the Markdown for the gallery looks like, here you go:

```markdown
![{240,240,resize="fill",count_offset=7,div_class="gallery",more_text="There are {remain} more cat pictures!",more_class="caption"}](
IMG_20130701_223914.jpg "Why are there cat photos here?"
|1373225533243.jpg
|1377619425569.jpg
|1383506651641.jpg
|DSC00124.jpg "Well, I thought this would be a cute way to demonstrate..."
|DSC00125.jpg "Image galleries!"
|DSC00605.jpg
|DSC01272 - Version 2.jpg{fill_crop_x=.33}
|DSC07661.jpg "In particular, image galleries support a few neat things."
|DSC07672.jpg "For example, the blog and feed templates will only show a few images."
|DSC07926.jpg
|DSC07929.jpg
|DSC07935.jpg "And those images will link to the entry itself."
|DSC08896.jpg "But then when you click through, the whole gallery appears!"
|DSC09705.jpg "And we use Lightbox.js to present them nicely."
|IMG_0072.jpg "This is how I feel too."
|IMG_0074.jpg
|IMG_0086.jpg
|IMG_0118.jpg
|IMG_0122.jpg
|IMG_0131.jpg
|IMG_0133.jpg
)
```

The `{240,240,resize="fill",count_offset=7}` in the alt text means "make thumbnails 240x240, and in a view with
a limit, skip the first 7 entries" (this is how `DSC01272 - Version 2.jpg` is used as the poster frame
on the index and feed), and each image is separated by a `|`. Oh, and spaces are allowed in filenames, and
newlines are allowed in the image specification.

Also, the `{fill_crop_x=.33}` parameter on `DSC01272 - Version 2.jpg` shifts the crop rectangle a little bit so
that Fiona is nicely centered in the thumbnail square. :)

Another thing to note: these files (including the .md file) are all stored in a directory called `/blog/catpics`,
but the entry has a `Category: blog` on it to make it appear as if it's in the `blog` category. Image file lookups
are relative to the markdown file, not to the URL, so I can move this directory anywhere on the site and it will
continue to work.
