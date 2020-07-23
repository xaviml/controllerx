


### Sonos/Symfonisk display unit with ESPHome
Using ControllerX - Controlling your Sonos speakers have never been easier 😎 But the occasional wish for visual check on what’s actually playing, volume setting, media artist/title, active speakers in group etc. is still there. Leaving a display integration as the obvious solution for this need.

All it takes is an ESP8266 with ESPHome software, an appropriate display, a handful of HA sensors and you’re all set to go 🚀 ESPHome is a system framework for ESP8266 units that has support for several I2C OLED/E-ink display types and numerous sensors, has direct HA integration via add-on and easy, yet powerful YAML configuration. Read more about ESPHome and how to set it up in HA here: https://esphome.io/

### Hardware:
Wemos D1 mini – ESP8266
https://www.aliexpress.com/item/32845253497.html?spm=a2g0s.9042311.0.0.27424c4dFNzmlu

2,42” 12864 SSD1309 display (direct replacement for the much smaller 0,96” SSD1306 display and can use same library)
https://www.aliexpress.com/item/33024448944.html?spm=a2g0s.9042311.0.0.27424c4d28nV4A

One note on the SSD1309 display. In order to get it to work as I2C instead of SPI, you need to do a bit of soldering. On the specific display type I bought, you need to bridge (short) R5 and move R4 to R3. Remember that display will NOT work unless RES is connected to RST on ESP8266 (or any available pin and controlled in ESPHome sw). Note: Display only supports 3,3v on VCC. Some have reported that display tolerates 5v. I wouldn’t take that risk, though! I’ve kept both CS and DS ‘floating’. Haven’t had any I2C address issues so far. Use pull-up/down resistors if you experience issues.

### Display setup:
My current display setup consists of four pages that all are displayed for 5 seconds.

Information on screen:
-	All pages: Source (if not present, display ‘Sonos Playlist’), volume setting and play/pause/idle status.
•	Page 1: Active master/slave speakers.
•	Page 2: Media artist/media title (if not available from stream, display time instead)
•	Page 3: Display time
•	Page 4: Display outdoor temperature sensor value

If you only need the Sonos playing details on display, you can just remove page 3 & 4 from the YAML configuration.

### True Type Fonts:
Three 'standard' Calibri TT fonts are used plus a special version of Heydings Icons font in which I've included some Heydings Controls icons as well.
Calibri TTF fonts link: [https://www.fontdload.com/dl/calibri-font/](https://www.fontdload.com/dl/calibri-font/)
Heydings Icons special file link: ???
Copy Calibri Bold, Calibri Regular, Calibri Light fonts plus the special Heydings Icons font file to the ESPHome folder (/config/ESPHome/)


### Home Assistant sensors:
Below you’ll find the HA template sensors needed in `configuration.yaml `for ESPHome display to work.

Note: `media_artist` and `media_title` attributes from HA's Sonos integration could be swapped for some radio stations, as these attributes are split from one combined string in the stream. Some radio stations have artist - title order, others use title - artist. You really can't tell...
My danish radio stations (source list) all use the 'swapped' version, so my templates below swap these two attributes for radio stations. 

Enter master speaker as entity ID for all bla bla bla
Without this specific hardcoded entity, templates simply doesn't always update correctly.
Needed for now.

```yaml
# Sonos sensors
sensor:
  - platform: template
    sensors:
      sonos_master_friendly:
        friendly_name: "Sonos Master Friendly"
        entity_id: group.sonos_all
        value_template: "{{ state_attr(state_attr('group.sonos_all', 'entity_id')[0], 'friendly_name') }}"
      sonos_slaves_friendly:
        friendly_name: "Sonos Slaves Friendly"
        entity_id: group.sonos_all
        value_template: >- 
           {% for entity_id in state_attr("group.sonos_all", "entity_id")[1:] -%}
             {% set friendly_name = state_attr(entity_id, "friendly_name") %}
             {%- if loop.last %}{{ friendly_name }}{% else %}{{ friendly_name }}, {% endif -%}
           {%- endfor %}
      media_title:
        entity_id: media_player.kokken # Sonos master speaker
        value_template: >-
          {% if is_state('sensor.media_source' , "no source") %}
            {{ state_attr(state_attr('group.sonos_all', 'entity_id')[0], 'media_title') }}
          {% else %}
            {{ state_attr(state_attr('group.sonos_all', 'entity_id')[0], 'media_artist') }}
          {% endif %}
      media_artist: # Swap title/artist if 'source' attribute is not present = radio
        entity_id: media_player.kokken # Sonos master speaker
        value_template: >-
          {% if is_state('sensor.media_source' , "no source") %}
            {{ state_attr(state_attr('group.sonos_all', 'entity_id')[0], 'media_artist') }}
          {% else %}
            {{ state_attr(state_attr('group.sonos_all', 'entity_id')[0], 'media_title') }}
          {% endif %}
      media_album_name:
        entity_id: media_player.kokken # Sonos master speaker
        value_template: "{{ state_attr(state_attr('group.sonos_all', 'entity_id')[0], 'media_album_name') }}"
      media_source: # Remove all after 'DR P4 Fyn' as source (to fit on display)
        entity_id: media_player.kokken # Sonos master speaker
        value_template: >-
          {% if state_attr(state_attr('group.sonos_all', 'entity_id')[0], 'source') %}
            {{states.media_player.kokken.attributes.source.split('96.8')[0]}}
          {% else %}
            no source
          {% endif %}
      volume:
        entity_id: media_player.kokken # Sonos master speaker
        value_template: "{{ state_attr(state_attr('group.sonos_all', 'entity_id')[0], 'volume_level')|float * 100 }}"
      gruppe: # USed YES !!
        entity_id: media_player.kokken # Sonos master speaker
        value_template: "{{ state_attr(state_attr('group.sonos_all', 'entity_id')[0], 'sonos_group') }}"
```

### Home Assistant group:
bla bla bla
If you're only using one speaker, you still need to create the group and populate with that single entity as the group entity is needed in the code. 

```yaml
sonos_all:
	name: sonos_all
	entities:
	  - media_player.office #this HAS to be your MASTER speaker
	  - media_player.kitchen #SLAVE speaker #1
	  - media_player.livingroom #SLAVE speaker #2
```

### Home assistant automations:
bla bla bla

```yaml
- id: test_gruppeskift
  alias: test_gruppeskift
  trigger:
    platform: state
    entity_id: sensor.gruppe
  action:
  - service: group.set
    data_template:
      object_id: sonos_all
      entities: "{{ state_attr(state_attr('group.sonos_all', 'entity_id')[0], 'sonos_group') | join(',') }}"

- id: Sonos reset to radio
  alias: Sonos reset to radio
  trigger:
    platform: state
    entity_id: sensor.0x90fd9ffffe0cbd69_action
    to: 'toggle_hold'
  action:
  - service: light.turn_on
    data:
      entity_id: light.kokkenbord_5
      flash: short
  - service: sonos.join
    data:
      master: media_player.kokken
      entity_id:
      - media_player.stue
      - media_player.alrum
  - service: media_player.volume_set
    data_template:
      entity_id:
      - media_player.kokken
      - media_player.alrum
      - media_player.stue
      volume_level: 0.25
  - service: media_player.select_source
    data:
      entity_id: media_player.kokken
      source: 'DR P4 Fyn 96.8 (Nyheder)'
  - service: media_player.media_play
    entity_id: media_player.kokken
```


### ESPHome YAML configuration:
bla bla (loads of template sensors needed, as ESPHome currently don't support attributes.
Need to enter two things. Your Sonos master speaker entity and temparature sensor.
Temp sensor is not needed. You can just delete page 3 & 4 from the display configuration.

```yaml
esphome:
  name: ssd1309
  platform: ESP8266
  board: d1_mini

wifi:
  ssid: "your ssid"
  password: "your password"

  # Enable fallback hotspot (captive portal) in case wifi connection fails
  ap:
    ssid: "Ssd1309 Fallback Hotspot"
    password: "Autogenerated password"
captive_portal:

# Enable logging
logger:

# Enable Home Assistant API
api:

ota:

time:
  - platform: homeassistant
    id: esptime

sensor:
    # Outdoor temperature sensor - only used in lambda page 4
  - platform: homeassistant
    id: outdoor_temp
    entity_id: sensor.your_temperature_sensor
    internal: true
  - platform: homeassistant
    id: sonos_volume
    entity_id: sensor.volume
    internal: true

text_sensor:
    # Sonos master speaker
  - platform: homeassistant  
    id: sonos_status
    entity_id: media_player.your_master_speaker
    internal: true
  - platform: homeassistant  
    id: media_source
    entity_id: sensor.media_source
    internal: true
  - platform: homeassistant
    id: media_artist
    entity_id: sensor.media_artist
    internal: true
  - platform: homeassistant
    id: media_title
    entity_id: sensor.media_title
    internal: true
  - platform: homeassistant
    id: sonos_master
    entity_id: sensor.sonos_master_friendly
    internal: true
  - platform: homeassistant
    id: sonos_slaves
    entity_id: sensor.sonos_slaves_friendly
    internal: true
    
font:
  - file: "Calibri Bold.ttf"
    id: font_large
    size: 23
    glyphs: '!%"()+,-_.:°0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz█£$@æøåÆØÅ&#''´’?üöäé'
  - file: "Calibri Regular.ttf"
    id: font_medium
    size: 19
    glyphs: '!%"()+,-_.:°0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz█£$@æøåÆØÅ&#''´’?üöäé'
  - file: "Calibri Light.ttf"
    id: font_small
    size: 11
    glyphs: '!%"()+,-_.:°0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz█£$@æøåÆØÅ&#''´’?üöäé'
  - file: "Calibri Bold.ttf"
    id: font_small_bold
    size: 12
    glyphs: '!%"()+,-_.:°0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz█£$@æøåÆØÅ&#''´’?üöäé'
  - file: "HeydingsIconsSymbols.ttf"
    id: font_icons_small
    size: 11
    glyphs: '067HADJabjsmx'
  - file: "HeydingsIconsSymbols.ttf"
    id: font_icons_medium
    size: 19
    glyphs: '067HADJabjsmx'
  - file: "HeydingsIconsSymbols.ttf"
    id: font_icons_14
    size: 14
    glyphs: '067HADJabjsmx'
  
i2c:
  sda: D1
  scl: D2

interval:
  - interval: 5s
    then:
      - display.page.show_next: sonos
      - component.update: sonos

display:
  - platform: ssd1306_i2c
    model: "SSD1306 128x64"
    reset_pin: D0
    address: 0x3C
    brightness: 100%
    id: sonos
    pages:
      - id: page1
        lambda: |-
          // it.rectangle(0, 0, 128, 64); For visual check of display edges when playing with different fonts
          if (id(media_source).state != "no source") {
              it.printf(64, 0, id(font_large), TextAlign::TOP_CENTER, "%.12s", id(media_source).state.c_str()); // 
          } else {
              it.printf(64, 0, id(font_large), TextAlign::TOP_CENTER, "Sonos"); // if no source list attribute, display Sonos Playlist instead
          }
          it.printf(0, 20, id(font_icons_medium), TextAlign::TOP_LEFT, "m"); // speaker on sign
          it.printf(21, 22, id(font_medium), TextAlign::TOP_LEFT, "%.f", id(sonos_volume).state);
          if (id(sonos_status).state != "playing") {
              it.printf(127, 18, id(font_icons_medium), TextAlign::TOP_RIGHT, "7"); // pause sign
          } else {
              it.printf(127, 18, id(font_icons_medium), TextAlign::TOP_RIGHT, "6"); // play sign
          }
          it.printf(107, 22, id(font_medium), TextAlign::TOP_RIGHT, "%s", id(sonos_status).state.c_str());
          it.printf(00, 53, id(font_icons_small), TextAlign::BOTTOM_LEFT, "s"); // star sign for master speaker
          it.printf(64, 53, id(font_small_bold), TextAlign::BOTTOM_CENTER, "%s", id(sonos_master).state.c_str());
          it.printf(00, 65, id(font_icons_small), TextAlign::BOTTOM_LEFT, "a"); // chain sign for slave speaker(s)
          it.printf(64, 65, id(font_small), TextAlign::BOTTOM_CENTER, "%s", id(sonos_slaves).state.c_str());
         
      - id: page2
        lambda: |-
          // it.rectangle(0, 0, 128, 64); For visual check of display edges when playing with different fonts
          if (id(media_source).state != "no source") {
              it.printf(64, 0, id(font_large), TextAlign::TOP_CENTER, "%.12s", id(media_source).state.c_str()); // 
          } else {
              it.printf(64, 0, id(font_large), TextAlign::TOP_CENTER, "Playlist"); // if no source list attribute, display 'Sonos Playlist' instead
          }
          it.printf(0, 20, id(font_icons_medium), TextAlign::TOP_LEFT, "m"); // speaker on sign
          it.printf(21, 22, id(font_medium), TextAlign::TOP_LEFT, "%.f", id(sonos_volume).state);
          if (id(sonos_status).state != "playing") {
              it.printf(127, 18, id(font_icons_medium), TextAlign::TOP_RIGHT, "7"); // pause sign
          } else {
              it.printf(127, 18, id(font_icons_medium), TextAlign::TOP_RIGHT, "6"); // play sign
          }
          it.printf(107, 22, id(font_medium), TextAlign::TOP_RIGHT, "%s", id(sonos_status).state.c_str());
          if (id(media_title).state != "None") {
              it.printf(73, 53, id(font_small), TextAlign::BOTTOM_CENTER, "%.24s", id(media_artist).state.c_str());
              it.printf(73, 65, id(font_small), TextAlign::BOTTOM_CENTER, "%.24s", id(media_title).state.c_str());
              it.printf(00, 53, id(font_icons_small), TextAlign::BOTTOM_LEFT, "A"); // person sign (artist)
              it.printf(01, 63, id(font_icons_14), TextAlign::BOTTOM_LEFT, "j"); // note sign (title)
          } else {
              it.strftime(64, 42, id(font_large), TextAlign::TOP_CENTER, "%H:%M:%S", id(esptime).now());
          }
      
      
      - id: page3
        lambda: |-
          // it.rectangle(0, 0, 128, 64); For visual check of display edges when playing with different fonts
          if (id(media_source).state != "no source") {
              it.printf(64, 0, id(font_large), TextAlign::TOP_CENTER, "%.12s", id(media_source).state.c_str()); // 
          } else {
              it.printf(64, 0, id(font_large), TextAlign::TOP_CENTER, "Sonos"); // if no source list attribute, display Sonos Playlist instead
          }
          it.printf(0, 20, id(font_icons_medium), TextAlign::TOP_LEFT, "m"); // speaker on sign
          it.printf(21, 22, id(font_medium), TextAlign::TOP_LEFT, "%.f", id(sonos_volume).state);
          if (id(sonos_status).state != "playing") {
              it.printf(127, 18, id(font_icons_medium), TextAlign::TOP_RIGHT, "7"); // pause sign
          } else {
              it.printf(127, 18, id(font_icons_medium), TextAlign::TOP_RIGHT, "6"); // play sign
          }
          it.printf(107, 22, id(font_medium), TextAlign::TOP_RIGHT, "%s", id(sonos_status).state.c_str());
          it.strftime(64, 42, id(font_large), TextAlign::TOP_CENTER, "%H:%M:%S", id(esptime).now());
       
      - id: page4   
        lambda: |-
          // it.rectangle(0, 0, 128, 64); For visual check of display edges when playing with different fonts
          if (id(media_source).state != "no source") {
              it.printf(64, 0, id(font_large), TextAlign::TOP_CENTER, "%.12s", id(media_source).state.c_str()); // 
          } else {
              it.printf(64, 0, id(font_large), TextAlign::TOP_CENTER, "Playlist"); // if no source list attribute, display Sonos Playlist instead
          }
          it.printf(0, 20, id(font_icons_medium), TextAlign::TOP_LEFT, "m"); // speaker on sign
          it.printf(21, 22, id(font_medium), TextAlign::TOP_LEFT, "%.f", id(sonos_volume).state);
          if (id(sonos_status).state != "playing") {
              it.printf(127, 18, id(font_icons_medium), TextAlign::TOP_RIGHT, "7"); // pause sign
          } else {
              it.printf(127, 18, id(font_icons_medium), TextAlign::TOP_RIGHT, "6"); // play sign
          }
          it.printf(107, 22, id(font_medium), TextAlign::TOP_RIGHT, "%s", id(sonos_status).state.c_str());
          it.printf(64, 42, id(font_large), TextAlign::TOP_CENTER, "Out: %.1f°C", id(outdoor_temp).state);
```

## Future improvement plans
Improve/simplify templates
remove need for master entity so many places in configs
display shuffle and mute sign
implement brightness control on display
implement display on/off via PIR ?
Add more information using a 2,9" E-ink display
Add png file to e-paper display
use e-paper display as status display when Sonos are idle

Thank you Xavi for providing the solution to some of my templating issues 👍😎

<!--stackedit_data:
eyJoaXN0b3J5IjpbNjg3NzU4NDg0XX0=
-->