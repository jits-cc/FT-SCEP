# FT-SCEP
FT-SCEP is a tool that generates index files, also known as shops, for [Tinfoil](https://tinfoil.io/Download#download). FT-SCEP supports encrypting index files, saving them locally as a raw JSON and an encrypted Tinfoil file, and uploading it to Google Drive. FT-SCEP also supports custom VM code. Please read below for how to use this tool.

### Configuration Files
FT-SCEP uses configuration files that you generate. Here is an example one fully filled out.

```json
{
  "name": "FT-SCEP Test",
  "credentials": "google_creds.json",
  "token": "mytoken.json",
  "mirrors": [
    "1mLbgd1Cog4FoLdEr1_-ZrSFFf__q13WB",
    "1mLbgd1Cog4FOlDeR2_-ZrSFFf__q13WB",
    "1mLbgd1CoFOLDER3zd_-ZrSFFf__q13WB"
  ],
  "retail_list": "https://raw.githubusercontent.com/blawar/titledb/master/retailOnly.txt",
  "titledb": "https://raw.githubusercontent.com/blawar/titledb/master/titles.US.en.json",
  "encryption_key": "keys/14.public.key",
  "vm_file": "do_y.cat",
  "shop_configurations": [ 
    {
      "name": "My Games",
      "includes": "0333",
      "encryption_key": "keys/11.public.key",
      "file_id": "1mLbgd1Cog4shDE2zd_-ZrSFFf__q13WB",
      "tinfoil_path": "ftscep-shop.tfl",
      "json_path": "ftscep-shop.json",
      "shop_contents": {
        "success": "Welcome to FT-SCEP PoC Shop!"
      }
    },
    {
      "name": "Language Packs",
      "includes": "1000",
      "vm_file": "do_x.cat",
      "file_id": "1mLbsd1og4GhD62zd_-ZrSFFf__q13WB",
      "tinfoil_path": "ftscep-shop-packs.tfl",
      "json_path": "ftscep-shop-packs.json"
    }
  ]
}
```

Let's go over what each part means.

---
#### Name
The configuration name. The name is for presentation purpose only while the tool is running. It is not present anywhere in the shop. This is an optional field.
#### Google Credentials and Token
To function correctly, the tool requires a credentials and token. If you have these already in JSON format, you can use them here. If not, you will have to generate them. More on this in a future commit. These are required.
#### Mirrors
This is a list of Google Folder IDs, pointing to folders containing the games you want included in your shops. The tool will go through all of them. There are technically optional, but without them, there's no merit to this.
#### TitleDB and Retail List
These should be URIs pointing to the source of TitleDB. Only TitleDB is required.
#### Encryption Key and VM Code
The encryption key and VM code can be specified in the main configuration and it will be used for all the shop configurations, unless a shop configuration has their own. These are optional.

---
#### Shop Configurations
Here is where you can specify the shops you want generated. You can have multiple shop configurations.

##### Name
The shop configuration name. The name is for presentation purpose only while the tool is running. It is not present anywhere in the shop. This is an optional field.
##### Includes Value
An Includes Value is a 4 digit long value that let's the tool know what you want to include in the shop.

The first value represents langauge packs. `0` to not include them. `1` to include them.
The second, third, and fourth value represent base, updates, and DLC titles, respectively. `0` to not include them, `1` to only include first party, `2` to only included non-first party. `3` to include everything.

`1310`, for example, will tell the tool to include language packs, all base titles, updates for first party only, and to leave out all the DLC.

The includes value is optional, and if left out, no files will be included in the shop.
##### Encryption Key and VM Code
Including custom VM code and encryption keys per shop configuration will supersede the values specified in the main configuration. 
##### File ID
The File ID is a Google File ID pointing to where you would like the tool to upload the output shop to. This is an optional field.
##### Tinfoil and JSON Path
You can specify save paths, with full filename, for the encrypted JSON (if encrypted, otherwise ignored) and the JSON shop. The tool will save to the locations specified. These are optional fields.
##### Shop Contents
These are contents directly copied over to the shop, such as the success message. Anything included here, whether valid or not, will be included in the shop. You can leave this out to only include files in the shop.

---

#### Flags
FT-SCEP has a few flags at the moment.
##### `-c [Folder ID]`
This will create new files in Google Drive to upload your shops to. It will create them by default in your root folder (My Drive) unless you specify a folder ID to create them in. They are saved to your configuration file automatically. The newly created files are made accessible by link by anyone automatically. It will also set a very nice icon of Tinfoil as the thumbnail for a Tinfoil index file.
##### `--cache-ttl [TTL]`
TitleDB is rather large, and is constantly updated. FT-SCEP will cache the TitleDB and use it instead of redownloading the TitleDB each time. It has a lifespan of 28800 seconds. You can change the TTL with this flag.
##### `--cache-path [path]`
You can change the cache save path using this flag.
