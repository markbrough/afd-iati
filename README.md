# AFD and IATI datastore download scripts
Converts AFD data from AFD projects database to IATI format, and downloads
data from the IATI datastore (will be separated in future).

## License (MIT)

Copyright (c) 2013 Mark Brough, Publish What You Fund

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

## How to run the AFD-IATI conversion script

The following steps assume a Linux environment; other systems may differ.

1. Clone the repository:

        git clone git@github.com:markbrough/afd-iati.git

2. Install the requirements. It's recommended you setup a `virtualenv` for this:

        virtualenv ./pyenv
        source ./pyenv/bin/activate
        pip install -r requirements.txt

3. Run the script:

        ./afd.py

4. The files (one IATI-XML file per country/region) will be output to:

        /afd

## Troubleshooting

The site downloads the data that is scraped each night from the AFD website by
Scraperwiki. Sometimes, the Scraperwiki site times out, so if you get a timeout
error, just try running the script again.
