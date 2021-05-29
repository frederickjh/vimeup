# Translation of Vimeup

When code has been added the strings in Vimeup that will need to be translated to have the user interface in another language. After adding new string to the code the following command can be run to update the vimeup.pot file that can be used to create new translations from or update existing translations.

``` bash
pybabel extract --keywords=t ./vimeup.py -o locale/vimeup.pot
```
The coder has decided to name the translation function `t()` instead of the Python default translation function of `_()`. This is why there is the `--keywords=t` part in the command above. The default translation function can also be used, but I think that `t()` for translation is clearer as to what it does.

[Poedit](https://poedit.net/) can be downloaded for Windows, MacOS and Linux to translate the `.po` files for a new or existing translation. It can also be used to update the translation strings from either the `.pot` file or directly from the source code of `vimeup.py`.

## Poedit Configuration for Vimeup
### Catalog Properties

* Catalog > Properties
   * Translation Properties tab
      * Project name and version = Vimeup and the current version number.
      * Language, select the country, language pair for the translation
      * Charset and Source code charset = UTF-8
   * Sources Paths tab
      * Paths
         * Add the path to vimeup.py
   * Sources Keywords
      * Additional keywords
         * Add the key word "t".

### Poedit Preferences
   * Edit > Preferences >
      * General tab
         * Set the name and email address of the translator
         * Tick "Automatically compile MO file when saving" NOTE: This will be done after first manually compiling the MO file (File > Compile to MO...).
         * Tick "Show summary after catalog update"
      * Advanced tab
         * Set "Line endings:" to Unix (recommended).