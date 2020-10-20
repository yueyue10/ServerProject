"use strict";
//引入第三方模块
const request = require('request-promise');

async function getTokenApi(res, appid, secret) {
    let token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential" +
        `&appid=${appid}&secret=${secret}`
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
