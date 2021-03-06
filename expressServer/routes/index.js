var express = require("express");
var router = express.Router();
var path = require("path");
var pjson = require("../package.json");

/* GET home page. */
router.get("/", function (req, res, next) {
  let base_path = pjson.apidoc.url;
  res.render("index", {
    title: "Express Server",
    api_path: base_path + "/apidoc/",
    socket_demo_path: "/socket_demo",
    socket_ip_path: "/socket_ip",
    socket_jade_path: "/socketjade",
    socket_domain_path: base_path + "/socket_domain",
  });
});

router.get("/socket_demo", function (req, res) {
  res.sendFile(
    path.join(path.resolve(__dirname, ".."), "public/socket_demo.html")
  );
});

router.get("/socket_ip", function (req, res) {
  res.sendFile(path.join(path.resolve(__dirname, ".."), "public/socket_ip.html"));
});

router.get("/socket_domain", function (req, res) {
  res.sendFile(
    path.join(path.resolve(__dirname, ".."), "public/socket_domain.html")
  );
});

router.get("/socketjade", function (req, res, next) {
  res.render("socket", { title: "socket测试" });
});

module.exports = router;
