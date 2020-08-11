const express = require('express');
const router = express.Router();

/**
 * @apiDescription 获取grade的诗词列表
 * @api {get} /poetry/grade/poetryList 获取grade的诗词列表
 * @apiName /grade/poetryList
 * @apiGroup poetry
 * @apiSuccess {json} result
 * @apiSuccessExample {json} Success-Response:
 *  {
 *    "url" : ""
 *  }
 * @apiSampleRequest http://81.68.145.189:3000/poetry/grade/poetryList
 * @apiVersion 0.0.0
 */
router.get('/grade/poetryList', function (req, res, next) {
    let poetryList = [{"title": "《咏鹅》", "time": "[唐]", "author": "骆宾王", "content": ["鹅，鹅，鹅，曲项向天歌。", "白毛浮绿水，红掌拨清波。"]}]
    res.json(poetryList);
});

module.exports = router;
