var express = require("express");
var router = express.Router();
var path = require("path");
var pjson = require("../package.json");

/* GET home page. */
router.get("/", function (req, res, next) {
  let base_path = pjson.apidoc.url;
  res.render("index", {
    title: "Express Server",
    api_path: "/apidoc/",
    socketio_path: "/socketio",
    sockettest_path: "/sockettest",
    socketjade_path: "/socketjade",
    sockettest_domain_path: base_path + "/sockettest/domain",
  });
});

router.get("/socketio", function (req, res) {
  res.sendFile(
    path.join(path.resolve(__dirname, ".."), "public/socketio.html")
  );
});

router.get("/sockettest", function (req, res) {
  res.sendFile(path.join(path.resolve(__dirname, ".."), "public/socket.html"));
});

router.get("/sockettest/domain", function (req, res) {
  res.sendFile(
    path.join(path.resolve(__dirname, ".."), "public/socket_domain.html")
  );
});

router.get("/socketjade", function (req, res, next) {
  res.render("socket", { title: "socket测试" });
});

module.exports = router;
