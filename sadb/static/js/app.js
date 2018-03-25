"use strict";

angular.module('sadb',['ngRoute','bw.paging','tableSort','ui.select','ngSanitize'])
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
            .when("/taxonomy",{
                templateUrl:"/static/pages/taxonomy.html",
                controller: "taxonomyController"
            })
            .when("/gene_info",{
                templateUrl:"/static/pages/test.html",
                controller: "testController"
            })
            .when("/browse",{
                templateUrl:"/static/pages/browse.html",
                controller: "browseController"
            });
    })
    .service('sadbService',function () {
        this.getBrowserBaseUrl = function () {
            return "127.0.0.1";
            };
        this.getBrowserDataHubNaseUrl = function () {
            // return "192.168.0.101/sadb";
            return "0.0.0.0:3000";
        };
        this.getAPIBaseUrl = function () {
            //return "/sadb"
            return ""
        }
    })
    .controller('navigation', navigation);
    function navigation($scope,$http,$routeParams,sadbService) {
        console.log("navi work")
        $("input").keyup(function(event){
            if(event.keyCode ==13){
            $scope.search_query();
        }
    });
    var flag=0
    var base_url = sadbService.getAPIBaseUrl();
    $scope.search_query = function () {
        var query_item = $('#search').val();

        if(/[@#\$%\^&\*]+/g.test(query_item)){
            console.log(query_item)
            alert("Invalid input");
            flag=1;
            history.back();
        }
        if(flag==0){
            if(query_item.indexOf("SR")==0){
                $scope.filter_sra(query_item)
            }
            else {
                $scope.filter_gene(query_item)
            }
        }


        }
        $scope.filter_sra = function (query_sra) {
            window.open(base_url+"#/sra_info?sra="+query_sra,"_self")
        }
        $scope.filter_gene = function (query_gene) {
            window.open(base_url+"#/gene_info?gene_id="+query_gene,"_self")
        }

    }

