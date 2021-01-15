console.log("Beep beep i'm a sheep!");

require("dotenv").config();

const Discord = require("discord.js");
const client = new Discord.Client();

client.login(process.env.BOT_TOKEN);

client.on("ready", ()=>{
  console.log("I like trains!");
});

client.on("message",msg=>{
  console.log(msg.content);
  //if(msg.channel.id==idDelCanale) // Limita il canale
  if(msg.content.toLowerCase() == "!ping") {
    msg.reply("Pong!");
  }
});