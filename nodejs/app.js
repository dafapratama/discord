import { sleep } from "./utils/utils.js";
import { getChannelMessages } from "./wrappers/getChannelMessages.js";
import { getChannelName, getChannels } from "./wrappers/getChannels.js";
import fs from "fs";
import { exportUserInfo } from "./wrappers/getAccountInfo.js";
import prompt from "prompt";

const exportAllDms = async (token) => {
  const channels = await getChannels(token);
  // console.log(`Found ${channels.length} dms`);
  // console.log("Starting to export dms...");
  console.log(channels)

  for (let channel of channels) {
    let messages = await getChannelMessages(token, channels[0]["id"]);
    let channelname = await getChannelName(token, channels[0]["id"]);
    fs.mkdirSync(`./output/dms/${channelname}`, { recursive: true });
    fs.writeFileSync(
      `./output/dms/${channelname}/messages.json`,
      JSON.stringify(messages)
    );
    console.log(`Finished exporting (${channelname})`);

    await sleep(500);
  }
};

const exportAccountInfo = async (token) => {
  const accountInfo = await exportUserInfo(token);
  fs.mkdirSync(`output`, { recursive: true });
  fs.writeFileSync(`./output/accountinfo.json`, JSON.stringify(accountInfo));
  console.log(`Finished exporting account info`);
};

prompt.start();
prompt.get(["token"], function (err, result) {
  if (err) {
    return onErr(err);
  }
  exportAccountInfo(result.token);
  exportAllDms(result.token);
});
