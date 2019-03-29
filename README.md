# TV EPG generator

This EPG generator comes from the need to produce a EPG file for a channels' list, where each of channels' EPG can come from different EPG providers.
We always see EPG generators that grab all the channels from a provider and produce its own list, but I failed to find one that allows to chose which provider
to use for a specific channel.

This script is written in Python3 and produces a XMLTV compatible xml file, with all the channels and programmes selected.

## Installing

Some providers depend on external libraries, so you'll need to install the following:

`pip3 install beautifulsoup4 pytz`

Then `git clone` the repository and check the Usage section below.


## Example: channelList.xml

The channel list input file is a simple XML, as follows:

```
<?xml version="1.0" encoding="UTF-8"?>
<channelList>
    <channel>
        <tvg-id name="Channel 1 HD" icon="https://icon_url.png">channel_id</tvg-id>
        <provider code="PC001">PROVIDER</provider>
    </channel>
    ...
</channelList>
```

- tvg-id name: M3U display name
- tvg-id icon: URL to the icon for this channel
- tvg-id: channel_id, which will identify the channel and its programmes in the XMLTV file.
- provider code: Code for which this channels is identified by by the EPG provider
- provider PROVIDER: Provider tag, which identified the provider module that will be handling fetching the EPG for this channel.

## Usage

Once the channel list xml is created just run the script:

```
usage: tvEPG.py [-h] [-i INPUT] [-o OUTPUT] [-d DAYS] [-p PROVIDER] [-c CHANNEL] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Specify the input channel list file
  -o OUTPUT, --output OUTPUT
                        Specify the output XMLTV filename
  -d DAYS, --days DAYS  Specify the number of days to process
  -p PROVIDER, --provider PROVIDER
                        Filter on provider
  -c CHANNEL, --channel CHANNEL
                        Filter on channel (name)
  --debug               Turn debug on
```

A xml file will be generated with the channels and programmes contents if no errors occur.

## Adding a new provider

Providers are stored in `providers` module, add one and add it to the if condition of providers in the `tvEPG.py`.

Providers get a list of ChannelInfo objects and the number of days of programmes to look at. The ChannelInfo is basically the `<channel>` information.
The provider should produce and return two lists, one for channels containing `Channel` objects and another for programmes containing `Programme` objects.

Dates produces by the providers need to be in the following format:

`%Y%m%d%H%M%S +DST_OFFSET` - Example: `20181022190000 +0100`

## Known issues
This is very poorly tested and it works for the providers I include, there's no guarantees this will work without changes for new EPG providers, nor that this produces a EPG file compatible with your system. Please provide me with examples and I'll try to improve it, or simply submit a PR.

I used this project to learn Python, so please bear with me if things are poorly done and/or designed. Many things might be improved which I'll do as soon as I'm aware of them.

Feedback, improvements or suggestions are always welcome.

## Roadmap
In no specific order:

- Find a way to dynamically register providers without the need to change `tvEPG.py`
- Move all the date format and handling outside of the providers, or pass the format to the providers.
- Be more resilient, in case any provider breaks, we don't stop the EPG generation.
- Support for more than one provider for each channel, so that if one provider fails we can fall back to another.
- More providers, including a generic provider to fetch channels and programmes from another xmltv file.
- Register hooks to perform certain operations at the end, i.e. Dropbox uploader, FTP file, zip/rar/compress output file, etc..
- Provide utilities for provider classes to make https requests
- Add (more) logging
- Make use of the xmltv `episode-num` tag
- ...

## Credits
This was heavily inspired from an EPG script from warlockPT, which only supported MEO. I decided to pick up his channel list definition on XML idea and took it from there.

## License
GPL3
