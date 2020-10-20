"use strict";
//引入第三方模块
const request = require('request-promise');

const pubAcc = {
    appid: 'wx0cf966d7586ab293',
    secret: '2757f050fb94ab0dafd1b7f117b940bb'
}

// const pubAcc = {
//     appid: 'wx1133701f39faa59a',
//     secret: 'e8070faf725e27f8f275969435c0a2b2'
// }

async function getTokenApi(res) {
    let token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential" +
        `&appid=${pubAcc.appid}&secret=${pubAcc.secret}`
    let webData = await getWebData(token_url)
    console.log("webData", webData)
    res.json(webData)
}

async function getWebData(web_url) {
    return new Promise((resolve, reject) => {
        request(web_url).then(html => {
            if (typeof (html) == "string")
                html = JSON.parse(html)
            resolve(html);
        }).catch(err => {
            reject(err);
        })
    })
}

module.exports = getTokenApi;
