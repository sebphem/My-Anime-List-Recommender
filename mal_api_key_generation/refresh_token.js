import config from '../keys/config.json' assert {type:'json'}
import mal_token from '../keys/mal_token.json' assert {type:'json'}
import fs from 'fs';

let url = `https://myanimelist.net/v1/oauth2/token`
let mal_keys = await fetch(url, {
    method: "POST",
    headers:{
        'Content-type':'application/x-www-form-urlencoded'
    },
    body:`client_id=${config.CLIENT_ID}&client_secret=${config.CLIENT_SECRET}&grant_type=refresh_token&refresh_token=${mal_token.refresh_token}`
})

const new_keys = await mal_keys.json()
console.log(new_keys)
await fs.writeFileSync('./keys/mal_token.json', JSON.stringify(new_keys,null,4));
export {}