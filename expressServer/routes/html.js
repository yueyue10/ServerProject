var superagent = require('superagent');
var cheerio = require('cheerio');

function getWeiXinHtml(res, webUrl = "https://mp.weixin.qq.com/s/Dc9h48oNsh82I760U1OdYg") {
    superagent.get(webUrl).end(function (err, sres) {
        let result = {}
        if (err) result.error = err
        let $ = cheerio.load(sres.text);
        let items = [];
        let test = []
        $('div.rich_media_content').children().each(function (i, elem) {
            //测试代码
            let content = {}
            test[i] = $(this).html()
            //
            if ($(this).is('p')) {
                let text = $(this).find('span').text();
                if (text) content.text = text
                let image = $(this).find('img').attr('data-src');
                if (image) content.image = image
            }
            if ($(this).is('section')) {
                let code = $(this).find('code').text();
                if (code) content.code = code
                let text = $(this).find('span').text();
                if (text) code.title = text
            }
            content.text = $(this).find('span').text();
            items[i] = content
        });
        result.content = items
        // result.content = test
        console.log("result", result)
        res.json(result)  //返回json数据
        return result
    })
}

module.exports = {
    getWeiXinHtml
}

