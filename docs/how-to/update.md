---
layout: page
title: Update
---

Note that AppDaemon will need to be restarted when installing a new version of ControllerX. This is due to AppDaemon not reimporting the modules again. If AppDaemon server is not restarted, then it will keep executing the old version.

## Update from 2.1.X to 2.2.0

If you are updating from 2.1.X to 2.2.0, you will need to change your configuration.
- If you had `sensor` parameter, then you will need to change it to `controller` and add a new parameter `integration: z2m`
- If you had `event_id` parameter, then you will need to change it to `controller` and add a new parameter `integration: deconz`
