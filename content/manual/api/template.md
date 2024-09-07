Title: Template object
Path-Alias: /api/template
Date: 2018-04-25 15:15:40-07:00
Entry-ID: 416
UUID: 26798d78-9d88-4fd5-95cd-f03baca12aff

Template API for the `template` object

.....

The `template` object provides the following:

* **`name`**: The name of the template
* **`filename`**: The underlying filename of the template
* **`last_modified`**: When the file was most recently modified
* <span id="func-image">**`image`**</span>: Resolves an image relative to this template's context, by path. This is a context-specific version of the [global `image` function](324#func-image).

