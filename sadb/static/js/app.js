"use strict";

angular.module('sadb',['ngRoute','bw.paging','tableSort'])
    .config(function($routeProvider){
        $routeProvider
            .when("/", {
                templateUrl: "/static/pages/home.html",
                controller: "HomeController"
            })
            .when("/sra_info",{
                templateUrl:"/static/pages/sra.html",
                controller: "SRAController"
            })
            .when("/gene_info",{
                templateUrl:"/static/pages/test.html",
                controller: "testController"
            })
            .when("/information",{
                templateUrl:"/static/pages/information.html",
                controller: "infoController"
            });
    })
    .service('sadbService',function () {
        this.getBrowserBaseUrl = function () {
            return "127.0.0.1";
            };
        this.getBrowserDataHubNaseUrl = function () {
            // return "192.168.0.101/sadb";
            return "0.0.0.0:5000";
        };
        this.getAPIBaseUrl = function () {
            //return "/sadb"
            return ""
        }
    });