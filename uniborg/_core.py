# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import asyncio
import traceback
import os
from datetime import datetime
from uniborg import util


DELETE_TIMEOUT = 5


@borg.on(util.admin_cmd(pattern="load (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def load_reload(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    try:
        if shortname in borg._plugins:  # pylint:disable=E0602
            borg.remove_plugin(shortname)  # pylint:disable=E0602
        borg.load_plugin(shortname)  # pylint:disable=E0602
        msg = await event.respond(f" എന്തോ ....എവിടെയോ ..... (re) തകരാറ്‌ പോലെ .....😨😨  {shortname} ഞാൻ സെറ്റാക്കിട്ടുണ്ട് ....🤗🤗")
        await asyncio.sleep(DELETE_TIMEOUT)
        await msg.delete()
    except Exception as e:  # pylint:disable=C0103,W0703
        trace_back = traceback.format_exc()
        # pylint:disable=E0602
        logger.warn(f"പൊന്നു മോനെ ..... (re) നീ അന്യേഷിച്ച {shortname} കാണുന്നില്ല .....🤗🤗: {trace_back}")
        await event.respond(f"നാശം ...... (re) നിന്റെ {shortname} എന്റെ കൈയ്യിൽ ഇല്ല...😡😡: {e}")


@borg.on(util.admin_cmd(pattern="(?:unload|remove) (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def remove(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    if shortname == "_core":
        msg = await event.respond(f" മോനെ ......😨😨 {shortname} ഇവൻ എറങ്ങി പോണില്ല .....😂😂")
    elif shortname in borg._plugins:  # pylint:disable=E0602
        borg.remove_plugin(shortname)  # pylint:disable=E0602
        msg = await event.respond(f" കുട്ടാ .....🥰🥰 {shortname} ഇനി അന്രേഷിക്കണ്ട കേട്ടൊ .....🤗🤗")
    else:
        msg = await event.respond(f"എടാ... {shortname} മൊത്തം virus ആണ് ...😬😬")
    await asyncio.sleep(DELETE_TIMEOUT)
    await msg.delete()


@borg.on(util.admin_cmd(pattern="send plugin (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def send_plug_in(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    input_str = event.pattern_match["shortname"]
    the_plugin_file = "./stdplugins/{}.py".format(input_str)
    start = datetime.now()
    await event.client.send_file(  # pylint:disable=E0602
        event.chat_id,
        the_plugin_file,
        force_document=True,
        allow_cache=False,
        reply_to=message_id
    )
    end = datetime.now()
    time_taken_in_ms = (end - start).seconds
    await event.edit("Plug ഞാൻ അയച്ചു ..... {} ഏകദേശം {} seconds വേണ്ടി വന്നു".format(input_str, time_taken_in_ms))
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()


@borg.on(util.admin_cmd(pattern="install plugin"))  # pylint:disable=E0602
async def install_plug_in(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                borg.n_plugin_path  # pylint:disable=E0602
            )
            if "(" not in downloaded_file_name:
                borg.load_plugin_from_file(downloaded_file_name)  # pylint:disable=E0602
                await event.edit("പുതിയ പ്ലഗ് കേറ്റി ഇട്ടിട്ടുണ്ട് എന്ന് പറയാൻ പറഞ്ഞു `{}`".format(os.path.basename(downloaded_file_name)))
            else:
                os.remove(downloaded_file_name)
                await event.edit("നീ പോയി പുതിയ പ്ലഗ് കൊണ്ടുവാ .....😏😏")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)
    await event.delete()
