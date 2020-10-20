"use strict";
//引入第三方模块
const nodemailer = require("nodemailer");

//
function sendMail(res, mail, code) {
    // 创建发送邮件的对象
    let transporter = nodemailer.createTransport({
        //node_modules/nodemailer/lib/well-known/services.json  查看相关的配置，如果使用qq邮箱，就查看qq邮箱的相关配置
        host: "smtp.qq.com",
        port: 465,
        secure: true, // true for 465, false for other ports
        auth: {
            //发送者邮箱
            user: '1650432983@qq.com', // generated ethereal user
            //pass 不是邮箱账户的密码而是stmp的授权码（必须是相应邮箱的stmp授权码）
            //邮箱---设置--账户--POP3/SMTP服务 开启--成功开启POP3/SMTP服务,在第三方客户端登录时，密码框请输入以下授权码：
            pass: 'oejibamllhlgdehb'
        }
    });

    // 邮件的相关信息
    let mailOption = {
        //发送者邮箱
        from: '1650432983@qq.com', // sender address
        //接收者邮箱，多个邮箱用逗号间隔
        to: mail, // list of receivers
        //邮件标题
        subject: "个人工具箱邮箱注册验证",
        //文件内容，发送文件是text格式或者html格式，二者只能选择一个
        // text: "Hello world?", // plain text body
        html: code
    }

    // 发送邮件
    transporter.sendMail(mailOption, (error, info) => {
        console.log(error);
        console.log(info);
        if (error) {
            res.json({msg: "发送失败"})
        } else {
            res.json({msg: "发送成功"})
        }
    })
}

module.exports = sendMail;
