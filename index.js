console.log("Beep beep i'm a sheep!");

require("dotenv").config();
const https = require("https");
const http = require('http');

const Discord = require("discord.js");
const client = new Discord.Client();

const regexCorso = /!corso (\d+)/;

client.login(process.env.BOT_TOKEN);

client.on("ready", () => {
  console.log("I like trains!");
});

client.on("message", msg => {
  //if(msg.channel.id==idDelCanale) // Limita il canale
  if(msg.content.toLowerCase() == "!ping")
    msg.reply("Pong!");
  else if(msg.content.toLowerCase() == "!classificau")
    msg.reply("https://www.umanet.net/students/ranking/2");
  else if(msg.content.toLowerCase() == "!spoonriver")
    msg.reply("Schifo totale! :face_vomiting:");
  else if(msg.content.toLowerCase() == "!corsi") {
    let testo = "";
    https.get("https://www.umanet.net/api/subjects/", res => {
      res.on('data', d => testo += d);
      res.on("end", () => {
        testo = eval(testo);
        let ris = "I corsi sono:\n";
        for(let i = 0; i < testo.length; i++)
          ris += testo[i].title + "\n";
        msg.reply(ris);
      });
    });
  } else if(msg.content.toLowerCase().match(regexCorso)) {
    const id = regexCorso.exec(msg.content.toLowerCase())[1];
    let testo = "";
    https.get("https://www.umanet.net/api/courses/", res => {
      res.on('data', (d) => testo += d);
      res.on("end", () => {
        testo = eval(testo);
        let ris = "Corso ";
        for(let i = 0; i < testo.length; i++)
          if(testo[i].id == id) {
            ris += testo[i].title + ":\n";
            ris+="Paragrafi:\n";
            for(let j=0; j<testo[i].modules.length; j++) {
              ris+="--"+testo[i].modules[j].title+"\n";
              if(testo[i].modules[j].description)
                ris+="----"+testo[i].modules[j].description+"\n";
            }
          }
        msg.reply(ris);
      });
    });
  }
});



 http.createServer(function (request, response) {
    response.writeHead(200, { 'Content-Type': 'text/html' });
    response.end("<h1>Ciao</h1>", 'utf-8');
 }).listen(process.env.PORT||5000);