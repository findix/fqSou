#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import subprocess

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import Config
import Log


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        else:
            self.write('error:' + str(status_code))


class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        if username == Config.read_config("config.properties", "admin",
                                          "admin_username") and password == Config.read_config("config.properties",
                                                                                               "admin", "admin_passwd"):
            self.set_secure_cookie("user", username)
        self.redirect("/admin")


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.set_secure_cookie("user", "")
        self.redirect("/")


class ChangePasswdHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        password = self.get_argument("password")
        Config.write_config("config.properties", "admin", "admin_passwd", password)
        self.redirect("/admin")


class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        print Config.read_config("config.properties", "config", "shadowsocks_config")
        json = open(Config.read_config("config.properties", "config", "shadowsocks_config"), "r")
        self.render("admin.html", json=json.read())


class SaveHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        json = self.get_argument("json")
        config = open(Config.read_config("config.properties", "config", "shadowsocks_config"), "w")
        config.write(json)
        config.close()
        status = subprocess.call("ssserver -c /etc/shadowsocks.json -d restart", shell=True)
        self.write("成功" if status == 0 else "失败")


class LogHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        logs = Log.get_logs(r"/var/log/port-ip-monitor.log")
        logs.reverse()
        self.render("log.html", logs=logs)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = tornado.web.Application(
        handlers=[
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/changepasswd", ChangePasswdHandler),
            (r"/admin", AdminHandler),
            (r"/save", SaveHandler),
            (r"/log", LogHandler),
            (r".*", BaseHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=False,
        login_url=r"/login",
        cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo="
    )
    application.listen(3000)
    tornado.ioloop.IOLoop.instance().start()