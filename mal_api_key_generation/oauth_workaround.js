import pkceChallenge from "pkce-challenge";
import config from '../keys/config.json' assert {type:'json'}
import express from "express"
import fs from 'fs';

const make_final_html_page = async(token_req_response) =>{
    return `<!DOCTYPE html>
    <style>
        .token{
            background-color: black;
            color: black;
        }
        .token:hover{
            color: white;
        }
    </style>
    <head>
    <title>Response from MAL</title>
    </head>
    <body>
        <div>
            Response from MAL
        </div>
        <div>
            Days The Key Is Active:
            <div>
                ${token_req_response.expires_in / 86400}
            </div>
            Access Token:
            <div class="token">
                ${token_req_response.access_token}
            </div>
            Refresh Token:
            <div class="token">
            ${token_req_response.refresh_token}
            </div>
        </div>
    </body>`
}


const app = express()
app.get('/', async (req, res) =>{
    console.log(`req: ${req}`)
    let code = req.query.code
    let url = `https://myanimelist.net/v1/oauth2/token`
    let mal_keys = await fetch(url, {
        method: "POST",
        headers:{
            'Content-type':'application/x-www-form-urlencoded'
        },
        body:`client_id=${config.CLIENT_ID}&grant_type=authorization_code&client_secret=${config.CLIENT_SECRET}&code=${code}&code_verifier=${challengeVal.code_challenge}`
    })
    console.log(mal_keys)
    if(mal_keys.status >= 400 && mal_keys.status < 600){
        res.status(400).send('fucked up')
        console.log('status: ',mal_keys.status)
        console.log('status text: ',mal_keys.statusText)
        console.log('json: ', await mal_keys.json())
        console.log('text: ', mal_keys.text())
        // mal_keys.then((values) => console.log(values))
    }
    else{
    console.log('status: ',mal_keys.status)
    console.log('status text: ',mal_keys.statusText)
    const bearer = await mal_keys.json().then((val) => {return val})
    console.log('json: ', bearer)
    res.send(await make_final_html_page(bearer))
    fs.writeFileSync('./keys/mal_token.json', JSON.stringify(bearer,null,4));
    }
})

const challengeVal = await pkceChallenge(128)
// https://myanimelist.net/apiconfig/references/authorization
const  first_url = `https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id=${config.CLIENT_ID}&code_challenge=${challengeVal.code_challenge}&code_challenge_method=plain`
console.log("Put this Link in a Web Browser:\n",first_url)

app.listen(5500)
// main()
export {}